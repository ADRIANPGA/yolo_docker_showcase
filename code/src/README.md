# YOLO Object Detection App

This is a Streamlit-based web application for object detection using YOLO (You Only Look Once) models.

## Project Structure

The application is organized in a modular structure:

```
src/
├── main.py           # Main entry point for the application
├── ui.py             # UI components and styling
├── detection.py      # Object detection logic
├── utils.py          # Utility functions
├── models/           # Directory for model files
│   ├── yolov8n.pt    # YOLOv8 nano model
│   ├── yolov8n.onnx  # YOLOv8 nano ONNX model
│   └── ...
└── resources/        # Resources like images, logos, etc.
    ├── cds_logo.png  # Logo for the sidebar
    └── sample_images/ # Sample images for testing
```

## Features

- Object detection using YOLOv8 models
- Support for both PyTorch and ONNX models
- Upload your own images or use sample images
- Adjust confidence threshold for detection
- Filter detections by class
- Customize bounding box colors
- Download processed images with detections

## Running the App

To run the app, navigate to the `src` directory and run:

```bash
streamlit run main.py
```

## Dependencies

The app requires the following main dependencies:
- streamlit
- opencv-python
- numpy
- ultralytics (for YOLOv8)
- Pillow

## Customization

You can customize the app by:
- Adding more models to the `models` directory
- Adding sample images to the `resources/sample_images` directory
- Modifying the UI styling in the `ui.py` file 