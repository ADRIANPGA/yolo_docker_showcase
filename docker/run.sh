#!/bin/bash
set -e  # Exit immediately if a command exits with a non-zero status

# Navigate to the parent directory (project root)
cd "$(dirname "$0")/.."

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
  echo "Error: Docker is not running or not properly configured."
  echo "Please start Docker and try again."
  exit 1
fi

# Parse arguments
DETACHED=""
IMAGE_NAME=""
IMAGE_TAG=""
PORT="34000"
CONTAINER_NAME="yolo-streamlit-container"
ARGS=""

# Process command line arguments
while [[ $# -gt 0 ]]; do
  case "$1" in
    -d|--detach)
      DETACHED="-d"
      shift
      ;;
    --name)
      IMAGE_NAME="$2"
      shift 2
      ;;
    --tag)
      # Check if the tag contains a colon, which might indicate a full image reference
      if [[ "$2" == *":"* ]]; then
        # Split the value into name and tag parts
        IMAGE_NAME=$(echo "$2" | cut -d':' -f1)
        IMAGE_TAG=$(echo "$2" | cut -d':' -f2)
        echo "Detected full image reference. Using name='$IMAGE_NAME', tag='$IMAGE_TAG'"
      else
        IMAGE_TAG="$2"
      fi
      shift 2
      ;;
    --port)
      PORT="$2"
      shift 2
      ;;
    --container-name)
      CONTAINER_NAME="$2"
      shift 2
      ;;
    *)
      # Pass other arguments to docker run
      ARGS="$ARGS $1"
      shift
      ;;
  esac
done

echo "Running Docker container with GPU support..."

# Create logs directory if it doesn't exist
mkdir -p logs

# Set the default image name and tag if not provided
if [ -z "$IMAGE_NAME" ]; then
  IMAGE_NAME="yolo-streamlit"
fi

if [ -z "$IMAGE_TAG" ]; then
  IMAGE_TAG="latest"
fi

FULL_IMAGE_NAME="$IMAGE_NAME:$IMAGE_TAG"

# Check if the image exists
if ! docker image inspect $FULL_IMAGE_NAME > /dev/null 2>&1; then
  echo "Error: Image $FULL_IMAGE_NAME does not exist."
  echo "Please build the image first with: ./docker/build.sh"
  exit 1
fi

# Check if nvidia-smi is available for GPU mode
if ! command -v nvidia-smi &> /dev/null; then
  echo "Warning: No NVIDIA GPU found or NVIDIA Docker toolkit not installed."
  echo "To run with GPU support, you need:"
  echo "  1. A compatible NVIDIA GPU"
  echo "  2. NVIDIA drivers installed"
  echo "  3. NVIDIA Container Toolkit (nvidia-docker2)"
  echo ""
  echo "The container will run in CPU-only mode (slower performance)."
  GPU_FLAG=""
else
  echo "NVIDIA GPU found. Using --gpus all flag for hardware acceleration..."
  GPU_FLAG="--gpus all"
fi

# Remove container if it already exists
if docker ps -a --format '{{.Names}}' | grep -q "^${CONTAINER_NAME}$"; then
  echo "Removing existing container ${CONTAINER_NAME}..."
  if ! docker rm -f ${CONTAINER_NAME} > /dev/null; then
    echo "Error: Failed to remove existing container."
    exit 1
  fi
fi

# Common volume mappings and environment variables
COMMON_OPTS="-p $PORT:8000 \
  -v $(pwd)/src:/app/src \
  -v $(pwd)/logs:/app/logs \
  -e PYTHONPATH=/app \
  -e PYTHONUNBUFFERED=1 \
  -e STREAMLIT_SERVER_PORT=8000 \
  -e STREAMLIT_SERVER_ADDRESS=0.0.0.0 \
  -e STREAMLIT_BROWSER_GATHER_USAGE_STATS=false \
  -e STREAMLIT_THEME_PRIMARY_COLOR=#2e7d32 \
  -e LOG_LEVEL=INFO \
  -e LOG_TO_FILE=true \
  -e LOG_FILENAME=/app/logs/app.log"

# Run the container using docker run
echo "Starting container on port $PORT..."
if ! docker run $DETACHED $COMMON_OPTS \
  $GPU_FLAG \
  --name $CONTAINER_NAME \
  $FULL_IMAGE_NAME $ARGS; then
  
  if [ -n "$GPU_FLAG" ]; then
    echo "Error: Failed to start container with GPU support."
    echo "Trying to run without GPU support..."
    if ! docker run $DETACHED $COMMON_OPTS \
      --name $CONTAINER_NAME \
      $FULL_IMAGE_NAME $ARGS; then
      echo "Error: Failed to start container."
      exit 1
    fi
  else
    echo "Error: Failed to start container."
    exit 1
  fi
fi

# If running in detached mode
if [ -n "$DETACHED" ]; then
  echo ""
  echo "Container started successfully."
  echo "Access the application at: http://localhost:$PORT"
  
  # Show GPU status if available
  if [ -n "$GPU_FLAG" ]; then
    echo ""
    echo "GPU support is enabled. CUDA should be available inside the container."
    echo "To verify GPU utilization, run: nvidia-smi"
  else
    echo ""
    echo "Running in CPU-only mode. For faster performance, consider adding GPU support."
  fi
fi 