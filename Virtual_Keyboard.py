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

class KeyButton:
    def __init__(self, text, pos, size):
        self.text = text
        self.x, self.y = pos
        self.w, self.h = size
        self.last_click = 0

    def is_hovering(self, fx, fy):
        return self.x < fx < self.x + self.w and self.y < fy < self.y + self.h

def get_dist(p1, p2):
    return math.hypot(p2[0] - p1[0], p2[1] - p1[1])

def draw_keyboard(frame, keys, shift_active):
    overlay = frame.copy()
    cv2.rectangle(overlay, (20, 20), (1260, 460), THEME['bg'], cv2.FILLED)
    frame = cv2.addWeighted(overlay, 0.4, frame, 0.6, 0)

    for k in keys:
        # Determine Key Color
        if k.text == "SHIFT" and shift_active:
            color = THEME['shift_active']
        elif k.text == "SAVE":
            color = THEME['save_btn']
        else:
            color = THEME['key']
        
        cv2.rectangle(frame, (k.x, k.y), (k.x + k.w, k.y + k.h), color, cv2.FILLED)
        cv2.rectangle(frame, (k.x, k.y), (k.x + k.w, k.y + k.h), THEME['border'], 2)