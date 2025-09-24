# Drone Project #1: Video Frame Stitching

This project uses **Python** and **OpenCV** to extract frames from a drone video and stitch them into a single panoramic image covering the entire flight path. The project is designed to dynamically choose the optimal frame sampling and stitching parameters to balance **quality** and **processing time**.

---

## Features

- **Automatic frame extraction** from video at dynamic intervals
- **Dynamic downsampling and step selection** for optimal speed and quality
- **Panorama stitching** using OpenCV's `cv2.Stitcher`
- **Fast execution mode**: ensures stitching completes under 1 second per attempt
- Fully configurable: adjust `step`, `scale`, and maximum frames dynamically

---

## Requirements

- Python 3.8+
- OpenCV (`opencv-python`)
- NumPy (optional, if doing further image processing)

Install dependencies with:

```bash
pip install opencv-python
