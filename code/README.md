# YOLO Object Detection with Streamlit

This project provides a modern, interactive web interface for object detection using YOLO (You Only Look Once) models with Streamlit.

## Features

- Upload images for object detection
- Select from a collection of sample test images
- Side-by-side comparison of original and processed images
- Filter detection results by object class
- Customizable bounding box colors
- Model selection (YOLOv8n, YOLOv8s, YOLOv8m)
- Adjustable confidence threshold
- Download processed images with bounding boxes
- Modern UI with white and green color scheme
- Pre-installed libraries for computer vision and machine learning
- No persistent storage of uploaded or processed images
- Tabbed interface for easy navigation

## Docker Setup

The project is containerized using Docker for easy deployment and development.

### Prerequisites

- Docker
- Docker Compose

### Running the Application

1. Clone this repository
2. Navigate to the project directory
3. Run the application using Docker Compose:

```bash
docker-compose up --build
```

4. Access the application at http://localhost:34000

### Development with Volume Mapping

The Docker setup includes volume mapping for the following directories:

- `./src:/app/src`: Maps the source code directory (includes resources, models, and sample images)
- `./.streamlit:/app/.streamlit`: Maps the Streamlit configuration directory

This allows you to make changes to the code on your local machine and see the changes immediately without rebuilding the Docker image. Streamlit automatically refreshes when code changes are detected.

## Project Structure

```
.
├── src/                # Source code directory
│   ├── app.py          # Main Streamlit application
│   ├── resources/      # Static resources (sample images, icons, etc.)
│   │   └── sample_images/ # Sample images for testing
│   └── models/         # Pre-trained and custom models
├── .streamlit/         # Streamlit configuration
├── Dockerfile          # Docker configuration
├── docker-compose.yml  # Docker Compose configuration
├── requirements.txt    # Core Python dependencies
└── requirements-dev.txt # Additional development dependencies
```

## Dependency Management

The project uses two requirements files to manage dependencies:

- **requirements.txt**: Contains the core dependencies needed for the application to run, including YOLO, PyTorch, TensorFlow, and other machine learning libraries.

- **requirements-dev.txt**: Documents additional libraries installed in the Docker container for development and enhanced functionality, such as Streamlit extensions and additional computer vision tools.

This separation helps avoid duplication and ensures that the Docker image only installs each dependency once, while still documenting all available libraries for developers.

## UI Features

The Streamlit UI includes:

- **Tabs**:
  - Upload Image: For uploading your own images
  - Sample Images: For selecting from pre-loaded test images

- **Sidebar**: 
  - Model selection
  - Confidence threshold slider
  - Class filter input
  - Bounding box color picker

- **Main Content**:
  - File uploader or sample image selection
  - Side-by-side image comparison
  - Download button for processed images
  - Detection details with counts and confidence scores

## Pre-installed Libraries

The Docker image comes with a comprehensive set of pre-installed libraries for computer vision, machine learning, and data science:

### Core Libraries (from requirements.txt)
- OpenCV: Computer vision and image processing
- PyTorch & TorchVision: Deep learning framework
- TensorFlow: Deep learning framework
- Ultralytics: YOLO implementation
- ONNX & ONNX Runtime: Model optimization and inference
- NumPy, Pandas, Matplotlib, Seaborn, Plotly: Data processing and visualization
- SciPy, Scikit-learn, Scikit-image: Scientific computing and machine learning

### Additional Libraries (from Dockerfile)
- Streamlit Extensions: For enhanced UI components
- Albumentations: Image augmentation
- Supervision: Computer vision annotation tools
- Gradio: Alternative UI framework

See `requirements.txt` and `requirements-dev.txt` for the complete list of dependencies.

## Pre-loaded Models

The Docker image comes with pre-downloaded YOLOv8 models:
- YOLOv8n (Nano): Smallest and fastest model
- YOLOv8s (Small): Balance of speed and accuracy

## Sample Images

The Docker image includes 5 sample test images for quick testing of the object detection capabilities. These images are displayed in the "Sample Images" tab of the application.

## Customization

You can modify the code in the `src` directory to customize the application. Changes will be automatically applied due to Streamlit's hot-reloading feature.

## License

[MIT License](LICENSE) 