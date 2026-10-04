"""
Tracker module for maintaining face identity across frames.
Uses simple centroid tracking with disappearance handling.
"""

import numpy as np
from typing import Dict, List, Tuple, Optional
from collections import OrderedDict
from scipy.spatial import distance as dist


class CentroidTracker:
    """
    Simple centroid-based tracker for maintaining face identity across frames.
    Tracks objects based on their centroid positions.
    """
    
    def __init__(self, max_disappeared: int = 30):
        """
        Initialize the centroid tracker.
        
        Args:
            max_disappeared: Maximum frames an object can disappear before deregistration
        """
        self.next_object_id = 0
        self.objects = OrderedDict()  # {object_id: centroid}
        self.disappeared = OrderedDict()  # {object_id: disappeared_count}
        self.max_disappeared = max_disappeared
        
        # Map track IDs to visitor IDs
        self.track_to_visitor = {}  # {track_id: visitor_id}
        
        # Track bounding boxes
        self.bboxes = OrderedDict()  # {object_id: (x1, y1, x2, y2)}
    
    def register(self, centroid: np.ndarray, bbox: Tuple[int, int, int, int]) -> int:
        """
        Register a new object with its centroid.
        
        Args:
            centroid: (x, y) coordinates of object center
            bbox: Bounding box (x1, y1, x2, y2)
            
        Returns:
            Assigned track ID
        """
        track_id = self.next_object_id
        self.objects[track_id] = centroid
        self.disappeared[track_id] = 0
        self.bboxes[track_id] = bbox
        self.next_object_id += 1
        
        return track_id
    
    def deregister(self, object_id: int):
        """
        Remove an object from tracking.
        
        Args:
            object_id: Track ID to remove
        """
        if object_id in self.objects:
            del self.objects[object_id]
        if object_id in self.disappeared:
            del self.disappeared[object_id]
        if object_id in self.bboxes:
            del self.bboxes[object_id]
        if object_id in self.track_to_visitor:
            del self.track_to_visitor[object_id]
    
    def update(
        self, 
        detections: List[Tuple[int, int, int, int]]
    ) -> Dict[int, Tuple[int, int, int, int]]:
        """
        Update tracker with new detections.
        
        Args:
            detections: List of bounding boxes [(x1, y1, x2, y2), ...]
            
        Returns:
            Dictionary mapping {track_id: bbox}
        """
        # If no detections, mark all existing objects as disappeared
        if len(detections) == 0:
            for object_id in list(self.disappeared.keys()):
                self.disappeared[object_id] += 1
                
                # Deregister if disappeared too long
                if self.disappeared[object_id] > self.max_disappeared:
                    self.deregister(object_id)
            
            return self.bboxes.copy()
        
        # Calculate centroids from bounding boxes
        input_centroids = np.zeros((len(detections), 2), dtype="int")
        
        for (i, (x1, y1, x2, y2)) in enumerate(detections):
            cX = int((x1 + x2) / 2.0)
            cY = int((y1 + y2) / 2.0)
            input_centroids[i] = (cX, cY)
        
        # If no objects being tracked, register all
        if len(self.objects) == 0:
            for i in range(len(input_centroids)):
                self.register(input_centroids[i], detections[i])
        
        # Otherwise, try to match with existing objects
        else:
            object_ids = list(self.objects.keys())
            object_centroids = list(self.objects.values())
            
            # Compute distance between each pair of objects and centroids
            D = dist.cdist(np.array(object_centroids), input_centroids)
            
            # Find minimum distance matches
            rows = D.min(axis=1).argsort()
            cols = D.argmin(axis=1)[rows]
            
            used_rows = set()
            used_cols = set()
            
            for (row, col) in zip(rows, cols):
                if row in used_rows or col in used_cols:
                    continue
                
                # Update the object
                object_id = object_ids[row]
                self.objects[object_id] = input_centroids[col]
                self.bboxes[object_id] = detections[col]
                self.disappeared[object_id] = 0
                
                used_rows.add(row)
                used_cols.add(col)
            
            # Handle disappeared objects
            unused_rows = set(range(D.shape[0])) - used_rows
            for row in unused_rows:
                object_id = object_ids[row]
                self.disappeared[object_id] += 1
                
                if self.disappeared[object_id] > self.max_disappeared:
                    self.deregister(object_id)
            
            # Register new objects
            unused_cols = set(range(D.shape[1])) - used_cols
            for col in unused_cols:
                self.register(input_centroids[col], detections[col])
        
        return self.bboxes.copy()
    
    def assign_visitor_id(self, track_id: int, visitor_id: str):
        """
        Map a track ID to a visitor ID.
        
        Args:
            track_id: Internal tracking ID
            visitor_id: Recognized visitor ID
        """
        self.track_to_visitor[track_id] = visitor_id
    
    def get_visitor_id(self, track_id: int) -> Optional[str]:
        """
        Get visitor ID for a track ID.
        
        Args:
            track_id: Internal tracking ID
            
        Returns:
            Visitor ID or None
        """
        return self.track_to_visitor.get(track_id)
    
    def get_all_tracked_objects(self) -> Dict[int, Dict]:
        """
        Get all currently tracked objects with their info.
        
        Returns:
            Dictionary of tracked objects
        """
        result = {}
        for track_id, bbox in self.bboxes.items():
            result[track_id] = {
                'bbox': bbox,
                'visitor_id': self.get_visitor_id(track_id),
                'disappeared': self.disappeared.get(track_id, 0)
            }
        return result


if __name__ == "__main__":
    # Test tracker
    tracker = CentroidTracker(max_disappeared=30)
    
    # Simulate detections
    frame1_detections = [(100, 100, 200, 200), (300, 300, 400, 400)]
    tracked1 = tracker.update(frame1_detections)
    print(f"Frame 1: {tracked1}")
    
    frame2_detections = [(105, 105, 205, 205), (305, 305, 405, 405)]
    tracked2 = tracker.update(frame2_detections)
    print(f"Frame 2: {tracked2}")
    
    # Assign visitor IDs
    tracker.assign_visitor_id(0, "VISITOR_001")
    tracker.assign_visitor_id(1, "VISITOR_002")
    
    print(f"All tracked: {tracker.get_all_tracked_objects()}")
