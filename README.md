# 🕵️ Investigation Support System

An AI-powered surveillance and investigation system that combines real-time object detection, multi-object tracking, face recognition, evidence capture, and persistent detection logging to assist in monitoring and investigation tasks.

---

## 🚀 Features

- 🎯 Real-time person detection using YOLOv8
- 👤 Face recognition for known individuals
- 🆔 Multi-object tracking with unique Track IDs
- 📸 Automatic evidence capture
- 🗃️ SQLite-based detection logging
- ⚡ GPU acceleration using CUDA
- 📈 Real-time FPS monitoring
- 👥 Live person counting

---

## 🛠️ Tech Stack

- Python
- OpenCV
- Ultralytics YOLOv8
- Face Recognition (dlib)
- SQLite
- PyTorch (CUDA)
- NumPy

---

## 📂 Project Structure


Investigation-Support-System/

├── app.py
├── database.py
├── detections/
├── known_faces/
├── models/
├── detections.db
├── requirements.txt
├── requirements-gpu.txt
└── README.md


---

## ⚙️ Installation

Clone the repository

git clone <https://github.com/commit-msuyog/Investigation-Support-System>
cd Investigation-Support-System


Install dependencies


pip install -r requirements.txt


Install GPU-enabled PyTorch (Optional)

pip install torch torchvision --index-url https://download.pytorch.org/whl/cu128


---

## ▶️ Run

python app.py

---

## 🗃️ Database

All detections are automatically stored inside a SQLite database.

Each detection includes:

- Track ID
- Person Name
- Confidence Score
- Screenshot Path
- Detection Timestamp

---

## 📌 Current Features

✅ Person Detection

✅ Face Recognition

✅ Multi Object Tracking

✅ Screenshot Capture

✅ SQLite Detection Log

✅ GPU Acceleration

---

## 🚧 Upcoming Features

- Streamlit Dashboard
- Evidence Gallery
- Detection Analytics
- Search & Filters
- Unknown Person Alerts
- Detection History
- Multi-camera Support
