# Eulerian Video Magnification

This project demonstrates basic Eulerian Video Magnification (EVM) techniques in Python. EVM reveals subtle motions in video by applying temporal bandpass filtering and amplifying the resulting signal. These scripts provide a minimal working example for experimenting with EVM on your own videos.

## Prerequisites
- Python 3.8 or later
- `opencv-python`
- `numpy`
- `scipy`

All Python dependencies are listed in `requirements.txt`. Install them with:
```bash
pip install -r requirements.txt
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

## Web interface

For an interactive GUI in your browser, run the Streamlit app. Using
`python -m` ensures the module is launched even if the `streamlit`
executable is not on your system `PATH`:

```bash
python -m streamlit run web_gui.py
```

If you prefer, you can also execute the script directly with Python:

```bash
python web_gui.py
```

Upload a video, adjust the parameters in the sidebar, and download the
amplified result directly from the page.
