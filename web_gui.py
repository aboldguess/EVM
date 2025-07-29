"""Streamlit web interface to perform Eulerian Video Magnification."""

import streamlit as st
import cv2
import numpy as np
from scipy.signal import butter, filtfilt
import tempfile
import os

# Title for the web application displayed in browser
# Display the title at the top of the web page
st.title("Eulerian Video Magnification")

# Sidebar controls for user-adjustable parameters
st.sidebar.header("Parameters")

# How strongly to amplify subtle motion
a_factor = st.sidebar.slider(
    "Amplification factor", min_value=5, max_value=60, value=30, step=5
)
# Frequency band that contains the motion to reveal
low_freq = st.sidebar.number_input(
    "Low frequency (Hz)", min_value=0.1, max_value=2.0, value=0.4, step=0.1
)
high_freq = st.sidebar.number_input(
    "High frequency (Hz)", min_value=0.5, max_value=3.0, value=1.0, step=0.1
)

# File uploader lets the user choose a video from their machine
uploaded = st.file_uploader("Upload video", type=["mp4", "mov", "avi"])

# Helper function used to filter frames in the temporal domain

def bandpass_filter(data, lowcut, highcut, fs, order=2):
    """Apply a Butterworth bandpass filter along the time axis."""
    nyquist = 0.5 * fs
    low = lowcut / nyquist
    high = highcut / nyquist
    # Design filter and apply forward-backward filtering for zero phase shift
    b, a = butter(order, [low, high], btype="band")
    return filtfilt(b, a, data, axis=0)

# When the user presses the button, process the video
if uploaded and st.button("Process video"):
    # Use a temporary directory so intermediate files are cleaned up automatically
    with tempfile.TemporaryDirectory() as tmpdir:
        # Save the uploaded file to disk for OpenCV to read
        input_path = os.path.join(tmpdir, uploaded.name)
        with open(input_path, "wb") as f:
            f.write(uploaded.getbuffer())

        cap = cv2.VideoCapture(input_path)
        if not cap.isOpened():
            st.error("Could not open video file")
            st.stop()

        # Extract properties needed to create the output video
        frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps = cap.get(cv2.CAP_PROP_FPS)

        # Read all frames into memory for batch processing
        frames = []
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            # Convert BGR to RGB for consistency across platforms
            frames.append(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        cap.release()

        # Convert to float for processing, then apply bandpass filter
        frames = np.array(frames, dtype="float32")
        filtered_frames = bandpass_filter(frames, low_freq, high_freq, fps)
        # Add the amplified motion back onto the original frames
        amplified = frames + a_factor * filtered_frames

        # Write processed frames back to a new video file
        output_path = os.path.join(tmpdir, "amplified.mp4")
        fourcc = cv2.VideoWriter_fourcc(*"mp4v")
        out = cv2.VideoWriter(
            output_path, fourcc, fps, (frame_width, frame_height)
        )

        for frame in amplified:
            frame = np.clip(frame, 0, 255).astype("uint8")
            out.write(cv2.cvtColor(frame, cv2.COLOR_RGB2BGR))

        out.release()

        # Display the result and provide a download button
        st.success("Processing finished")
        with open(output_path, "rb") as f:
            st.download_button(
                label="Download amplified video",
                data=f,
                file_name="amplified.mp4",
                mime="video/mp4",
            )
            st.video(f)

