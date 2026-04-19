# 🏟 Real-Time Crowd Detection AI System

A Smart AI-powered system that detects crowd density in real-time using **YOLOv8, OpenCV, and Streamlit**.  
It helps in intelligent stadium management by analyzing crowd flow at multiple gates and providing real-time insights.

---

## 🚀 Features

- 🎥 Real-time webcam-based crowd detection  
- 🧠 YOLOv8 AI model (Ultralytics) integration  
- 🚪 Gate-wise crowd monitoring (Gate 1–4)  
- 🔄 Automatic gate cycling system  
- 📊 Live analytics dashboard  
- 📈 Real-time graph visualization  
- 🔥 Crowd heatmap analysis  
- 🚨 Emergency alert system  
- 🎟 Seat availability prediction  

---

## 🛠 Tech Stack

- Python  
- Streamlit  
- OpenCV  
- YOLOv8 (Ultralytics)  
- Pandas  
- Plotly  

---

## 📂 Project Structure
Real-Time-Crowd-Detection-AI/
│
├── app.py # Main Streamlit application (UI + live detection)
├── camera.py # Camera initialization and handling
├── crowd.py # YOLO-based crowd detection logic
├── logic.py # Smart analysis (best gate, alerts, status)
├── data.json # Sample crowd/gate data
├── requirements.txt # Required Python libraries
├── yolov8n.pt # Pre-trained YOLOv8 model
│
├── screenshots/ # Output images for README
│ ├── dashboard.png
│ ├── detection.png

## 📸 Output

### Dashboard
![Dashboard](<img width="1784" height="922" alt="Screenshot 2026-04-19 195720" src="https://github.com/user-attachments/assets/6bedcf47-85b5-4827-9991-1d47deaa600d" />
)

### Live Detection
![Detection](<img width="1736" height="649" alt="Screenshot 2026-04-19 195731" src="https://github.com/user-attachments/assets/000d0399-8529-41a3-aa60-3db97c4bbad0" />
)

