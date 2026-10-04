"""
Main application for Intelligent Face Tracking System.
Detects, recognizes, tracks faces and counts unique visitors.
"""

import cv2
import numpy as np
import json
import os
from datetime import datetime
from typing import Dict, List, Optional, Tuple
from ultralytics import YOLO

from database import Database
from logger import EventLogger
from recognizer import FaceRecognizer
from tracker import CentroidTracker


class FaceTrackingSystem:
    """Main system for face detection, recognition, tracking and counting."""
    
    def __init__(self, config_path: str = "config.json"):
        """
        Initialize the face tracking system.
        
        Args:
            config_path: Path to configuration file
        """
        # Load configuration
        with open(config_path, 'r') as f:
            self.config = json.load(f)
        
        # Initialize components
        self.logger = EventLogger(self.config['log_path'])
        self.database = Database(self.config['database_path'])
        self.recognizer = FaceRecognizer(self.config['similarity_threshold'])
        self.tracker = CentroidTracker(self.config['max_disappear_frames'])
        
        # Load YOLO for face detection
        print("Loading YOLO model...")
        self.yolo = YOLO('yolov8n.pt')  # YOLOv8 nano for speed
        print("YOLO model loaded successfully")
        
        # Tracking variables
        self.frame_count = 0
        self.active_visitors = {}  # {track_id: {'visitor_id': str, 'has_entry': bool}}
        
        # Create output directories
        os.makedirs(self.config['entries_folder'], exist_ok=True)
        os.makedirs(self.config['exits_folder'], exist_ok=True)
        
        # Log system start
        video_source = self.config.get('rtsp_url') or self.config['video_source']
        self.logger.system_start(video_source)
    
    def detect_faces(self, frame: np.ndarray) -> List[Tuple[int, int, int, int]]:
        """
        Detect faces in a frame using YOLO.
        
        Args:
            frame: Input BGR frame
            
        Returns:
            List of bounding boxes [(x1, y1, x2, y2), ...]
        """
        # Run YOLO detection
        results = self.yolo(frame, verbose=False)
        
        faces = []
        for result in results:
            boxes = result.boxes
            
            for box in boxes:
                # Get bounding box coordinates
                x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()
                confidence = float(box.conf[0])
                
                # Filter by confidence and minimum size
                w = x2 - x1
                h = y2 - y1
                
                if confidence >= self.config['confidence_threshold'] and \
                   w >= self.config['min_face_size'] and \
                   h >= self.config['min_face_size']:
                    
                    faces.append((int(x1), int(y1), int(x2), int(y2)))
        
        return faces
    
    def crop_face(self, frame: np.ndarray, bbox: Tuple[int, int, int, int]) -> np.ndarray:
        """
        Crop face from frame using bounding box.
        
        Args:
            frame: Input BGR frame
            bbox: Bounding box (x1, y1, x2, y2)
            
        Returns:
            Cropped face image
        """
        x1, y1, x2, y2 = bbox
        
        # Ensure coordinates are within frame bounds
        h, w = frame.shape[:2]
        x1 = max(0, x1)
        y1 = max(0, y1)
        x2 = min(w, x2)
        y2 = min(h, y2)
        
        face = frame[y1:y2, x1:x2]
        return face
    
    def save_face_image(
        self, 
        face: np.ndarray, 
        visitor_id: str, 
        event_type: str
    ) -> str:
        """
        Save cropped face image to disk.
        
        Args:
            face: Cropped face image
            visitor_id: Unique visitor identifier
            event_type: "ENTRY" or "EXIT"
            
        Returns:
            Path to saved image
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
        filename = f"{visitor_id}_{timestamp}.jpg"
        
        if event_type == "ENTRY":
            folder = self.config['entries_folder']
        else:
            folder = self.config['exits_folder']
        
        # Create date subfolder
        date_folder = datetime.now().strftime("%Y-%m-%d")
        full_folder = os.path.join(folder, date_folder)
        os.makedirs(full_folder, exist_ok=True)
        
        filepath = os.path.join(full_folder, filename)
        cv2.imwrite(filepath, face)
        
        return filepath
    
    def recognize_or_register(
        self, 
        face: np.ndarray, 
        track_id: int
    ) -> Optional[str]:
        """
        Recognize face or register as new visitor.
        
        Args:
            face: Cropped face image
            track_id: Tracking ID
            
        Returns:
            Visitor ID
        """
        # Generate embedding
        embedding = self.recognizer.get_embedding(face)
        
        if embedding is None:
            return None
        
        # Get all known embeddings from database
        known_embeddings = self.database.get_all_embeddings()
        
        # Try to find match
        match = self.recognizer.find_matching_face(embedding, known_embeddings)
        
        if match:
            # Known visitor
            visitor_id, confidence = match
            self.logger.face_recognized(visitor_id, confidence)
            self.logger.embedding_generated(visitor_id)
            
            return visitor_id
        else:
            # New visitor - register
            visitor_count = self.database.get_unique_visitor_count()
            visitor_id = f"VISITOR_{visitor_count + 1:03d}"
            
            # Save to database
            self.database.register_visitor(visitor_id, embedding)
            
            self.logger.face_registered(visitor_id)
            self.logger.embedding_generated(visitor_id)
            self.logger.unique_count_update(self.database.get_unique_visitor_count())
            
            return visitor_id
    
    def handle_entry(self, visitor_id: str, face: np.ndarray):
        """
        Handle visitor entry event.
        
        Args:
            visitor_id: Unique visitor identifier
            face: Cropped face image
        """
        # Save face image
        image_path = self.save_face_image(face, visitor_id, "ENTRY")
        
        # Log to database
        self.database.log_event(visitor_id, "ENTRY", image_path)
        
        # Log event
        self.logger.entry_logged(visitor_id)
    
    def handle_exit(self, visitor_id: str, face: np.ndarray):
        """
        Handle visitor exit event.
        
        Args:
            visitor_id: Unique visitor identifier
            face: Cropped face image
        """
        # Save face image
        image_path = self.save_face_image(face, visitor_id, "EXIT")
        
        # Log to database
        self.database.log_event(visitor_id, "EXIT", image_path)
        
        # Log event
        self.logger.exit_logged(visitor_id)
    
    def process_frame(self, frame: np.ndarray) -> np.ndarray:
        """
        Process a single frame.
        
        Args:
            frame: Input BGR frame
            
        Returns:
            Annotated frame with bounding boxes and IDs
        """
        self.frame_count += 1
        
        # Skip frames based on configuration
        if self.frame_count % self.config['detection_skip_frames'] != 0:
            return frame
        
        # Detect faces
        face_bboxes = self.detect_faces(frame)
        
        if face_bboxes:
            self.logger.face_detected(self.frame_count)
        
        # Update tracker
        tracked_objects = self.tracker.update(face_bboxes)
        
        # Process each tracked object
        current_track_ids = set()
        
        for track_id, bbox in tracked_objects.items():
            current_track_ids.add(track_id)
            
            # Check if this is a new track
            if track_id not in self.active_visitors:
                # Crop face
                face = self.crop_face(frame, bbox)
                
                if face.size > 0:
                    # Recognize or register
                    visitor_id = self.recognize_or_register(face, track_id)
                    
                    if visitor_id:
                        # Assign visitor ID to track
                        self.tracker.assign_visitor_id(track_id, visitor_id)
                        
                        # Mark as active
                        self.active_visitors[track_id] = {
                            'visitor_id': visitor_id,
                            'has_entry': True,
                            'last_bbox': bbox
                        }
                        
                        # Log entry
                        self.handle_entry(visitor_id, face)
                        self.logger.tracking_started(visitor_id, track_id)
            else:
                # Update last seen bbox
                self.active_visitors[track_id]['last_bbox'] = bbox
        
        # Check for exits (tracks that disappeared)
        disappeared_tracks = set(self.active_visitors.keys()) - current_track_ids
        
        for track_id in disappeared_tracks:
            visitor_info = self.active_visitors[track_id]
            visitor_id = visitor_info['visitor_id']
            last_bbox = visitor_info['last_bbox']
            
            # Crop last known face
            face = self.crop_face(frame, last_bbox)
            
            if face.size > 0:
                # Log exit
                self.handle_exit(visitor_id, face)
                self.logger.tracking_lost(visitor_id, track_id)
            
            # Remove from active
            del self.active_visitors[track_id]
        
        # Draw annotations
        annotated_frame = frame.copy()
        
        for track_id, bbox in tracked_objects.items():
            visitor_id = self.tracker.get_visitor_id(track_id)
            
            if visitor_id:
                x1, y1, x2, y2 = bbox
                
                # Draw bounding box
                cv2.rectangle(annotated_frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                
                # Draw visitor ID
                label = f"{visitor_id}"
                cv2.putText(
                    annotated_frame, 
                    label, 
                    (x1, y1 - 10),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.6,
                    (0, 255, 0),
                    2
                )
        
        # Draw unique count
        unique_count = self.database.get_unique_visitor_count()
        cv2.putText(
            annotated_frame,
            f"Unique Visitors: {unique_count}",
            (10, 30),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 0, 255),
            2
        )
        
        return annotated_frame
    
    def run(self):
        """Run the face tracking system."""
        # Determine video source
        video_source = self.config.get('rtsp_url')
        if not video_source or video_source == "":
            video_source = self.config['video_source']
        
        # Open video stream
        cap = cv2.VideoCapture(video_source)
        
        if not cap.isOpened():
            self.logger.error(f"Failed to open video source: {video_source}")
            return
        
        # Get video properties
        fps = int(cap.get(cv2.CAP_PROP_FPS))
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        
        self.logger.info(f"Video properties: {width}x{height} @ {fps} FPS")
        
        # Optional: Save output video
        output_path = "output/processed_video.mp4"
        os.makedirs("output", exist_ok=True)
        
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
        
        try:
            while True:
                ret, frame = cap.read()
                
                if not ret:
                    break
                
                # Process frame
                annotated_frame = self.process_frame(frame)
                
                # Write to output
                out.write(annotated_frame)
                
                # Display (optional - comment out for headless systems)
                cv2.imshow('Face Tracking System', annotated_frame)
                
                # Press 'q' to quit
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
        
        finally:
            # Cleanup
            cap.release()
            out.release()
            cv2.destroyAllWindows()
            
            # Get final statistics BEFORE closing database
            unique_count = self.database.get_unique_visitor_count()
            total_events = len(self.database.get_all_events())
            
            self.logger.system_stop(unique_count, total_events)
            self.logger.info(f"Processed video saved to: {output_path}")
            
            # Print statistics while database is still open
            self.print_statistics()
            
            # NOW close database
            self.database.close()
    
    def print_statistics(self):
        """Print final statistics."""
        print("\n" + "="*60)
        print("FINAL STATISTICS")
        print("="*60)
        
        unique_count = self.database.get_unique_visitor_count()
        events = self.database.get_all_events()
        
        print(f"Total Unique Visitors: {unique_count}")
        print(f"Total Events Logged: {len(events)}")
        
        # Count entries and exits
        entries = sum(1 for e in events if e['event_type'] == 'ENTRY')
        exits = sum(1 for e in events if e['event_type'] == 'EXIT')
        
        print(f"Total Entries: {entries}")
        print(f"Total Exits: {exits}")
        print("="*60 + "\n")


def main():
    """Main entry point."""
    print("="*60)
    print("INTELLIGENT FACE TRACKING SYSTEM")
    print("="*60)
    print()
    
    # Initialize system
    system = FaceTrackingSystem("config.json")
    
    # Run tracking (statistics printed inside run method now)
    system.run()


if __name__ == "__main__":
    main()
