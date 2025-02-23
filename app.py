import cv2
import numpy as np
import streamlit as st

st.title("Webcam Number Detection")

# List available webcams (manually defined for now)
webcam_options = {
    "Default Webcam (0)": 0,
    "External Webcam (1)": 1,
    "Other Device (2)": 2
}

# User selects webcam
selected_webcam = st.selectbox("Select Webcam", list(webcam_options.keys()))
cam_index = webcam_options[selected_webcam]

# Open the selected webcam
cap = cv2.VideoCapture(cam_index)

if "detected_number" not in st.session_state:
    st.session_state.detected_number = "No number detected yet"

if st.button("Capture Frame"):
    ret, frame = cap.read()
    if ret:
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        points_of_interest = [(100, 100), (200, 150), (300, 200)]
        values = [gray[y, x] for x, y in points_of_interest]
        threshold = 128
        binary_values = [1 if val > threshold else 0 for val in values]
        detected_number = int("".join(map(str, binary_values)), 2)

        st.image(frame, channels="BGR")
        st.session_state.detected_number = f"Computed Number: {detected_number}"

cap.release()

# Display the detected number
st.write(st.session_state.detected_number)
