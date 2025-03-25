# Object Detection with YOLO - Docker Microservices

This project provides dockerized microservices for object detection using YOLO (You Only Look Once) models. The application offers two implementation options:

1. **FastAPI Microservice**: A high-performance API for object detection
2. **Streamlit UI**: A modern, interactive web interface for visual object detection

Both implementations are containerized with Docker, making them easy to deploy and run.

## Features

- Detect objects in uploaded images
- Filter detection results by object class
- Pre-trained YOLO models (YOLOv8n, YOLOv8s, YOLOv8m)
- Adjustable confidence threshold
- Optimized for performance with ONNX format models
- RESTful API with FastAPI
- Interactive UI with Streamlit
- Containerized with Docker for easy deployment

## FastAPI Microservice

The FastAPI implementation provides a high-performance API for object detection.

### API Endpoints

- **POST /detect/<label?>**: Upload an image and detect objects with an optional label filter

### FastAPI Setup

1. Navigate to the API project directory:

    ```bash
    cd Object_Detection_Yolo_with_FastAPI
    ```

2. Build and run the Docker container:

    ```bash
    docker build -t object_detection .
    docker run -d -p 8000:8000 object_detection
    ```

3. Access the API at http://localhost:8000

### API Usage Examples

**cURL:**
```bash
curl -X POST 'http://localhost:8000/detect/person' -H 'accept: application/json' -H 'Content-Type: multipart/form-data' -F 'image=@bus.JPG;type=image/jpeg'
```

**Python:**
```python
import requests

# API endpoint URL
api_endpoint = "http://localhost:8000/detect/"

# Image file
image_path = "test_image1_bus_people.jpg"

# Make POST request
files = {"image": open(image_path, "rb")}
response = requests.post(api_endpoint, files=files)

# Check response
if response.status_code == 200:
    result = response.json()
    print("Detection Results:", result)
else:
    print("API request failed:", response.text)
```

## Streamlit UI

The Streamlit implementation provides a modern, interactive web interface for object detection.

### Streamlit Features

- Upload images or select from sample test images
- Side-by-side comparison of original and processed images
- Customizable bounding box colors
- Download processed images with bounding boxes
- Modern UI with white and green color scheme
- Tabbed interface for easy navigation

### Streamlit Setup

1. Navigate to the Streamlit project directory:

    ```bash
    cd code
    ```

2. Run the application using Docker Compose:

    ```bash
    docker-compose up --build
    ```

3. Access the application at http://localhost:34000

### Development with Volume Mapping

The Streamlit Docker setup includes volume mapping for:

- `./src:/app/src`: Maps the source code directory
- `./.streamlit:/app/.streamlit`: Maps the Streamlit configuration directory

This allows for immediate code changes without rebuilding the Docker image.

## Project Structure

```
.
├── Object_Detection_Yolo_with_FastAPI/  # FastAPI implementation
│   ├── app/                # FastAPI application
│   ├── test_images/        # Test images
│   ├── models/             # Model directory
│   ├── Dockerfile          # Docker configuration
│   └── requirements.txt    # Python dependencies
│
├── code/                   # Streamlit implementation
│   ├── src/                # Source code directory
│   │   ├── app.py          # Main Streamlit application
│   │   ├── resources/      # Static resources (sample images, icons, etc.)
│   │   └── models/         # Pre-trained and custom models
│   ├── .streamlit/         # Streamlit configuration
│   ├── Dockerfile          # Docker configuration
│   ├── docker-compose.yml  # Docker Compose configuration
│   ├── requirements.txt    # Core Python dependencies
│   └── requirements-dev.txt # Additional development dependencies
```

## YOLO Models and Usage

This project uses YOLOv8 models for object detection. The models are converted to ONNX format for improved performance.

### YOLO Python Usage

```python
from ultralytics import YOLO

# Load and export the model
model = YOLO('yolov8n.pt')  
model.export(format='onnx')

# Load the ONNX model
onnx_model = YOLO(onnx_model_path, task='detect')
source = "https://ultralytics.com/images/bus.jpg"

# Perform object detection
result = onnx_model(source, save=True)
```

For more examples, see the [YOLOv8 Documentation](https://docs.ultralytics.com).

## Pre-installed Libraries

Both implementations come with comprehensive libraries for computer vision and machine learning:

- **OpenCV**: Computer vision and image processing
- **PyTorch & TorchVision**: Deep learning framework
- **TensorFlow**: Deep learning framework
- **Ultralytics**: YOLO implementation
- **ONNX & ONNX Runtime**: Model optimization and inference
- **NumPy, Pandas, Matplotlib**: Data processing and visualization
- **FastAPI/Uvicorn/Gunicorn**: High-performance API framework (API version)
- **Streamlit**: Interactive UI framework (UI version)

## Docker Notes

Both implementations use Docker for containerization. The FastAPI version uses Uvicorn managed by Gunicorn for high performance, while the Streamlit version uses Streamlit's built-in server.

### Alpine Python Warning

It's generally recommended to avoid using Alpine for Python projects and opt for the `slim` Docker image versions instead. When installing Python packages in Alpine, you may encounter difficulties due to the lack of precompiled wheels, resulting in longer build times and potentially larger images.

## Testing

To test the FastAPI implementation, use the docker_image_test.py file in the test_images folder:

```bash
python docker_image_test.py
```

The tests should produce:
```json
Test Status: {'Test 1': 'Success', 'Test 2': 'Success', 'Test 3': 'Success'}
```

## License

[MIT License](LICENSE)