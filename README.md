# Intelligent Face Tracking System

An AI-based visitor tracking system that detects, recognizes, tracks faces in real-time and accurately counts unique visitors from video/camera streams.

## ✅ **DEMO RESULTS - PROOF OF RECOGNITION**

**Successfully tested:** Same person entering → exiting → re-entering is recognized as ONE unique visitor!

### 🎯 Demo Sequence
```
01:22:24 → Person enters     → VISITOR_001 registered
01:22:57 → Person exits      → EXIT logged
01:23:02 → Person returns    → VISITOR_001 recognized (confidence: 0.58)
                              → NOT counted as VISITOR_002!
```

### 📊 Final Statistics
- **Unique Visitors**: 1 ✅
- **Total Events**: 3 (2 entries + 1 exit)
- **Recognition**: ✅ Same person correctly identified on return
- **No Duplicates**: ✅ Count stayed at 1 (not 2)

**Key Evidence**: The system recognized the returning person with embedding similarity match, proving the face recognition and unique counting works correctly!

[See detailed demo analysis →](#demo-analysis)

## 📋 Problem Statement

This system addresses the challenge of accurately counting unique visitors in a video stream by:

1. **Detecting faces** using YOLO
2. **Recognizing faces** using InsightFace embeddings
3. **Automatically registering** new visitors with unique IDs
4. **Tracking faces** across frames
5. **Logging entry/exit events** with timestamps and images
6. **Counting unique visitors** without duplicate counting

### Key Challenge
When the same person appears multiple times, the system must recognize them as the same visitor, not create a new entry.

**Example:**
- Person A enters → VISITOR_001
- Person B enters → VISITOR_002  
- Person A leaves
- Person A returns → Still VISITOR_001 ✓ (not VISITOR_003 ✗)
- **Unique Count: 2**

## 🎯 Main Objective

Build an AI system that:
- Detects faces in real-time video/RTSP streams
- Recognizes whether faces are new or known
- Automatically registers new faces with unique IDs
- Tracks individuals while in frame
- Logs every entry/exit with timestamped images
- Maintains accurate unique visitor count

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────┐
│                   VIDEO / RTSP CAMERA                   │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
            ┌────────────────┐
            │ FACE DETECTION │
            │     (YOLO)     │
            └────────┬───────┘
                     │
                     ▼
            ┌────────────────┐
            │  FACE CROPPING │
            └────────┬───────┘
                     │
                     ▼
            ┌────────────────┐
            │ FACE EMBEDDING │
            │  (InsightFace) │
            └────────┬───────┘
                     │
                     ▼
            ┌────────────────┐
            │ DATABASE SEARCH│
            │  (Similarity)  │
            └────────┬───────┘
                     │
        ┌────────────┴────────────┐
        ▼                         ▼
   ┌─────────┐              ┌──────────┐
   │NEW FACE │              │KNOWN FACE│
   │         │              │          │
   │Register │              │Recognize │
   │  NEW ID │              │ EXIST ID │
   └────┬────┘              └─────┬────┘
        │                         │
        └────────────┬────────────┘
                     │
                     ▼
            ┌────────────────┐
            │    TRACKING    │
            │ (CentroidTrack)│
            └────────┬───────┘
                     │
                     ▼
            ┌────────────────┐
            │  ENTRY / EXIT  │
            │     EVENTS     │
            └────────┬───────┘
                     │
        ┌────────────┼────────────┐
        ▼            ▼            ▼
   ┌────────┐  ┌─────────┐  ┌──────────┐
   │ IMAGES │  │DATABASE │  │events.log│
   │ (logs/)│  │(SQLite) │  │          │
   └────────┘  └─────────┘  └──────────┘
                     │
                     ▼
            ┌────────────────┐
            │ UNIQUE VISITOR │
            │     COUNT      │
            └────────────────┘
```

## 🔧 Technology Stack

| Component | Technology |
|-----------|-----------|
| Programming Language | Python 3.8+ |
| Face Detection | YOLOv8 (Ultralytics) |
| Face Recognition | InsightFace (ArcFace) |
| Tracking | Centroid Tracker |
| Database | SQLite |
| Configuration | JSON |
| Image Processing | OpenCV |
| Embeddings | NumPy, scikit-learn |

## 📁 Project Structure

```
face_tracker/
│
├── main.py                 # Main application entry point
├── database.py             # SQLite database operations
├── recognizer.py           # InsightFace embedding & recognition
├── tracker.py              # Centroid-based object tracking
├── logger.py               # Event logging system
│
├── config.json             # System configuration
├── requirements.txt        # Python dependencies
├── README.md              # This file
│
├── logs/                  # Stored face images
│   ├── entries/           # Entry event images
│   │   └── YYYY-MM-DD/
│   └── exits/             # Exit event images
│       └── YYYY-MM-DD/
│
├── database/              # SQLite database
│   └── visitors.db        # Visitor & event data
│
├── output/                # Processed videos
│   └── processed_video.mp4
│
└── events.log             # System event log
```

## ⚙️ Configuration

Edit `config.json` to customize system behavior:

```json
{
    "video_source": "sample.mp4",
    "rtsp_url": "",
    "detection_skip_frames": 5,
    "similarity_threshold": 0.5,
    "confidence_threshold": 0.5,
    "min_face_size": 30,
    "max_disappear_frames": 30,
    "database_path": "database/visitors.db",
    "log_path": "events.log",
    "entries_folder": "logs/entries",
    "exits_folder": "logs/exits"
}
```

### Configuration Parameters

| Parameter | Description | Default |
|-----------|-------------|---------|
| `video_source` | Path to video file | `sample.mp4` |
| `rtsp_url` | RTSP camera URL (overrides video_source if set) | `""` |
| `detection_skip_frames` | Process every Nth frame (reduces computation) | `5` |
| `similarity_threshold` | Minimum similarity (0-1) to match faces | `0.5` |
| `confidence_threshold` | Minimum detection confidence | `0.5` |
| `min_face_size` | Minimum face size in pixels | `30` |
| `max_disappear_frames` | Frames before considering exit | `30` |

## 🚀 Setup Instructions

### Prerequisites
- Python 3.8 or higher
- pip package manager
- (Optional) CUDA-capable GPU for faster processing

### Installation Steps

1. **Clone or download this project**
```bash
cd face_tracker
```

2. **Create virtual environment (recommended)**
```bash
python -m venv venv

# On Windows
venv\Scripts\activate

# On Linux/Mac
source venv/bin/activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Download InsightFace models**

The first run will automatically download the InsightFace model (~250MB). Ensure you have internet connection.

5. **Prepare your video**

Place your video file in the project directory and update `config.json`:
```json
{
    "video_source": "your_video.mp4"
}
```

Or use RTSP camera:
```json
{
    "rtsp_url": "rtsp://your_camera_ip:554/stream"
}
```

### Running the System

```bash
python main.py
```

The system will:
- Process the video frame by frame
- Display annotated video with bounding boxes and IDs
- Save processed video to `output/processed_video.mp4`
- Store face images in `logs/entries/` and `logs/exits/`
- Log all events to `events.log`
- Store visitor data in `database/visitors.db`

**To stop**: Press `q` in the video window or `Ctrl+C` in terminal

## 📊 System Output

### 1. Processed Video
Located in `output/processed_video.mp4`
- Bounding boxes around detected faces
- Visitor IDs displayed above each face
- Real-time unique visitor count

### 2. Face Images
```
logs/
├── entries/
│   └── 2026-10-03/
│       ├── VISITOR_001_20261003_101522_123456.jpg
│       └── VISITOR_002_20261003_101530_654321.jpg
└── exits/
    └── 2026-10-03/
        ├── VISITOR_001_20261003_101745_789012.jpg
        └── VISITOR_002_20261003_101800_345678.jpg
```

### 3. Events Log (events.log)
```
[2026-10-03 10:15:22] INTELLIGENT FACE TRACKING SYSTEM STARTED
[2026-10-03 10:15:22] Video source: sample.mp4
[2026-10-03 10:15:22] [Frame 5] Face detected
[2026-10-03 10:15:22] New face registered: VISITOR_001
[2026-10-03 10:15:22] Face embedding generated for VISITOR_001
[2026-10-03 10:15:22] ENTRY - VISITOR_001
[2026-10-03 10:15:22] Tracking started: VISITOR_001 (Track ID: 0)
[2026-10-03 10:15:30] [Frame 50] Face detected
[2026-10-03 10:15:30] New face registered: VISITOR_002
[2026-10-03 10:15:30] ENTRY - VISITOR_002
[2026-10-03 10:17:45] EXIT - VISITOR_001
[2026-10-03 10:17:45] Tracking lost: VISITOR_001 (Track ID: 0)
```

### 4. Database (SQLite)

**visitors table:**
| visitor_id | first_seen | last_seen | total_visits | embedding |
|------------|-----------|-----------|--------------|-----------|
| VISITOR_001 | 2026-10-03 10:15:22 | 2026-10-03 10:17:45 | 1 | [binary] |
| VISITOR_002 | 2026-10-03 10:15:30 | 2026-10-03 10:18:00 | 1 | [binary] |

**events table:**
| event_id | visitor_id | event_type | timestamp | image_path |
|----------|-----------|-----------|-----------|------------|
| 1 | VISITOR_001 | ENTRY | 2026-10-03 10:15:22 | logs/entries/... |
| 2 | VISITOR_002 | ENTRY | 2026-10-03 10:15:30 | logs/entries/... |
| 3 | VISITOR_001 | EXIT | 2026-10-03 10:17:45 | logs/exits/... |

### 5. Console Output
```
============================================================
INTELLIGENT FACE TRACKING SYSTEM
============================================================

Video properties: 1920x1080 @ 30 FPS
[2026-10-03 10:15:22] Face detected
[2026-10-03 10:15:22] New face registered: VISITOR_001
...

============================================================
FINAL STATISTICS
============================================================
Total Unique Visitors: 2
Total Events Logged: 4
Total Entries: 2
Total Exits: 2
============================================================
```

## 🧠 How It Works

### 1. Face Detection (YOLO)
- Processes frames at configurable intervals (`detection_skip_frames`)
- Detects faces with bounding boxes
- Filters by confidence threshold

### 2. Face Recognition (InsightFace)
- Crops detected face from frame
- Generates 512-dimensional embedding vector
- Compares with stored embeddings using cosine similarity

### 3. Registration vs Recognition Workflow

**For every detected face:**

1. **Generate Embedding** → Create 512-dimensional vector from current face
2. **Database Search** → Compare against all stored visitor embeddings
3. **Decision**:
   - **Similarity ≥ threshold** → Recognize as existing visitor
   - **Similarity < threshold** → Register as new visitor

```python
# Pseudo-code
face_detected = yolo.detect(frame)
current_embedding = insightface.generate_embedding(face_detected)

for stored_visitor in database:
    similarity = cosine_similarity(current_embedding, stored_visitor.embedding)
    if similarity >= threshold:
        return stored_visitor.id  # Recognized!

# No match found - new visitor
new_id = create_new_visitor()
database.save(new_id, current_embedding)
return new_id
```

**Important**: An embedding is generated for **every** face appearance. This allows the system to compare the current observation against the stored identity embeddings, enabling recognition of returning visitors.

### 4. Tracking
- Maintains identity across frames using centroid tracking
- Maps tracking IDs to visitor IDs
- Handles temporary occlusions

### 5. Entry/Exit Detection
- **Entry**: First time a track ID appears
- **Exit**: Track ID disappears for more than `max_disappear_frames`

### 6. Unique Counting
- Each unique face receives one visitor ID
- Same person returning is recognized (not counted again)
- Count = Number of unique visitor IDs in database

## 🔍 Key Assumptions

1. **Same Person Recognition**: A face is considered the same person when the embedding similarity exceeds `similarity_threshold` (default: 0.5)

2. **Exit Detection**: A person is considered to have exited when they disappear from frame for `max_disappear_frames` consecutive frames (default: 30)

3. **Face Quality**: System assumes reasonably clear face images (minimum 30x30 pixels)

4. **Single Face per Person**: Each person has one primary face representation

5. **Lighting Conditions**: Best performance in consistent lighting; extreme lighting changes may affect recognition

6. **Camera Angle**: Front or near-front facing angles work best

7. **Video Format**: System supports standard video formats (MP4, AVI) and RTSP streams

## 💻 Compute Requirements

### Minimum Requirements
- **CPU**: Intel Core i5 or equivalent
- **RAM**: 8GB
- **Storage**: 2GB free space
- **Processing Speed**: ~5-10 FPS on CPU

### Recommended Requirements
- **CPU**: Intel Core i7 or equivalent
- **GPU**: NVIDIA GPU with CUDA support
- **RAM**: 16GB
- **Storage**: 5GB free space
- **Processing Speed**: ~30+ FPS with GPU

### GPU Acceleration

To enable GPU acceleration, modify `recognizer.py`:

```python
self.app = FaceAnalysis(
    name='buffalo_l',
    providers=['CUDAExecutionProvider', 'CPUExecutionProvider']
)
```

And install CUDA-enabled dependencies:
```bash
pip install onnxruntime-gpu
```

## 🧪 Testing with Sample Data

### Test with Sample Video

1. Place `sample.mp4` in project directory
2. Update `config.json`:
   ```json
   {"video_source": "sample.mp4"}
   ```
3. Run: `python main.py`

### Test with RTSP Camera

1. Update `config.json`:
   ```json
   {"rtsp_url": "rtsp://192.168.1.100:554/stream"}
   ```
2. Run: `python main.py`

### Test Individual Modules

```bash
# Test database
python database.py

# Test logger
python logger.py

# Test tracker
python tracker.py
```

## 📈 Performance Optimization

1. **Reduce Detection Frequency**: Increase `detection_skip_frames` (e.g., 10)
2. **Lower Resolution**: Resize frames before processing
3. **GPU Acceleration**: Enable CUDA support
4. **Adjust Thresholds**: Tune `confidence_threshold` and `similarity_threshold`

## 🐛 Troubleshooting

### Issue: "Failed to open video source"
- Check video file path in `config.json`
- Ensure video file exists and is readable
- For RTSP: Verify camera URL and network connectivity

### Issue: "InsightFace model download fails"
- Ensure internet connection
- Check firewall settings
- Manually download model from InsightFace GitHub

### Issue: "Low FPS / Slow processing"
- Increase `detection_skip_frames`
- Enable GPU acceleration
- Reduce video resolution

### Issue: "Same person counted twice"
- Lower `similarity_threshold` (e.g., 0.4)
- Check face image quality
- Ensure consistent lighting

### Issue: "Different people recognized as same"
- Increase `similarity_threshold` (e.g., 0.6)
- Improve face detection quality

## 📝 Development Workflow

This project was developed using AI-assisted coding with the following workflow:

1. **Problem Analysis**: Understanding hackathon requirements
2. **Architecture Design**: Modular system design
3. **Module Implementation**: Step-by-step implementation
   - Database layer
   - Logging system
   - Face recognition
   - Tracking system
   - Main application
4. **Testing**: Individual module and integration testing
5. **Documentation**: Comprehensive README and code comments


## 🎥 Demo Video
[![Demo Video](https://img.youtube.com/vi/XUlbgz139eI/0.jpg)](https://youtu.be/XUlbgz139eI)
▶️ **Watch Demo**: https://youtu.be/XUlbgz139eI


## 📄 License

This project is created for educational purposes as part of a hackathon.

## 🙏 Acknowledgments

- **YOLO**: Ultralytics YOLOv8
- **InsightFace**: Face recognition library
- **OpenCV**: Computer vision operations

---

## 📊 Demo Analysis

### Actual Test Results

Our demo video (27.7 seconds, 830 frames) proves the system correctly handles the re-identification challenge:

#### Event Timeline

| Time | Event | Visitor ID | Action Taken |
|------|-------|-----------|--------------|
| 01:22:24 | Face detected (Frame 5) | NEW | Registration triggered |
| 01:22:24 | New face registered | VISITOR_001 | Embedding generated & stored |
| 01:22:24 | Entry event | VISITOR_001 | Entry logged to database |
| 01:22:24 | Tracking started | Track ID: 0 | Centroid tracker activated |
| 01:22:57 | Exit event | VISITOR_001 | Person left frame completely |
| 01:22:57 | Tracking lost | Track ID: 0 | Tracker deactivated |
| 01:23:02 | Face detected (Frame 575) | RETURNING | Face appeared again |
| 01:23:02 | **Recognized visitor** | **VISITOR_001** | **Similarity: 0.58 (matched!)** |
| 01:23:02 | Re-entry event | VISITOR_001 | Second entry logged |
| 01:23:02 | Tracking restarted | Track ID: 2 | New track, same visitor ID |

#### Why This Proves Recognition Works

**The Critical Test:**
```
First appearance  → VISITOR_001 created
Person leaves     → EXIT logged
Person returns    → System must decide: New person or same person?
Result            → VISITOR_001 recognized (NOT VISITOR_002)
```

**Evidence:**
1. ✅ Embedding generated on re-entry (Frame 575)
2. ✅ Compared against stored VISITOR_001 embedding
3. ✅ Similarity score: 0.58 (above threshold of 0.5)
4. ✅ Recognized as existing visitor
5. ✅ No new visitor ID created
6. ✅ Unique count remains: 1

### Database Proof

**visitors table:**
```
Visitor ID      First Seen           Last Seen            Visits
VISITOR_001     2026-10-03 01:22:24  2026-10-03 01:22:24  1

Total Unique Visitors: 1
```

**events table:**
```
Visitor ID      Event      Timestamp            Image Path
VISITOR_001     ENTRY      2026-10-03 01:22:24  logs/entries/2026-10-03/VISITOR_001_*.jpg
VISITOR_001     EXIT       2026-10-03 01:22:57  logs/exits/2026-10-03/VISITOR_001_*.jpg
VISITOR_001     ENTRY      2026-10-03 01:23:02  logs/entries/2026-10-03/VISITOR_001_*.jpg

Total Events: 3 (2 entries + 1 exit)
```

### What Makes This Demo Strong

| Requirement | Implementation | Evidence |
|------------|----------------|----------|
| Face Detection | YOLO detects faces | ✅ 380+ frames with face detected |
| New Face Registration | Auto-create visitor ID | ✅ VISITOR_001 created at 01:22:24 |
| Embedding Generation | InsightFace creates vector | ✅ Embedding generated twice (registration + recognition) |
| Face Recognition | Compare embeddings | ✅ Similarity: 0.58 matched stored embedding |
| No Duplicate Counting | Same person = same ID | ✅ Count stayed at 1, not 2 |
| Entry Logging | Log with timestamp + image | ✅ 2 entry events logged |
| Exit Logging | Log when leaving frame | ✅ 1 exit event logged |
| Tracking | Track across frames | ✅ Tracking IDs: 0 and 2 mapped to VISITOR_001 |
| Database Storage | SQLite persistence | ✅ All data in visitors.db |
| Event Logging | Text log file | ✅ All events in events.log |
| Unique Counting | Count distinct people | ✅ Final count: 1 unique visitor |

### Interview Explanation

**Q: "Why does your log show 'Face embedding generated' twice for the same visitor?"**

**A:** "When a face is detected, I generate its embedding from the current frame. For a new face, I register and store its identity in the database. When the same face appears again later, I generate a fresh embedding from the new observation and compare it with all stored embeddings using cosine similarity. Since the similarity score (0.58) passed our threshold (0.5), the system recognized it as VISITOR_001 instead of creating a new visitor ID. This is how the system achieves re-identification without duplicate counting."

---

**This project is a part of a hackathon run by https://katomaran.com**

## 📧 Contact

For questions or issues, please open an issue in the repository.

---

*Built with ❤️ using AI-assisted development*
