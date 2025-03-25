# Object Detection with YOLO

This project provides applications for object detection using YOLO (You Only Look Once) models:

1. **FastAPI Microservice**: A high-performance API for object detection
2. **Streamlit UI**: A user-friendly web interface for visual object detection

## Quick Start

### Option 1: Running the Streamlit UI (Recommended for beginners)

1. Navigate to the Streamlit project directory:
   ```bash
   cd code/src
   ```

2. Follow the setup instructions in the [Streamlit README](code/src/README.md).

3. Once set up, run the application:
   ```bash
   streamlit run main.py
   ```

   The app will be available at http://localhost:8501

### Option 2: Docker (Advanced)

If you're familiar with Docker, you can run the application using Docker Compose:

1. Navigate to the project directory:
   ```bash
   cd code
   ```

2. Run Docker Compose:
   ```bash
   docker-compose up --build
   ```

3. Access the application at http://localhost:34000

## Features

- Detect objects in uploaded images
- Filter detection results by object class
- Adjustable confidence threshold
- Customizable bounding box colors
- Download processed images with bounding boxes

## Project Structure

```
.
├── Object_Detection_Yolo_with_FastAPI/  # FastAPI implementation
│   ├── app/                # FastAPI application
│   └── models/             # Model directory
│
└── code/                   # Streamlit implementation
    ├── src/                # Source code directory
    │   ├── app.py          # Main Streamlit application
    │   ├── resources/      # Static resources
    │   └── models/         # Pre-trained models
    └── requirements.txt    # Python dependencies
```