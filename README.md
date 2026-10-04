Absolutely — here is the **full final README.md**, with the changes applied and the interview section removed.

````markdown
# Intelligent Face Tracking System

## Demo Results

The system was tested using a sample video containing a single person entering, leaving, and returning.

- **Unique Visitors:** 1
- **Total Events:** 3
- **Entries:** 2
- **Exits:** 1
- **Currently Inside:** 1
- **Returning Visitor:** VISITOR_001 recognized again
- **Similarity Score:** 0.65

The same person was recognized as `VISITOR_001` when returning instead of being registered as a new visitor. Therefore, the unique visitor count remained **1**.

---

## Problem Statement

Build an AI-driven visitor tracking system that can detect, track, recognize, and count unique visitors from a video or RTSP camera stream.

The system should automatically register new faces, recognize returning visitors, track their movement, and record entry and exit events with timestamps and face images.

---

## Main Objective

The main objective is to develop an intelligent face tracking system that:

- Detects faces from video input.
- Generates face embeddings.
- Automatically registers new visitors.
- Assigns a unique visitor ID.
- Recognizes returning visitors.
- Tracks visitors across frames.
- Detects entry and exit events.
- Stores visitor and event information in a database.
- Saves cropped face images.
- Maintains event logs.
- Counts unique visitors accurately.

---

## System Architecture

```text
                Video / RTSP Input
                        |
                        v
                Face Detection
                  (YOLO)
                        |
                        v
                Face Tracking
              (Tracker Module)
                        |
                        v
              Face Recognition
             (ArcFace Embedding)
                        |
             +----------+----------+
             |                     |
             v                     v
       New Visitor             Existing Visitor
             |                     |
             v                     v
        Generate ID            Recognize ID
        VISITOR_XXX                 |
             |                     |
             +----------+----------+
                        |
                        v
                Entry / Exit Logic
                        |
             +----------+----------+
             |                     |
             v                     v
          SQLite DB            events.log
             |                     |
             +----------+----------+
                        |
                        v
                Dashboard / Reports
````

---

## Tech Stack

### Programming Language

* Python

### AI / Computer Vision

* YOLO
* InsightFace
* ArcFace
* OpenCV

### Tracking

* Custom tracking logic

### Database

* SQLite

### Configuration

* JSON

### Logging

* Python logging
* `events.log`

### Input

* Video file for development/testing
* RTSP stream supported through configuration

---

## Project Structure

```text
intelligent-face-tracking/
│
├── main.py
├── database.py
├── recognizer.py
├── tracker.py
├── logger.py
├── dashboard.py
├── view_data.py
├── config.json
├── requirements.txt
├── README.md
│
├── output/
│   └── processed_video.mp4
│
├── logs/
│   └── events.log
│
├── data/
│   ├── faces/
│   └── database.db
│
└── screenshots/
```

---

## Configuration

The system uses `config.json` for configuration.

Example:

```json
{
    "input_source": "sample.mp4",
    "rtsp_url": "rtsp://username:password@camera_ip:port/stream",
    "detection_interval": 5,
    "similarity_threshold": 0.5
}
```

### Configuration Parameters

* `input_source` – Video file used for processing.
* `rtsp_url` – RTSP camera stream URL.
* `detection_interval` – Number of frames skipped between detection cycles.
* `similarity_threshold` – Threshold used for face recognition.

The configuration allows the system to be adjusted without modifying the main source code.

---

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/VikashiniSri27/intelligent-face-tracking.git
```

### 2. Open the Project

```bash
cd intelligent-face-tracking
```

### 3. Create a Virtual Environment

```bash
python -m venv venv
```

### 4. Activate the Virtual Environment

Windows:

```bash
venv\Scripts\activate
```

### 5. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Running the System

Run the main program:

```bash
python main.py
```

The system processes the input video and performs:

1. Face detection
2. Face tracking
3. Face embedding generation
4. Face recognition
5. Visitor registration
6. Entry/exit detection
7. Database storage
8. Event logging

The processed video is saved in the output directory.

---

## System Output

### Event Log

The system maintains an `events.log` file containing important system events.

Example:

```text
ENTRY VISITOR_001 2026-10-03 01:22:24
TRACKING_STARTED VISITOR_001
TRACKING_LOST VISITOR_001
EXIT VISITOR_001 2026-10-03 01:22:57
RECOGNIZED VISITOR_001 similarity=0.65
ENTRY VISITOR_001 2026-10-03 01:23:02
```

The log records events such as:

* Face detection
* Embedding generation
* Visitor registration
* Recognition
* Tracking
* Entry
* Exit

---

## Database

The system uses SQLite to store visitor and event information.

### Visitors Table

Example:

```text
visitor_id     first_seen             last_seen              total_visits
VISITOR_001    2026-10-03 01:22:24    2026-10-03 01:23:02    1
```

### Events Table

Example:

```text
visitor_id     event_type    timestamp
VISITOR_001    ENTRY         2026-10-03 01:22:24
VISITOR_001    EXIT          2026-10-03 01:22:57
VISITOR_001    ENTRY         2026-10-03 01:23:02
```

The database provides a persistent record of visitors and their events.

---

## How the System Works

### 1. Face Detection

YOLO detects faces in the input video.

The detected face regions are passed to the next stage.

### 2. Face Embedding

InsightFace / ArcFace generates an embedding for each detected face.

The embedding represents the facial characteristics of the visitor.

### 3. New Visitor Registration

If the generated embedding does not match any stored visitor embedding, the system registers the person as a new visitor.

Example:

```text
VISITOR_001
```

A cropped face image and visitor information are stored.

### 4. Returning Visitor Recognition

When a previously registered person appears again, their face embedding is compared with stored embeddings.

If the similarity score is above the configured threshold, the existing visitor ID is used.

Example:

```text
Similarity = 0.65
Visitor = VISITOR_001
```

The system does not create another visitor.

Therefore:

```text
Unique Visitors = 1
```

even though the person entered twice.

### 5. Tracking

The detected visitor is tracked across video frames.

Tracking reduces the need to perform full face recognition on every frame.

### 6. Entry Detection

When a visitor enters the monitored area, an entry event is created.

Example:

```text
ENTRY VISITOR_001
```

### 7. Exit Detection

When the tracked visitor leaves the monitored area, an exit event is generated.

Example:

```text
EXIT VISITOR_001
```

### 8. Database Storage

Visitor information and event information are stored in SQLite.

### 9. Event Logging

Important operations are written to `events.log` for debugging, monitoring, and verification.

---

## Demo Sequence

The final demonstration contains the following sequence:

```text
01:22:24
VISITOR_001 enters
        |
        v
New visitor registered
        |
        v
Tracking started
        |
        v
01:22:57
VISITOR_001 exits
        |
        v
01:23:02
VISITOR_001 returns
        |
        v
Existing visitor recognized
Similarity = 0.65
        |
        v
VISITOR_001 enters again
```

Final result:

```text
Unique Visitors : 1
Total Entries   : 2
Total Exits     : 1
Currently Inside: 1
Total Events    : 3
```

The important point is that the returning visitor is recognized as the same person, so the unique visitor count remains **1**.

---

## Dashboard

The project also includes a dashboard for displaying visitor statistics.

The dashboard provides:

* Unique visitors
* Total entries
* Total exits
* Currently inside
* Recent events
* Visitor information
* First seen time
* Last seen time
* Number of visits

Example:

```text
-----------------------------------------
        INTELLIGENT FACE TRACKING
-----------------------------------------

Unique Visitors       : 1
Total Entries         : 2
Total Exits           : 1
Currently Inside      : 1

Recent Events
-----------------------------------------
VISITOR_001   ENTRY    01:22:24
VISITOR_001   EXIT     01:22:57
VISITOR_001   ENTRY    01:23:02
```

---

## Sample Output

### Unique Visitor Count

```text
Total Unique Visitors: 1
```

### Event Summary

```text
Total Events: 3
- Entries: 2
- Exits: 1
```

### Current Status

```text
Currently Inside: 1
```

---

## Assumptions

The following assumptions are used:

* The camera provides a sufficiently clear view of the face.
* The face is visible for enough frames to generate an embedding.
* Lighting conditions are reasonably suitable for face detection.
* The configured similarity threshold is appropriate for the environment.
* A visitor leaving and returning is recognized using their stored face embedding.
* The system uses a video file during development and testing.
* RTSP input can be configured using `config.json`.

---

## Compute Requirements

The system is designed to run on a computer capable of running Python-based computer vision models.

### Recommended

* Python 3.10+
* 8 GB RAM or higher
* Modern multi-core CPU
* NVIDIA GPU recommended for faster inference

### CPU

The system can run on CPU, but processing may be slower depending on:

* Video resolution
* Number of faces
* Detection frequency
* Model size

### GPU

A CUDA-compatible NVIDIA GPU can improve:

* YOLO inference speed
* Face embedding generation
* Overall processing performance

---

## Testing

The system was tested using a sample video.

The final test verified:

* Face detection
* New visitor registration
* Face embedding generation
* Visitor ID assignment
* Face tracking
* Entry detection
* Exit detection
* Returning visitor recognition
* Unique visitor counting
* SQLite database storage
* Event logging
* Dashboard statistics

### Test Result

```text
Unique Visitors : 1
Entries         : 2
Exits           : 1
Currently Inside: 1
Total Events    : 3
```

The same visitor was recognized after returning instead of being registered again.

---

## Optimization

The system uses configurable detection intervals to reduce unnecessary face detection operations.

For example:

```json
"detection_interval": 5
```

This allows the system to skip some frames between detection cycles.

The approach helps reduce computational requirements while maintaining tracking between detection operations.

---

## Troubleshooting

### Camera / Video Not Opening

Check the configured input source:

```json
{
    "input_source": "sample.mp4"
}
```

For an RTSP camera, verify the RTSP URL and camera connectivity.

### Face Not Recognized

Possible reasons:

* Poor lighting
* Face is too small
* Face angle is too large
* Low-quality input
* Similarity threshold is too high

The threshold can be adjusted in `config.json`.

### Slow Processing

Possible improvements:

* Increase `detection_interval`
* Reduce input video resolution
* Use GPU acceleration
* Use a smaller detection model

### Incorrect Recognition

The similarity threshold can be adjusted according to the environment.

A lower threshold may increase matching but can also increase false matches.

A higher threshold makes matching stricter.

---

## Development Workflow

AI-assisted development was used during the implementation of this project.

The development process involved:

1. Breaking the requirements into modules.
2. Designing the project architecture.
3. Creating individual Python modules.
4. Implementing face detection.
5. Implementing face embedding generation.
6. Implementing visitor registration.
7. Implementing recognition.
8. Implementing tracking.
9. Implementing entry/exit logging.
10. Implementing SQLite database storage.
11. Testing using sample video.
12. Debugging and improving the system.
13. Creating dashboard and database reporting.
14. Validating the final output against the hackathon requirements.

AI-generated code was reviewed, modified, tested, and integrated according to the project requirements.

---

## Demo Video

[Watch Demo on YouTube](https://youtu.be/XUlbgz139eI)

The demonstration shows:

* Project structure
* Main processing pipeline
* New visitor registration
* Visitor tracking
* Exit detection
* Returning visitor recognition
* Database output
* Event logs
* Dashboard statistics

---

## Demo Analysis

The final demonstration verifies the complete visitor lifecycle.

### Event 1 — New Visitor Entry

```text
VISITOR_001
ENTRY
01:22:24
```

The face is detected and a new visitor ID is generated.

### Event 2 — Visitor Exit

```text
VISITOR_001
EXIT
01:22:57
```

The system detects that the visitor has left the monitored area.

### Event 3 — Returning Visitor

```text
VISITOR_001
ENTRY
01:23:02
```

The visitor appears again.

The system compares the new face embedding with the stored embedding and recognizes the visitor as:

```text
VISITOR_001
Similarity = 0.65
```

No new visitor is created.

Therefore:

```text
Unique Visitors = 1
```

while:

```text
Total Entries = 2
Total Exits = 1
```

This demonstrates that the system distinguishes between **unique visitors** and **multiple visits by the same visitor**.

---

## Requirement Coverage

| Requirement              | Implementation        |
| ------------------------ | --------------------- |
| Face Detection           | YOLO                  |
| Face Recognition         | InsightFace / ArcFace |
| Face Embeddings          | ArcFace               |
| New Visitor Registration | Automatic             |
| Unique Visitor ID        | `VISITOR_XXX`         |
| Visitor Recognition      | Embedding similarity  |
| Tracking                 | Tracker module        |
| Entry Detection          | Implemented           |
| Exit Detection           | Implemented           |
| Unique Visitor Count     | SQLite / logs         |
| Event Logging            | `events.log`          |
| Face Image Storage       | Local storage         |
| Database                 | SQLite                |
| Configuration            | `config.json`         |
| Video Input              | Sample video          |
| RTSP Support             | Configuration         |
| Dashboard                | `dashboard.py`        |
| Database Reporting       | `view_data.py`        |

---

## Future Improvements

Possible future improvements include:

* Multi-camera support
* Improved multi-person tracking
* GPU acceleration
* Advanced tracking algorithms such as ByteTrack or DeepSORT
* Cloud database support
* Real-time RTSP deployment
* Better entry/exit zone configuration
* Improved dashboard visualization
* Authentication and access control
* Large-scale visitor analytics

---

## License

This project was developed as part of a hackathon project.

---

## Acknowledgements

* YOLO
* InsightFace
* ArcFace
* OpenCV
* SQLite
* Python

---

## Hackathon

This project is a part of a hackathon run by [https://katomaran.com](https://katomaran.com)

---

## Contact

**Vikashini Sri Matheswaran**

GitHub:
[https://github.com/VikashiniSri27](https://github.com/VikashiniSri27)

LinkedIn:
[https://linkedin.com/in/vikashinisrimatheswaran](https://linkedin.com/in/vikashinisrimatheswaran)

```

**This is the version I recommend submitting.**
```
