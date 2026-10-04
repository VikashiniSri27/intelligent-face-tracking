"""
Face recognition module using InsightFace.
Generates face embeddings and compares them for identification.
"""

import cv2
import numpy as np
from typing import Optional, Tuple, List
from insightface.app import FaceAnalysis
from sklearn.metrics.pairwise import cosine_similarity


class FaceRecognizer:
    """Handles face embedding generation and recognition using InsightFace."""
    
    def __init__(self, similarity_threshold: float = 0.5):
        """
        Initialize InsightFace model.
        
        Args:
            similarity_threshold: Minimum similarity score to consider faces as same person
        """
        self.similarity_threshold = similarity_threshold
        
        # Initialize InsightFace
        print("Loading InsightFace model...")
        self.app = FaceAnalysis(
            name='buffalo_l',
            providers=['CPUExecutionProvider']  # Use GPU if available: 'CUDAExecutionProvider'
        )
        self.app.prepare(ctx_id=0, det_size=(640, 640))
        print("InsightFace model loaded successfully")
    
    def get_embedding(self, face_image: np.ndarray) -> Optional[np.ndarray]:
        """
        Generate face embedding from a cropped face image.
        
        Args:
            face_image: RGB face image (cropped)
            
        Returns:
            512-dimensional embedding vector or None if face not detected
        """
        try:
            # InsightFace expects BGR format
            if len(face_image.shape) == 3 and face_image.shape[2] == 3:
                face_bgr = cv2.cvtColor(face_image, cv2.COLOR_RGB2BGR)
            else:
                face_bgr = face_image
            
            # Detect and analyze face
            faces = self.app.get(face_bgr)
            
            if len(faces) > 0:
                # Get the first face's embedding
                embedding = faces[0].embedding
                
                # Normalize embedding
                embedding = embedding / np.linalg.norm(embedding)
                
                return embedding.astype(np.float32)
            else:
                return None
                
        except Exception as e:
            print(f"Error generating embedding: {e}")
            return None
    
    def compare_faces(
        self, 
        embedding1: np.ndarray, 
        embedding2: np.ndarray
    ) -> float:
        """
        Compare two face embeddings using cosine similarity.
        
        Args:
            embedding1: First face embedding
            embedding2: Second face embedding
            
        Returns:
            Similarity score (0 to 1, higher means more similar)
        """
        try:
            # Reshape for sklearn
            emb1 = embedding1.reshape(1, -1)
            emb2 = embedding2.reshape(1, -1)
            
            # Calculate cosine similarity
            similarity = cosine_similarity(emb1, emb2)[0][0]
            
            # Convert from [-1, 1] to [0, 1]
            similarity = (similarity + 1) / 2
            
            return float(similarity)
            
        except Exception as e:
            print(f"Error comparing embeddings: {e}")
            return 0.0
    
    def find_matching_face(
        self, 
        new_embedding: np.ndarray,
        known_embeddings: List[Tuple[str, np.ndarray]]
    ) -> Optional[Tuple[str, float]]:
        """
        Find if the new face matches any known face in database.
        
        Args:
            new_embedding: Embedding of the new face
            known_embeddings: List of (visitor_id, embedding) tuples from database
            
        Returns:
            Tuple of (visitor_id, similarity) if match found, None otherwise
        """
        if not known_embeddings:
            return None
        
        best_match = None
        best_similarity = 0.0
        
        for visitor_id, known_embedding in known_embeddings:
            similarity = self.compare_faces(new_embedding, known_embedding)
            
            if similarity > best_similarity:
                best_similarity = similarity
                best_match = visitor_id
        
        # Return match only if similarity exceeds threshold
        if best_similarity >= self.similarity_threshold:
            return (best_match, best_similarity)
        else:
            return None
    
    def is_same_person(
        self, 
        embedding1: np.ndarray, 
        embedding2: np.ndarray
    ) -> bool:
        """
        Check if two embeddings represent the same person.
        
        Args:
            embedding1: First face embedding
            embedding2: Second face embedding
            
        Returns:
            True if same person, False otherwise
        """
        similarity = self.compare_faces(embedding1, embedding2)
        return similarity >= self.similarity_threshold


if __name__ == "__main__":
    # Test recognizer
    recognizer = FaceRecognizer(similarity_threshold=0.5)
    
    # Test with sample image (you need to provide a test image)
    # test_img = cv2.imread("test_face.jpg")
    # embedding = recognizer.get_embedding(test_img)
    # print(f"Embedding shape: {embedding.shape if embedding is not None else 'None'}")
