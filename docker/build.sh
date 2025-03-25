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
IMAGE_NAME=""
IMAGE_TAG=""
ARGS=""

# Process command line arguments
while [[ $# -gt 0 ]]; do
  case "$1" in
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
    *)
      # Pass other arguments
      ARGS="$ARGS $1"
      shift
      ;;
  esac
done

echo "Building Docker image with GPU support..."

# Set the default image name and tag if not provided
if [ -z "$IMAGE_NAME" ]; then
  IMAGE_NAME="yolo-streamlit"
fi

if [ -z "$IMAGE_TAG" ]; then
  IMAGE_TAG="latest"
fi

FULL_IMAGE_NAME="$IMAGE_NAME:$IMAGE_TAG"

# The project root is the current working directory after the cd command above
# So we use "." for the context and specify the Dockerfile path with -f
PROJECT_ROOT="."

# Build with GPU support
echo "Building GPU image: $FULL_IMAGE_NAME"
if ! docker build -t $FULL_IMAGE_NAME \
  --build-arg BASE=gpu \
  --build-arg PYTORCH_CUDA=cu118 \
  -f docker/Dockerfile $PROJECT_ROOT; then
  echo "Error: Failed to build GPU image."
  exit 1
fi

# Verify the image was created successfully
if ! docker image inspect $FULL_IMAGE_NAME > /dev/null 2>&1; then
  echo "Error: Image $FULL_IMAGE_NAME was not created successfully."
  exit 1
fi

echo "Build completed successfully for $FULL_IMAGE_NAME"
echo ""
echo "You can push this image to Docker Hub with:"
echo "docker push $FULL_IMAGE_NAME" 