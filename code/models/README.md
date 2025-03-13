# Models Directory

This directory contains pre-trained models for the YOLO Object Detection application.

## Pre-installed Models

The Docker container comes pre-loaded with the following models:
- `yolov8n.pt`: YOLOv8 Nano model (smallest, fastest)
- `yolov8s.pt`: YOLOv8 Small model (balance of speed and accuracy)

## Adding Custom Models

You can add your own custom-trained models to this directory. The directory is mounted as a volume in the Docker container, so any models you add here will be immediately available to the application.

## Supported Model Formats

The application supports the following model formats:
- PyTorch (`.pt`)
- ONNX (`.onnx`)

## Model Conversion

The application can automatically convert PyTorch models to ONNX format for faster inference. When a PyTorch model is first used, an ONNX version will be created and saved for future use.

## Using Custom Models

To use a custom model in the application:

1. Place your model file in this directory
2. Update the application code to include your model in the model selection dropdown
3. Restart the application if necessary

Example code to add a custom model:

```python
# Add to the model_mapping dictionary in app.py
model_mapping = {
    "YOLOv8n": "yolov8n",
    "YOLOv8s": "yolov8s",
    "YOLOv8m": "yolov8m",
    "My Custom Model": "path/to/custom_model"
} 