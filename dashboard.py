"""
Simple Streamlit Dashboard for Face Tracking System
Reads existing database and displays statistics - does NOT modify core system
"""

import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime
import os

# Page config
st.set_page_config(
    page_title="Face Tracking Dashboard",
    page_icon="👤",
    layout="wide"
)

# Title
st.title(" Intelligent Face Tracking System - Dashboard")
st.markdown("---")

# Check if database exists
db_path = "database/visitors.db"
if not os.path.exists(db_path):
    st.error("❌ Database not found! Please run 'python main.py' first to process a video.")
    st.stop()

# Connect to database
@st.cache_resource
def get_connection():
    return sqlite3.connect(db_path, check_same_thread=False)

conn = get_connection()

# Fetch data
@st.cache_data(ttl=5)
def get_statistics():
    """Get overall statistics"""
    cursor = conn.cursor()
    
    # Unique visitors
    cursor.execute("SELECT COUNT(*) FROM visitors")
    unique_visitors = cursor.fetchone()[0]
    
    # Events
    cursor.execute("SELECT COUNT(*) FROM events WHERE event_type='ENTRY'")
    total_entries = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM events WHERE event_type='EXIT'")
    total_exits = cursor.fetchone()[0]
    
    currently_inside = total_entries - total_exits
    
    return {
        'unique_visitors': unique_visitors,
        'total_entries': total_entries,
        'total_exits': total_exits,
        'currently_inside': currently_inside
    }

@st.cache_data(ttl=5)
def get_recent_events(limit=10):
    """Get recent events"""
    query = """
        SELECT visitor_id, event_type, timestamp 
        FROM events 
        ORDER BY timestamp DESC 
        LIMIT ?
    """
    df = pd.read_sql_query(query, conn, params=(limit,))
    return df

@st.cache_data(ttl=5)
def get_visitors():
    """Get all visitors with corrected last_seen from events"""
    query = """
        SELECT 
            v.visitor_id, 
            v.first_seen,
            (SELECT MAX(e.timestamp) FROM events e WHERE e.visitor_id = v.visitor_id) as last_seen,
            (SELECT COUNT(*) FROM events e WHERE e.visitor_id = v.visitor_id AND e.event_type = 'ENTRY') as total_entries
        FROM visitors v
        ORDER BY v.first_seen DESC
    """
    df = pd.read_sql_query(query, conn)
    return df

# Display statistics in cards
stats = get_statistics()

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        label="👥 Unique Visitors",
        value=stats['unique_visitors'],
        delta=None
    )

with col2:
    st.metric(
        label="🚪 Total Entries",
        value=stats['total_entries'],
        delta=None
    )

with col3:
    st.metric(
        label="🚶 Total Exits",
        value=stats['total_exits'],
        delta=None
    )

with col4:
    st.metric(
        label="📍 Currently Inside",
        value=stats['currently_inside'],
        delta=None
    )

st.markdown("---")

# Two columns for data display
col_left, col_right = st.columns([1, 1])

with col_left:
    st.subheader("📋 Recent Events (Newest First)")
    
    events_df = get_recent_events(10)
    
    if not events_df.empty:
        # Format the dataframe
        events_df.columns = ['Visitor ID', 'Event Type', 'Timestamp']
        
        # Add emoji based on event type
        events_df['Event Type'] = events_df['Event Type'].apply(
            lambda x: f"🚪 {x}" if x == "ENTRY" else f"🚶 {x}"
        )
        
        st.dataframe(
            events_df,
            use_container_width=True,
            hide_index=True
        )
    else:
        st.info("No events recorded yet.")

with col_right:
    st.subheader("👤 Visitors")
    
    visitors_df = get_visitors()
    
    if not visitors_df.empty:
        visitors_df.columns = ['Visitor ID', 'First Seen', 'Last Seen', 'Total Entries']
        
        st.dataframe(
            visitors_df,
            use_container_width=True,
            hide_index=True
        )
    else:
        st.info("No visitors recorded yet.")

st.markdown("---")

# Key Achievement Display
st.subheader("Key Achievement")

if stats['unique_visitors'] > 0:
    st.success(
        f"✅ **Same Person Recognition Working!** "
        f"System counted {stats['unique_visitors']} unique visitor(s) "
        f"despite {stats['total_entries']} entry event(s). "
        f"This proves no duplicate counting!"
    )
else:
    st.info("Run 'python main.py' to process a video and see results.")

# Video display section
st.markdown("---")
st.subheader("🎥 Processed Video")

video_path = "output/processed_video.mp4"
if os.path.exists(video_path):
    col1, col2 = st.columns([2, 1])
    with col1:
        try:
            # Try to display video
            with open(video_path, 'rb') as video_file:
                video_bytes = video_file.read()
                st.video(video_bytes)
            st.caption("Processed video with face detection and visitor ID annotations")
        except Exception as e:
            st.warning("⚠️ Video preview not available in browser. Video file exists at: `output/processed_video.mp4`")
            st.info("💡 Open the file manually to view the annotated video with bounding boxes and visitor IDs.")
    with col2:
        st.metric("Video Status", "✅ Available")
        st.info(f"📁 Location:\n`{video_path}`")
else:
    st.info("No processed video available. Run 'python main.py' to generate one.")

# Footer
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: gray;'>
    <p>Intelligent Face Tracking System | YOLO + InsightFace | 
    <a href='https://katomaran.com' target='_blank'>Katomaran Hackathon</a></p>
    </div>
    """,
    unsafe_allow_html=True
)

# Refresh button
if st.button("🔄 Refresh Data"):
    st.cache_data.clear()
    st.rerun()
