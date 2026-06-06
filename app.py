import cv2
import mediapipe as mp
import pyttsx3
import streamlit as st
import numpy as np

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)

# Initialize Text-to-Speech
engine = pyttsx3.init()

# Gesture dictionary
gesture_dict = {
    "thumbs_up": "Yes",
    "thumbs_down": "No",
    "open_hand": "Hello",
    "fist": "Stop"
}

def speak(text):
    engine.say(text)
    engine.runAndWait()

def detect_gesture(hand_landmarks):
    landmarks = hand_landmarks.landmark
    thumb_tip = landmarks[mp_hands.HandLandmark.THUMB_TIP].y
    thumb_ip = landmarks[mp_hands.HandLandmark.THUMB_IP].y
    index_tip = landmarks[mp_hands.HandLandmark.INDEX_FINGER_TIP].y
    index_mcp = landmarks[mp_hands.HandLandmark.INDEX_FINGER_MCP].y

    if thumb_tip < thumb_ip:
        return "thumbs_up"
    elif thumb_tip > thumb_ip:
        return "thumbs_down"
    elif index_tip < index_mcp:
        return "open_hand"
    elif abs(index_tip - index_mcp) < 0.05:
        return "fist"
    else:
        return None

# Streamlit UI
st.title("🖐️ Sign-to-Speech Converter")
st.write("Show your hand gestures to the camera and hear them spoken aloud.")

run = st.checkbox("Start Camera")

FRAME_WINDOW = st.image([])

cap = cv2.VideoCapture(0)

while run:
    success, img = cap.read()
    if not success:
        st.write("Camera not detected.")
        break

    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(img_rgb)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_draw.draw_landmarks(img, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            gesture = detect_gesture(hand_landmarks)
            if gesture and gesture in gesture_dict:
                text = gesture_dict[gesture]
                cv2.putText(img, text, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                st.write(f"Detected Gesture: **{text}**")
                speak(text)

    FRAME_WINDOW.image(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))

cap.release()
