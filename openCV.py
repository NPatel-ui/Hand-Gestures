import cv2
import mediapipe as mp
import numpy as np
import pyautogui
import time
import math
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1)
mp_draw = mp.solutions.drawing_utils

# Initialize webcam
cap = cv2.VideoCapture(0)

# Initialize pycaw for system volume control
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None
)
volume_control = cast(interface, POINTER(IAudioEndpointVolume))
min_vol, max_vol = volume_control.GetVolumeRange()[:2]  # Min and Max volume in dB

# Gesture state
prev_gesture = ''
gesture_delay = 1  # seconds
last_action_time = time.time()

while True:
    success, img = cap.read()
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(img_rgb)

    h, w, c = img.shape
    lm_list = []

    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            mp_draw.draw_landmarks(img, handLms, mp_hands.HAND_CONNECTIONS)

            for id, lm in enumerate(handLms.landmark):
                cx, cy = int(lm.x * w), int(lm.y * h)
                lm_list.append((cx, cy))

        if lm_list:
            x1, y1 = lm_list[4]    # Thumb tip
            x2, y2 = lm_list[8]    # Index tip
            length = math.hypot(x2 - x1, y2 - y1)

            # Volume Control
            volume = np.interp(length, [30, 200], [0, 100])
            vol_db = np.interp(volume, [0, 100], [min_vol, max_vol])
            volume_control.SetMasterVolumeLevel(vol_db, None)

            cv2.putText(img, f'Volume: {int(volume)}%', (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 3)

            # Example Gesture Recognition Logic (simplified)
            current_time = time.time()

            # Play/Pause Gesture: Open Palm (length > 150)
            if length > 150 and (current_time - last_action_time) > gesture_delay:
                pyautogui.press('space')  # Play/Pause
                prev_gesture = 'Play/Pause'
                last_action_time = current_time

            # Next Track Gesture: Swipe Right
            if lm_list[8][0] - lm_list[4][0] > 50 and (current_time - last_action_time) > gesture_delay:
                pyautogui.press('right')  # Next Track
                prev_gesture = 'Next Track'
                last_action_time = current_time

            # Previous Track Gesture: Swipe Left
            if lm_list[4][0] - lm_list[8][0] > 50 and (current_time - last_action_time) > gesture_delay:
                pyautogui.press('left')  # Previous Track
                prev_gesture = 'Previous Track'
                last_action_time = current_time

            cv2.putText(img, f'Gesture: {prev_gesture}', (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 3)

    cv2.imshow('Hand Gesture Media Controller', img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
