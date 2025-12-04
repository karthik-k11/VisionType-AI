# VisionType AI: Virtual Gesture Keyboard ⌨️🖐️

A contactless, virtual keyboard interface powered by Computer Vision. This project enables users to type and save notes in mid-air using hand gestures, eliminating the need for physical hardware.

![Python](https://img.shields.io/badge/Python-3.10-blue) ![OpenCV](https://img.shields.io/badge/OpenCV-Computer%20Vision-green) ![MediaPipe](https://img.shields.io/badge/MediaPipe-Hand%20Tracking-orange) ![cvzone](https://img.shields.io/badge/cvzone-Vision%20Utils-blueviolet) ![pynput](https://img.shields.io/badge/pynput-Keyboard%20Control-red)

## 🚀 Features

* **Touchless Typing:** Uses the **Thumb & Index Finger** pinch gesture to register key presses with high precision.
* **Smart Interactions:**
    * **SHIFT Mode:** Toggle between uppercase and lowercase letters visually and functionally.
    * **SAVE Function:** Instantly saves your typed notes to a local `.txt` file with a timestamp.
    * **Real-time Feedback:** Keys light up and change color (Hover vs. Click) for an intuitive user experience.
* **Custom Geometry Logic:** Implements manual Euclidean distance calculations for click detection, removing reliance on heavy wrapper logic.
* **Modern UI:** A sleek, semi-transparent Dark Mode interface designed for visibility.
* **Performance:** Optimized for speed with a built-in FPS counter.

## 🛠️ Tech Stack

* **Language:** Python 3.10
* **Core Libraries:**
    * `opencv-python` (Image Processing)
    * `mediapipe` (Hand Landmark Detection)
    * `cvzone` (Helper module for Math/UI)
    * `pynput` (Simulates physical keyboard presses)