# Tesla_Autopilot_Object_Detection_Clone-Developer6316

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![OpenCV](https://img.shields.io/badge/OpenCV-4.5+-green.svg)
![YOLO](https://img.shields.io/badge/YOLO-v8-orange.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

A cross-platform real-time object detection and lane tracking system that mimics Tesla's Autopilot interface. Built with YOLOv8 and OpenCV.

## 🚀 Features

- **Real-time Object Detection** – YOLOv8 powered detection of vehicles, pedestrians, traffic signs, and more
- **Lane Detection** – Advanced lane marking with ROI-based filtering
- **Multiple Input Sources** – Webcam, photo, or video file support
- **Modern Dark GUI** – Sleek Tesla-inspired interface using CustomTkinter
- **Cross-Platform** – Works on Windows, macOS, and Linux
- **Performance Metrics** – Real-time FPS display

## 📋 Prerequisites

- Python 3.8 or higher
- Webcam (optional, for live detection)

## 🔧 Installation

### 1. Clone the Repository
```
git clone https://github.com/yourusername/tesla-autopilot-clone.git
cd tesla-autopilot-clone
```
### 2. Create a Virtual Environment (Recommended)
```
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```
### 4. Install Dependencies
```
pip install -r requirements.txt
```
### 6. Download YOLOv8 Weights
The application will automatically download the YOLOv8n model on first run. Alternatively, you can manually download it:
```
wget https://github.com/ultralytics/assets/releases/download/v0.0.0/yolov8n.pt
```
# Quick Setup Commands
After creating these files, run these commands to initialize your GitHub repository:

```
# Initialize Git repository
git init

# Add all files
git add .

# Commit changes
git commit -m "Initial commit: Tesla Autopilot Clone"

# Create repository on GitHub and push
git remote add origin https://github.com/yourusername/tesla-autopilot-clone.git
git branch -M main
git push -u origin main
```

## 🚀 Usage
Run the Application
```
python autopil2.py
```
Using the Interface
Select Input Source – Choose between Webcam, Photo, or Video

For Photo/Video – Click the respective "Select" button to choose your file

Click "Start Detection" – Begin real-time analysis

Click "Stop" – Stop the current detection session

Keyboard Shortcuts
Key	Action
Ctrl+Q	Quit application

## 📁 Project Structure
```
tesla-autopilot-clone/
├── autopil2.py          # Main application file
├── requirements.txt     # Python dependencies
├── README.md           # This file
├── LICENSE             # MIT License
├── .gitignore          # Git ignore file
└── yolov8n.pt          # YOLOv8 weights (auto-downloaded)
```
## 🛠️ Technical Details
Detection Engine
Model: YOLOv8n (lightweight, fast inference)

Detection Classes: 80 COCO classes (people, vehicles, traffic lights, etc.)

Lane Detection: Canny edge detection + Hough Line Transform

ROI: Custom trapezoidal region of interest

Performance
CPU: ~10-15 FPS (depending on hardware)

GPU: ~30-60 FPS (with CUDA support)

Resolution: 800x450 (optimized for performance)

⚙️ Configuration
Model Selection
Edit DetectionEngine in autopil2.py:

```python
self.model = YOLO("yolov8n.pt")  # Change to yolov8s.pt, yolov8m.pt, etc.
```
### GPU Acceleration
Uncomment GPU support in DetectionEngine:

```python
# self.model.to('cpu')  # Comment this line
self.model.to('cuda')   # Uncomment this line
```
📸 Screenshots
(Add screenshots of your application here)

### 🐛 Known Issues
First Run: Initial model download may take a few minutes

CPU Performance: Detection speed depends on hardware capability

Video Loop: Videos loop automatically in playback mode

### 🤝 Contributing
Contributions are welcome! Here's how:

Fork the repository

Create a feature branch (git checkout -b feature/AmazingFeature)

Commit your changes (git commit -m 'Add some AmazingFeature')

Push to the branch (git push origin feature/AmazingFeature)

Open a Pull Request

### 📝 License
This project is licensed under the MIT License – see the LICENSE file for details.

### 🙏 Acknowledgments
Ultralytics YOLOv8 – Object detection framework

OpenCV – Computer vision library

CustomTkinter – Modern GUI toolkit

### ⚠️ Disclaimer
This project is for educational purposes only. It is not affiliated with or endorsed by Tesla, Inc. The autopilot functionality is a simulation and should not be used in real vehicles or safety-critical applications.
