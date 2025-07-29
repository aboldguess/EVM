import cv2
import numpy as np
from scipy.signal import butter, filtfilt

# Ask the user for the video file path
input_video = input("Video path: ")

# Output filename for the amplified result
output_video = input_video.split(".")[0] + "_amplified" + ".mp4"

# Amplification factor controls how strong the motion exaggeration is
amplification_factor = 50  # Adjust for clearer but smooth amplification

# Frequency band (in Hz) that contains the motion to highlight
low_freq = 0.4
high_freq = 1.0

# Load the video
cap = cv2.VideoCapture(input_video)
if not cap.isOpened():
    print("Error: Could not open video file.")
    exit()

# Get video properties
frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = int(cap.get(cv2.CAP_PROP_FPS))

# Video writer setup for saving amplified output with high quality
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter(output_video, fourcc, fps, (frame_width, frame_height), isColor=False)

# Read all frames into a list for processing
frames = []
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break
    # Convert each frame to grayscale for processing
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    frames.append(gray_frame)

cap.release()
frames = np.array(frames, dtype='float32')

# Apply temporal filtering to isolate vibrations within frequency bounds
def bandpass_filter(data, lowcut, highcut, fs, order=2):
    """Apply a Butterworth bandpass filter along the time axis."""
    nyquist = 0.5 * fs
    low = lowcut / nyquist
    high = highcut / nyquist
    b, a = butter(order, [low, high], btype="band")
    y = filtfilt(b, a, data, axis=0)
    return y

# Apply the bandpass filter to the frames to get the motion component
filtered_frames = bandpass_filter(frames, low_freq, high_freq, fps)

# Amplify the filtered frames and add back to the original frames
amplified_frames = frames + amplification_factor * filtered_frames

# Convert back to uint8 and save each frame to the output video
for amplified_frame in amplified_frames:
    amplified_frame = np.clip(amplified_frame, 0, 255)  # Clip values to ensure they stay in the 0-255 range
    amplified_frame = amplified_frame.astype('uint8')
    out.write(amplified_frame)

out.release()
print("Amplified grayscale video saved as:", output_video)
