# Docker Setup

This directory contains all Docker-related files for the YOLO Object Detection with Streamlit project.

## Files

- `Dockerfile` - Defines a container image with GPU support using CUDA
- `docker-compose.yml` - Configuration for container deployment (not actively used)
- `.dockerignore` - Specifies files to exclude from the Docker build
- `build.sh` - Helper script to build the Docker image with GPU support
- `run.sh` - Helper script to run the Docker container with GPU support
- `container-startup.sh` - Runtime script to detect GPU availability inside the container

## GPU Support

This setup is designed to run with NVIDIA GPU support for optimal performance:

- Built with CUDA 11.8 and cuDNN for PyTorch GPU acceleration
- Gracefully falls back to CPU if no compatible GPU is available
- Requires NVIDIA drivers and NVIDIA Container Toolkit on the host

## Usage

### Building the Image

```bash
# Build with default settings
./docker/build.sh

# Build with custom name and tag
./docker/build.sh --name user/cds-object-detection --tag v1.0

# Build using a full image reference
./docker/build.sh --tag username/my-yolo-app:1.0.0
```

### Running the Container

```bash
# Run with default settings (port 34000)
./docker/run.sh

# Run in detached mode
./docker/run.sh -d

# Run custom named image
./docker/run.sh --name mycompany/object-detection --tag v1.0

# Run on a different port
./docker/run.sh --port 8080 -d

# Run with a custom container name
./docker/run.sh --container-name my-yolo-container
```

## Docker Hub Publishing

To publish to Docker Hub:

```bash
# Build and tag in one step
./docker/build.sh --name yourusername/yolo-streamlit --tag latest

# Push the image
docker push yourusername/yolo-streamlit:latest
```

## GPU Requirements for Users

For optimal performance:

1. A compatible NVIDIA GPU
2. NVIDIA drivers installed
3. NVIDIA Container Toolkit (nvidia-docker2)

The application will gracefully fall back to CPU-only mode if GPU is not available.

## Running from DockerHub (for your users)

Users can run your published images directly:

```bash
# With GPU support
docker run --gpus all -p 34000:8000 yourusername/yolo-streamlit:latest

# Without GPU (will use CPU)
docker run -p 34000:8000 yourusername/yolo-streamlit:latest
```

## Stopping Containers

```bash
# Stop the container
docker stop yolo-streamlit-container

# Remove the container
docker rm yolo-streamlit-container
```

## Access the Application

- Access via: http://localhost:34000 (or the port you specified) 