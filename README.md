# Hand Gesture Volume and Media Controller

A Python-based project that uses **OpenCV** and **MediaPipe** to implement real-time hand gesture recognition for controlling the **laptop volume** and **media player actions**. The system detects hand gestures using the webcam and allows intuitive control of volume, play, pause, next, and previous media playback without touching the keyboard or mouse.

---

## 🎯 Project Features

- 📷 Real-time hand tracking using **MediaPipe Hands**
- 🎛️ Volume control (increase, decrease, mute/unmute) using hand gestures
- ⏯️ Media player control:
  - Play/Pause
  - Next Track
  - Previous Track
- Visual feedback of hand landmarks and volume level
- Works using simple hand gestures in front of the webcam

---

## ✅ Technologies Used

- Python 🐍
- OpenCV (cv2) for webcam capture and display
- MediaPipe for accurate hand landmark detection
- Pycaw for controlling system audio volume
- PyAutoGUI for simulating media key presses

---

## 🚀 How It Works

1. The webcam captures the video feed.
2. MediaPipe detects hand landmarks in real time.
3. Specific hand gestures are recognized based on landmark positions:
   - Distance between thumb and index finger → Volume Up/Down
   - Number of fingers up → Play/Pause or Next/Previous track
4. System volume and media keys are controlled accordingly.

---

## 🎯 Example Gestures

| Gesture | Action |
|---------|--------|
| Pinch thumb + index closer/farther | Volume Up/Down |
| Open hand (5 fingers) | Play/Pause |
| Swipe left/right motion | Previous/Next Track |

---

## 💻 Prerequisites

- Python 3.7+
- Webcam

### 📦 Install dependencies

```bash
pip install opencv-python mediapipe pycaw pyautogui comtypes
