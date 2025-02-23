import cv2
import numpy as np
import streamlit as st

st.title("Webcam Number Detection")

# Open webcam
cap = cv2.VideoCapture(0)

if st.button("Capture Frame"):
    ret, frame = cap.read()
    if ret:
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        points_of_interest = [(100, 100), (200, 150), (300, 200)]
        values = [gray[y, x] for x, y in points_of_interest]
        threshold = 128
        binary_values = [1 if val > threshold else 0 for val in values]
        number = int("".join(map(str, binary_values)), 2)

        st.image(frame, channels="BGR")
        st.write(f"Computed Number: {number}")

cap.release()
