# Intelligent Face Tracking System

An AI-based visitor tracking system that detects, recognizes, tracks faces in real time, and accurately counts unique visitors from video/camera streams.

## ✅ Demo Results — Proof of Recognition

The system was successfully tested with the same person entering, exiting, and re-entering.

### Demo Sequence

```text
01:22:24 → Person enters     → VISITOR_001 registered
01:22:57 → Person exits      → EXIT logged
01:23:02 → Person returns    → VISITOR_001 recognized (similarity: 0.58)
                              → NOT counted as VISITOR_002
```

### Final Statistics

* **Unique Visitors:** 1
* **Total Events:** 3
* **Total Entries:** 2
* **Total Exits:** 1
* **Recognition:** Same person correctly identified on return
* **No Duplicate Counting:** Unique visitor count remained 1

The returning visitor was matched with the stored face embedding using cosine similarity, demonstrating re-identification and unique visitor counting.

---

## 📋 Problem Statement

This system addresses the challenge of accurately counting unique visitors in a video stream by:

1. Detecting faces using YOLO
2. Recognizing faces using InsightFace embeddings
3. Automatically registering new visitors with unique IDs
4. Tracking faces across frames
5. Logging entry/exit events with timestamps and images
6. Counting unique visitors without duplicate counting

### Key Challenge

When the same person appears multiple times, the system must recognize them as the same visitor instead of creating a new visitor ID.

**Example:**

```text
Person A enters → VISITOR_001
Person B enters → VISITOR_002
Person A leaves
Person A returns → VISITOR_001
Unique Count → 2
```

---

## 🎯 Main Objective

Build an AI system that:

* Detects faces in video/RTSP streams
* Recognizes whether faces are new or known
* Automatically registers new faces with unique IDs
* Tracks individuals while they are in frame
* Logs every entry/exit with timestamped images
* Maintains an accurate unique visitor count

---

## 🏗️ System Architecture

```text
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
   │ Register│              │ Recognize│
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

---

## 🔧 Technology Stack

| Component            | Technology            |
| -------------------- | --------------------- |
| Programming Language | Python 3.8+           |
| Face Detection       | YOLOv8 (Ultralytics)  |
| Face Recognition     | InsightFace (ArcFace) |
| Tracking             | Centroid Tracker      |
| Database             | SQLite                |
| Configuration        | JSON                  |
| Image Processing     | OpenCV                |
| Embeddings           | NumPy, scikit-learn   |

---

## 📁 Project Structure

```text
face_tracker/
│
├── main.py                 # Main application
├── database.py             # SQLite database operations
├── recognizer.py           # InsightFace recognition
├── tracker.py              # Centroid-based tracking
├── logger.py               # Event logging
├── dashboard.py            # Visitor statistics dashboard
├── view_data.py            # Database/event summary
│
├── config.json             # System configuration
├── requirements.txt        # Python dependencies
├── README.md               # Project documentation
│
├── logs/
│   ├── entries/            # Entry event images
│   │   └── YYYY-MM-DD/
│   └── exits/              # Exit event images
│       └── YYYY-MM-DD/
│
├── database/
│   └── visitors.db         # Visitor and event data
│
├── output/
│   └── processed_video.mp4 # Processed video
│
└── events.log              # System event log
```

---

## ⚙️ Configuration

The system behavior can be customized using `config.json`.

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

| Parameter               | Description                          | Default      |
| ----------------------- | ------------------------------------ | ------------ |
| `video_source`          | Path to video file                   | `sample.mp4` |
| `rtsp_url`              | RTSP camera URL                      | `""`         |
| `detection_skip_frames` | Process every Nth frame              | `5`          |
| `similarity_threshold`  | Minimum similarity for face matching | `0.5`        |
| `confidence_threshold`  | Minimum YOLO confidence              | `0.5`        |
| `min_face_size`         | Minimum face size in pixels          | `30`         |
| `max_disappear_frames`  | Frames before considering exit       | `30`         |

---

## 🚀 Setup Instructions

### Prerequisites

* Python 3.8 or higher
* pip
* Optional NVIDIA CUDA-capable GPU

### 1. Clone or Download the Project

```bash
cd face_tracker
```

### 2. Create a Virtual Environment

**Windows:**

```bash
python -m venv venv
venv\Scripts\activate
```

**Linux/Mac:**

```bash
python -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. InsightFace Model

On the first run, InsightFace downloads the required model automatically.

Internet access is required for the initial model download.

### 5. Prepare Video

Place the video file in the project directory and configure:

```json
{
    "video_source": "sample.mp4"
}
```

### RTSP Camera

For an RTSP camera:

```json
{
    "rtsp_url": "rtsp://your_camera_ip:554/stream"
}
```

### 6. Run the System

```bash
python main.py
```

The system will:

* Detect faces
* Generate face embeddings
* Recognize existing visitors
* Register new visitors
* Track visitors
* Log entry and exit events
* Save face images
* Store data in SQLite
* Save the processed video

---

## 📊 System Output

### 1. Processed Video

The processed video is saved at:

```text
output/processed_video.mp4
```

It contains:

* Face bounding boxes
* Visitor IDs
* Unique visitor count

### 2. Face Images

Entry and exit images are stored separately:

```text
logs/
├── entries/
│   └── YYYY-MM-DD/
│       └── VISITOR_001_*.jpg
│
└── exits/
    └── YYYY-MM-DD/
        └── VISITOR_001_*.jpg
```

### 3. Event Log

The mandatory `events.log` records system activity.

Example:

```text
[time] INTELLIGENT FACE TRACKING SYSTEM STARTED
[time] Face detected
[time] New face registered: VISITOR_001
[time] Face embedding generated for VISITOR_001
[time] ENTRY - VISITOR_001
[time] Tracking started: VISITOR_001
[time] EXIT - VISITOR_001
[time] Tracking lost: VISITOR_001
[time] Face recognized: VISITOR_001
```

### 4. SQLite Database

The database stores visitor information and events.

#### Visitors Table

| visitor_id  | first_seen | last_seen   | total_visits |
| ----------- | ---------- | ----------- | ------------ |
| VISITOR_001 | Demo entry | Demo return | 1            |

#### Events Table

| event_id | visitor_id  | event_type | timestamp | image_path       |
| -------- | ----------- | ---------- | --------- | ---------------- |
| 1        | VISITOR_001 | ENTRY      | 01:22:24  | logs/entries/... |
| 2        | VISITOR_001 | EXIT       | 01:22:57  | logs/exits/...   |
| 3        | VISITOR_001 | ENTRY      | 01:23:02  | logs/entries/... |

### 5. Final Demo Statistics

```text
Unique Visitors: 1
Total Events: 3
Total Entries: 2
Total Exits: 1
Currently Inside: 1
```

---

## 🧠 How It Works

### 1. Face Detection — YOLO

YOLO detects faces from the input video.

* Frames are processed at configurable intervals.
* Face bounding boxes are generated.
* Low-confidence detections are filtered.

### 2. Face Recognition — InsightFace

For every detected face:

* The face is cropped.
* InsightFace generates a 512-dimensional embedding.
* The embedding is compared with stored visitor embeddings.

### 3. Registration vs Recognition

```text
              Face Detected
                    │
                    ▼
          Generate Embedding
                    │
                    ▼
       Compare with Database
                    │
                    ▼
          Similarity Check
             /          \
           YES           NO
            │             │
            ▼             ▼
      Existing ID     New Visitor
     VISITOR_001      VISITOR_002
```

If similarity is greater than or equal to the configured threshold, the existing visitor is recognized.

Otherwise, a new visitor ID is created.

### 4. Tracking

The Centroid Tracker:

* Maintains identity across frames
* Maps tracking IDs to visitor IDs
* Handles temporary disappearance

### 5. Entry and Exit Detection

* **Entry:** First appearance of a track
* **Exit:** Track disappears for more than `max_disappear_frames`

### 6. Unique Counting

Each unique visitor receives one visitor ID.

When the same person leaves and returns:

```text
VISITOR_001 enters
       ↓
VISITOR_001 exits
       ↓
VISITOR_001 returns
       ↓
VISITOR_001 recognized again
       ↓
Unique count remains 1
```

---

## 🔍 Key Assumptions

1. A face is considered the same person when embedding similarity exceeds the configured threshold.
2. The default similarity threshold is `0.5`.
3. A person is considered exited after disappearing for `30` consecutive frames by default.
4. Face images should be reasonably clear.
5. Minimum face size is configured as `30 × 30` pixels.
6. Consistent lighting provides better recognition performance.
7. Front or near-front camera angles work best.
8. MP4, AVI, and RTSP streams are supported.

---

## 💻 Compute Requirements

### Minimum

* **CPU:** Intel Core i5 or equivalent
* **RAM:** 8 GB
* **Storage:** 2 GB free space
* **Processing:** Approximately 5–10 FPS on CPU

### Recommended

* **CPU:** Intel Core i7 or equivalent
* **GPU:** NVIDIA GPU with CUDA support
* **RAM:** 16 GB
* **Storage:** 5 GB free space
* **Processing:** Approximately 30+ FPS with GPU

### GPU Acceleration

InsightFace can be configured to use CUDA:

```python
self.app = FaceAnalysis(
    name='buffalo_l',
    providers=['CUDAExecutionProvider', 'CPUExecutionProvider']
)
```

Install the GPU runtime:

```bash
pip install onnxruntime-gpu
```

---

## 🧪 Testing

### Sample Video

1. Place `sample.mp4` in the project directory.
2. Update `config.json`:

```json
{
    "video_source": "sample.mp4"
}
```

3. Run:

```bash
python main.py
```

### RTSP Camera

Configure:

```json
{
    "rtsp_url": "rtsp://192.168.1.100:554/stream"
}
```

Then run:

```bash
python main.py
```

### Individual Modules

```bash
python database.py
python logger.py
python tracker.py
```

---

## 📈 Performance Optimization

1. Increase `detection_skip_frames` to reduce detection frequency.
2. Resize frames to a lower resolution.
3. Enable GPU acceleration when available.
4. Tune `confidence_threshold`.
5. Tune `similarity_threshold` based on the camera environment.

---

## 🐛 Troubleshooting

### Failed to Open Video Source

* Check the video path in `config.json`.
* Make sure the video exists.
* Check that the video is readable.
* For RTSP, verify the camera URL and network connection.

### InsightFace Model Download Fails

* Check your internet connection.
* Check firewall settings.
* Retry the first run.

### Low FPS / Slow Processing

* Increase `detection_skip_frames`.
* Enable GPU acceleration.
* Reduce video resolution.

### Same Person Counted Twice

* Check face image quality.
* Ensure consistent lighting.
* Tune the similarity threshold.

### Different People Recognized as the Same

* Increase the similarity threshold.
* Improve face detection quality.
* Test with clearer face images.

---

## 📝 Development Workflow

This project was developed using AI-assisted coding.

### Development Process

1. **Problem Analysis**

   * Studied the hackathon requirements.
   * Identified face detection, recognition, tracking, and counting requirements.

2. **Architecture Design**

   * Designed a modular Python architecture.
   * Separated database, recognition, tracking, logging, and main processing.

3. **Module Implementation**

   * Database layer
   * Event logging
   * Face recognition
   * Centroid tracking
   * Main application
   * Dashboard and database viewer

4. **Testing**

   * Tested individual modules.
   * Tested complete video processing.
   * Tested visitor re-identification.

5. **Documentation**

   * Added setup instructions.
   * Added architecture and configuration details.
   * Added demo evidence and requirement coverage.

---

## 🎥 Demo Video

**Watch the demo:**

[https://youtu.be/XUlbgz139eI](https://youtu.be/XUlbgz139eI)

The demo demonstrates:

* New visitor registration
* Face embedding generation
* Entry logging
* Face tracking
* Exit detection
* Re-identification of a returning visitor
* No duplicate visitor creation
* SQLite database records
* Event logging
* Final unique visitor count

---

# 📊 Demo Analysis

## Actual Test Results

The demo video is approximately **27.7 seconds** and contains **830 frames**.

The main test demonstrates the system's ability to recognize the same visitor after they leave and return.

### Event Timeline

| Time     | Event               | Visitor ID  | Action                         |
| -------- | ------------------- | ----------- | ------------------------------ |
| 01:22:24 | Face detected       | NEW         | Registration triggered         |
| 01:22:24 | New face registered | VISITOR_001 | Embedding generated and stored |
| 01:22:24 | Entry event         | VISITOR_001 | Entry logged                   |
| 01:22:24 | Tracking started    | Track ID: 0 | Tracking activated             |
| 01:22:57 | Exit event          | VISITOR_001 | Person left frame              |
| 01:22:57 | Tracking lost       | Track ID: 0 | Tracking ended                 |
| 01:23:02 | Face detected       | RETURNING   | Face appeared again            |
| 01:23:02 | Recognized visitor  | VISITOR_001 | Similarity: 0.58               |
| 01:23:02 | Re-entry event      | VISITOR_001 | Second entry logged            |
| 01:23:02 | Tracking restarted  | Track ID: 2 | Same visitor ID                |

---

## Why This Proves Recognition Works

```text
First appearance
       ↓
VISITOR_001 created
       ↓
Person leaves
       ↓
EXIT logged
       ↓
Person returns
       ↓
New embedding generated
       ↓
Compared with stored embedding
       ↓
Similarity = 0.58
       ↓
VISITOR_001 recognized
       ↓
No new visitor ID
       ↓
Unique count remains 1
```

### Evidence

1. Embedding generated during the first registration.
2. The returning face generates a fresh embedding.
3. The new embedding is compared with the stored visitor embedding.
4. Similarity score is **0.58**.
5. Configured threshold is **0.5**.
6. The existing `VISITOR_001` is recognized.
7. No duplicate visitor ID is created.
8. Unique visitor count remains **1**.

---

## Database Proof

### Visitors

```text
Visitor ID
VISITOR_001

Total Unique Visitors: 1
```

### Events

```text
VISITOR_001  ENTRY  01:22:24
VISITOR_001  EXIT   01:22:57
VISITOR_001  ENTRY  01:23:02

Total Events: 3
Entries: 2
Exits: 1
```

---

## Requirement Coverage

| Requirement           | Implementation                    | Demo Evidence                            |
| --------------------- | --------------------------------- | ---------------------------------------- |
| Face Detection        | YOLO                              | Face detection in processed frames       |
| New Face Registration | Automatic visitor ID creation     | `VISITOR_001` registered                 |
| Embedding Generation  | InsightFace                       | Embeddings generated                     |
| Face Recognition      | Cosine similarity                 | Similarity 0.58 matched stored embedding |
| No Duplicate Counting | Same person keeps same visitor ID | Unique count remained 1                  |
| Entry Logging         | Timestamp + image                 | 2 entry events                           |
| Exit Logging          | Timestamp + image                 | 1 exit event                             |
| Tracking              | Centroid Tracker                  | Track IDs mapped to visitor ID           |
| Database Storage      | SQLite                            | Visitor/event data stored                |
| Event Logging         | `events.log`                      | System events recorded                   |
| Unique Counting       | Unique visitor IDs                | Final count: 1                           |

---

## 📄 License

This project is created for educational purposes as part of a hackathon.

## 🙏 Acknowledgments

* **YOLO:** Ultralytics YOLOv8
* **InsightFace:** Face recognition library
* **OpenCV:** Computer vision operations

---

**This project is a part of a hackathon run by [https://katomaran.com](https://katomaran.com)**

## 📧 Contact

For questions or issues, please open an issue in the repository.
