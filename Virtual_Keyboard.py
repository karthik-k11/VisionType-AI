import cv2
from cvzone.HandTrackingModule import HandDetector
from pynput.keyboard import Controller, Key
import time
import math
from datetime import datetime

#Settings
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

        
        # Text Logic 
        display_text = k.text
        if len(display_text) == 1: 
            display_text = display_text.upper() if shift_active else display_text.lower()

        scale = 1.5 if len(display_text) > 1 else 3.5
        off_x = 10 if len(display_text) > 1 else 22 # Slight adjustment for longer words
        
        cv2.putText(frame, display_text, (k.x + off_x, k.y + 60), 
                    cv2.FONT_HERSHEY_PLAIN, scale, THEME['text'], 3)
    return frame
def save_to_file(text_content):
    if not text_content: return
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open("my_notes.txt", "a") as f:
        f.write(f"[{timestamp}] {text_content}\n")

# --- SETUP ---
cap = cv2.VideoCapture(0)
cap.set(3, CAM_WIDTH)
cap.set(4, CAM_HEIGHT)
detector = HandDetector(detectionCon=0.8, maxHands=1)
kb = Controller()

keys_layout = [
    ["Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P"],
    ["A", "S", "D", "F", "G", "H", "J", "K", "L", ";"],
    ["Z", "X", "C", "V", "B", "N", "M", ",", ".", "/"],
    ["SHIFT", "SPACE", "BKSP", "CLR", "SAVE"] # Condensed names to fit
]

virtual_keys = []
# Generate Layout
for i, row in enumerate(keys_layout):
    for j, char in enumerate(row):
        w, h = 85, 85
        x, y = 50 + j * 105, 50 + i * 105
        
        # Manual positioning for the bottom row to fit 5 buttons
        if char == "SHIFT": w, x = 140, 50
        elif char == "SPACE": w, x = 230, 210
        elif char == "BKSP": w, x = 140, 460
        elif char == "CLR": w, x = 140, 620
        elif char == "SAVE": w, x = 140, 780
        
        virtual_keys.append(KeyButton(char, (x, y), (w, h)))

text_buf = ""
shift_mode = False
saved_feedback_timer = 0

while True:
    success, img = cap.read()
    if not success: break
    img = cv2.flip(img, 1)
    hands, img = detector.findHands(img, flipType=False)
    
    img = draw_keyboard(img, virtual_keys, shift_mode)

    if hands:
        lm = hands[0]['lmList']
        x1, y1 = lm[8][:2]  # Index Tip
        
        # Thumb configuration
        x2, y2 = lm[4][:2]  # Thumb Tip
        
        dist = get_dist((x1, y1), (x2, y2))

        for k in virtual_keys:
            if k.is_hovering(x1, y1):
                cv2.rectangle(img, (k.x, k.y), (k.x + k.w, k.y + k.h), THEME['hover'], cv2.FILLED)
                cv2.rectangle(img, (k.x, k.y), (k.x + k.w, k.y + k.h), THEME['border'], 2)
                
                # Re-draw text
                lbl = k.text
                if len(lbl) == 1: lbl = lbl.upper() if shift_mode else lbl.lower()
                scale = 1.5 if len(lbl) > 1 else 3.5
                cv2.putText(img, lbl, (k.x + 10, k.y + 60), cv2.FONT_HERSHEY_PLAIN, scale, THEME['text'], 3)

                # Click Check
                if dist < CLICK_SENSITIVITY and (time.time() - k.last_click) > CLICK_COOLDOWN:
                    k.last_click = time.time()
                    cv2.rectangle(img, (k.x, k.y), (k.x + k.w, k.y + k.h), THEME['click'], cv2.FILLED)

                    # --- LOGIC ---
                    if k.text == "SHIFT":
                        shift_mode = not shift_mode
                    elif k.text == "SPACE":
                        text_buf += " "
                        kb.press(Key.space); kb.release(Key.space)
                    elif k.text == "BKSP":
                        text_buf = text_buf[:-1]
                        kb.press(Key.backspace); kb.release(Key.backspace)
                    elif k.text == "CLR":
                        text_buf = ""
                    elif k.text == "SAVE":
                        save_to_file(text_buf)
                        text_buf = "" # Clear after save
                        saved_feedback_timer = time.time() # Start feedback timer
                    else:
                        char = k.text.upper() if shift_mode else k.text.lower()
                        text_buf += char
                        kb.press(char); kb.release(char)

    # --- TEXT BOX ---
    cv2.rectangle(img, (50, 550), (1230, 650), THEME['bg'], cv2.FILLED)
    cv2.rectangle(img, (50, 550), (1230, 650), THEME['border'], 2)

    # Show "SAVED!" message if we just saved
    if time.time() - saved_feedback_timer < 2: # Show for 2 seconds
        cv2.putText(img, "SAVED TO FILE!", (400, 620), cv2.FONT_HERSHEY_PLAIN, 4, (0, 255, 0), 4)
    else:
        cv2.putText(img, text_buf[-30:], (70, 620), cv2.FONT_HERSHEY_PLAIN, 4, THEME['text'], 4)

    cv2.imshow("VisionType Pro", img)
    if cv2.waitKey(1) & 0xFF == ord('q'): break

cap.release()
cv2.destroyAllWindows()

