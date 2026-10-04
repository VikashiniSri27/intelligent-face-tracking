"""
Database module for storing visitor information and events.
Uses SQLite for simplicity and portability.
"""

import sqlite3
import json
from datetime import datetime
from typing import Optional, List, Dict, Tuple
import numpy as np


class Database:
    """Handles all database operations for visitor tracking."""
    
    def __init__(self, db_path: str = "database/visitors.db"):
        """
        Initialize database connection and create tables if needed.
        
        Args:
            db_path: Path to SQLite database file
        """
        self.db_path = db_path
        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self.cursor = self.conn.cursor()
        self._create_tables()
    
    def _create_tables(self):
        """Create necessary database tables."""
        
        # Visitors table - stores unique visitor information
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS visitors (
                visitor_id TEXT PRIMARY KEY,
                first_seen TIMESTAMP,
                last_seen TIMESTAMP,
                total_visits INTEGER DEFAULT 1,
                embedding BLOB
            )
        """)
        
        # Events table - stores all entry/exit events
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS events (
                event_id INTEGER PRIMARY KEY AUTOINCREMENT,
                visitor_id TEXT,
                event_type TEXT,
                timestamp TIMESTAMP,
                image_path TEXT,
                FOREIGN KEY (visitor_id) REFERENCES visitors(visitor_id)
            )
        """)
        
        self.conn.commit()
    
    def register_visitor(self, visitor_id: str, embedding: np.ndarray) -> bool:
        """
        Register a new visitor in the database.
        
        Args:
            visitor_id: Unique identifier for the visitor
            embedding: Face embedding vector (512-dimensional)
            
        Returns:
            True if registration successful, False otherwise
        """
        try:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            # Convert numpy array to bytes for storage
            embedding_bytes = embedding.tobytes()
            
            self.cursor.execute("""
                INSERT INTO visitors (visitor_id, first_seen, last_seen, embedding)
                VALUES (?, ?, ?, ?)
            """, (visitor_id, timestamp, timestamp, embedding_bytes))
            
            self.conn.commit()
            return True
            
        except sqlite3.IntegrityError:
            # Visitor already exists
            return False
        except Exception as e:
            print(f"Error registering visitor: {e}")
            return False
    
    def update_visitor_last_seen(self, visitor_id: str):
        """
        Update the last_seen timestamp for a visitor.
        
        Args:
            visitor_id: Unique identifier for the visitor
        """
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        self.cursor.execute("""
            UPDATE visitors 
            SET last_seen = ?, total_visits = total_visits + 1
            WHERE visitor_id = ?
        """, (timestamp, visitor_id))
        
        self.conn.commit()
    
    def get_all_embeddings(self) -> List[Tuple[str, np.ndarray]]:
        """
        Retrieve all stored face embeddings.
        
        Returns:
            List of tuples (visitor_id, embedding)
        """
        self.cursor.execute("SELECT visitor_id, embedding FROM visitors")
        results = self.cursor.fetchall()
        
        embeddings = []
        for visitor_id, embedding_bytes in results:
            # Convert bytes back to numpy array
            embedding = np.frombuffer(embedding_bytes, dtype=np.float32)
            embeddings.append((visitor_id, embedding))
        
        return embeddings
    
    def log_event(self, visitor_id: str, event_type: str, image_path: str) -> int:
        """
        Log an entry or exit event.
        
        Args:
            visitor_id: Unique identifier for the visitor
            event_type: "ENTRY" or "EXIT"
            image_path: Path to saved face image
            
        Returns:
            Event ID of the logged event
        """
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        self.cursor.execute("""
            INSERT INTO events (visitor_id, event_type, timestamp, image_path)
            VALUES (?, ?, ?, ?)
        """, (visitor_id, event_type, timestamp, image_path))
        
        self.conn.commit()
        return self.cursor.lastrowid
    
    def get_unique_visitor_count(self) -> int:
        """
        Get total number of unique visitors.
        
        Returns:
            Count of unique visitors
        """
        self.cursor.execute("SELECT COUNT(*) FROM visitors")
        count = self.cursor.fetchone()[0]
        return count
    
    def get_all_events(self) -> List[Dict]:
        """
        Retrieve all events from database.
        
        Returns:
            List of event dictionaries
        """
        self.cursor.execute("""
            SELECT event_id, visitor_id, event_type, timestamp, image_path
            FROM events
            ORDER BY timestamp DESC
        """)
        
        events = []
        for row in self.cursor.fetchall():
            events.append({
                'event_id': row[0],
                'visitor_id': row[1],
                'event_type': row[2],
                'timestamp': row[3],
                'image_path': row[4]
            })
        
        return events
    
    def get_visitor_info(self, visitor_id: str) -> Optional[Dict]:
        """
        Get information about a specific visitor.
        
        Args:
            visitor_id: Unique identifier for the visitor
            
        Returns:
            Dictionary with visitor information or None
        """
        self.cursor.execute("""
            SELECT visitor_id, first_seen, last_seen, total_visits
            FROM visitors
            WHERE visitor_id = ?
        """, (visitor_id,))
        
        row = self.cursor.fetchone()
        if row:
            return {
                'visitor_id': row[0],
                'first_seen': row[1],
                'last_seen': row[2],
                'total_visits': row[3]
            }
        return None
    
    def close(self):
        """Close database connection."""
        self.conn.close()


if __name__ == "__main__":
    # Test database functionality
    db = Database("database/test_visitors.db")
    
    # Test registration
    test_embedding = np.random.rand(512).astype(np.float32)
    db.register_visitor("VISITOR_001", test_embedding)
    
    # Test event logging
    db.log_event("VISITOR_001", "ENTRY", "logs/entries/test.jpg")
    
    # Test retrieval
    print(f"Unique visitors: {db.get_unique_visitor_count()}")
    print(f"All events: {db.get_all_events()}")
    
    db.close()
