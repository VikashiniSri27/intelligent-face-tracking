"""
View All Visitor Data
Simple script to display all visitor entries, exits, and statistics
"""

import sqlite3
from datetime import datetime

print("="*80)
print("INTELLIGENT FACE TRACKING SYSTEM - DATA VIEWER")
print("="*80)
print()

# Connect to database
conn = sqlite3.connect('database/visitors.db')
cursor = conn.cursor()

# 1. VISITORS TABLE
print("📊 VISITORS (Unique People)")
print("-"*80)
cursor.execute("SELECT visitor_id, first_seen, last_seen, total_visits FROM visitors")
visitors = cursor.fetchall()

if visitors:
    print(f"{'Visitor ID':<15} {'First Seen':<20} {'Last Seen':<20} {'Visits':<10}")
    print("-"*80)
    for row in visitors:
        print(f"{row[0]:<15} {row[1]:<20} {row[2]:<20} {row[3]:<10}")
else:
    print("No visitors registered yet.")

print()
print(f"Total Unique Visitors: {len(visitors)}")
print()

# 2. EVENTS TABLE
print("="*80)
print("📝 EVENTS (Entries & Exits)")
print("-"*80)
cursor.execute("SELECT visitor_id, event_type, timestamp, image_path FROM events ORDER BY timestamp")
events = cursor.fetchall()

if events:
    print(f"{'Visitor ID':<15} {'Event':<10} {'Timestamp':<20} {'Image Path':<50}")
    print("-"*80)
    for row in events:
        # Shorten image path for display
        img_path = row[3][-50:] if len(row[3]) > 50 else row[3]
        print(f"{row[0]:<15} {row[1]:<10} {row[2]:<20} {img_path:<50}")
else:
    print("No events recorded yet.")

print()
print(f"Total Events: {len(events)}")

# Count entries and exits
entries = sum(1 for e in events if e[1] == 'ENTRY')
exits = sum(1 for e in events if e[1] == 'EXIT')

print(f"  - Entries: {entries}")
print(f"  - Exits: {exits}")

print()
print("="*80)

# 3. SUMMARY
print("📈 SUMMARY")
print("-"*80)
print(f"Unique Visitors:  {len(visitors)}")
print(f"Total Entries:    {entries}")
print(f"Total Exits:      {exits}")
print(f"Currently Inside: {entries - exits}")
print("="*80)

conn.close()

print()
print("💡 TIP: Run 'python view_data.py' anytime to see updated data!")
print()
