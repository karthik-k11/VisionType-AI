import cv2
from cvzone.HandTrackingModule import HandDetector
from pynput.keyboard import Controller, Key
import time
import math
from datetime import datetime

# --- SETTINGS ---
CAM_WIDTH, CAM_HEIGHT = 1280, 720
CLICK_SENSITIVITY = 40  # Slightly lower for thumb pinch accuracy
CLICK_COOLDOWN = 0.20 

THEME = {
    'bg': (25, 25, 25), 
    'key': (50, 50, 50), 
    'hover': (70, 70, 70), 
    'click': (0, 255, 127), 
    'shift_active': (255, 100, 100),
    'save_btn': (138, 43, 226),      # Purple color for Save button
    'text': (255, 255, 255), 
    'border': (200, 200, 200)
}