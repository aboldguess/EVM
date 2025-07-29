# Eulerian Video Magnification

This project demonstrates basic Eulerian Video Magnification (EVM) techniques in Python. EVM reveals subtle motions in video by applying temporal bandpass filtering and amplifying the resulting signal. These scripts provide a minimal working example for experimenting with EVM on your own videos.

## Prerequisites
- Python 3.8 or later
- `opencv-python`
- `numpy`
- `scipy`

Install the dependencies with:
```bash
pip install opencv-python numpy scipy
```

Sample videos are provided in the `sample_videos/` directory (`camera.mp4`, `subway.mp4`, and `wrist.mp4`) to test the scripts and observe the effect of motion amplification.

## Usage
Two scripts are included:

- `amp_color.py` – processes color videos.
- `amp_grayscale.py` – processes grayscale videos.

Run them by providing the path to a video when prompted. Example:
```bash
python amp_color.py       # for color amplification
python amp_grayscale.py   # for grayscale amplification
```
The processed video will be saved next to the source file with `_amplified` appended to its name.
