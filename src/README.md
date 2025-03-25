# YOLO Object Detection App

This is a Streamlit-based web application for object detection using YOLO (You Only Look Once) models.

## Features

- Object detection using YOLOv8 models
- Upload your own images or use sample images
- Adjust confidence threshold for detection
- Filter detections by class
- Customize bounding box colors
- Download processed images with detections

## Environment Setup

### Required Python Version
This application requires Python 3.11.5.

### Setup on Windows

1. Install Python 3.11.5 from the [official Python website](https://www.python.org/downloads/release/python-3115/)

2. Install Microsoft Visual C++ Build Tools (required for some packages):
   - Download the [Visual Studio Build Tools](https://visualstudio.microsoft.com/visual-cpp-build-tools/)
   - During installation, select "Desktop development with C++"

3. Open Command Prompt as Administrator and create a virtual environment:
   ```batch
   cd path\to\project\src
   python -m venv yolost
   yolost\Scripts\activate
   ```

4. Install the required packages:
   ```batch
   pip install -r requirements.txt
   ```

### Setup on WSL (Ubuntu)

1. Open WSL terminal and install Python 3.11.5:
   ```bash
   sudo apt update
   sudo apt install software-properties-common -y
   
   sudo apt install python3.11 python3.11-venv python3.11-dev -y
   ```
2. Create a virtual environment:
   ```bash
   cd path/to/project/src
   python3.11 -m venv yolost
   source yolost/bin/activate
   ```

3. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

## Running the App

To run the app, make sure your virtual environment is activated, navigate to the `src` directory and run:

```bash
streamlit run main.py
```

If that doesn't work, try:

```bash
python -m streamlit run main.py
```

## Troubleshooting

If you encounter issues with the installation:

1. Ensure you're using Python 3.11.5
2. For Windows users, make sure you've installed Microsoft Visual C++ Build Tools
3. If installation fails, try installing packages one by one:
   ```
   pip install streamlit==1.34.0
   pip install numpy==1.26.4
   pip install opencv-python-headless==4.9.0.80
   pip install pillow==10.3.0
   pip install ultralytics==8.1.9
   pip install torch==2.2.0+cpu torchvision==0.17.0+cpu --extra-index-url https://download.pytorch.org/whl/cpu
   pip install onnx==1.17.0
   pip install pyyaml==6.0.1 tqdm==4.66.3 matplotlib==3.8.2
   ```
4. If you encounter DLL load errors on Windows, install the [Microsoft Visual C++ Redistributable](https://aka.ms/vs/17/release/vc_redist.x64.exe) 