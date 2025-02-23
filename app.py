import cv2
import numpy as np
import streamlit as st

st.title("Webcam Number Detection")

# Function to detect available webcams
def list_available_cameras(max_cameras=5):
    """Detect available camera indices by attempting to open them."""
    available_cams = []
    for i in range(max_cameras):  # Check first `max_cameras` indices
        cap = cv2.VideoCapture(i, cv2.CAP_DSHOW)  # Use DirectShow backend for Windows (optional)
        if cap.isOpened():
            available_cams.append(i)
        cap.release()
    return available_cams

# Detect available webcams
available_cameras = list_available_cameras()
if not available_cameras:
    st.error("No webcams detected. Please connect a camera and restart the app.")
else:
    # Map detected cameras to Streamlit dropdown
    webcam_options = {f"Camera {i}": i for i in available_cameras}
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
