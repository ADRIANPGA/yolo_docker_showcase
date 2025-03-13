# Use the Python image
FROM python:3.10

# Install necessary system packages
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    libgl1 \
    libglib2.0-0 \
    libsm6 \
    libxrender1 \
    libxext6 \
    ffmpeg \
    libavcodec-dev \
    libavformat-dev \
    libswscale-dev \
    libv4l-dev \
    libxvidcore-dev \
    libx264-dev \
    libatlas-base-dev \
    gfortran \
    wget \
    unzip \
    git \
    curl

# Create app directory structure
RUN mkdir -p /app/src /app/.streamlit

# Specify the directory where the application will run
WORKDIR /app

# Copy application files into the Docker image
COPY requirements.txt /app/
COPY src/ /app/src/
COPY .streamlit/ /app/.streamlit/

# Install base Python packages
RUN pip install --no-cache-dir --upgrade pip setuptools wheel

# Install Streamlit and extensions (not in requirements.txt)
RUN pip install --no-cache-dir \
    streamlit==1.34.0 \
    streamlit-webrtc \
    streamlit-drawable-canvas \
    streamlit-folium \
    streamlit-aggrid \
    streamlit-option-menu \
    streamlit-extras \
    streamlit-image-comparison

# Install computer vision packages not in requirements.txt
RUN pip install --no-cache-dir \
    opencv-python-headless \
    albumentations \
    supervision \
    gradio

# Install project-specific requirements (avoiding duplicates)
# This will skip packages that are already installed
RUN pip install --no-cache-dir -r requirements.txt

# Download YOLOv8 models
RUN mkdir -p /app/src/models
RUN wget -q https://github.com/ultralytics/assets/releases/download/v0.0.0/yolov8n.pt -O /app/src/models/yolov8n.pt
RUN wget -q https://github.com/ultralytics/assets/releases/download/v0.0.0/yolov8s.pt -O /app/src/models/yolov8s.pt

# Expose port for Streamlit
EXPOSE 8000

# Run the Streamlit application
CMD ["streamlit", "run", "src/app.py", "--server.port=8000", "--server.address=0.0.0.0", "--server.runOnSave=true"]