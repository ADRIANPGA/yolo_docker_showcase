ARG CUDA_VERSION=11.8.0
ARG CUDNN_VERSION=8
ARG UBUNTU_VERSION=22.04
ARG PYTHON_VERSION=3.10
ARG BASE=cpu

# ===== Base Image (CPU) =====
FROM python:${PYTHON_VERSION}-slim AS base-cpu

# System dependencies for OpenCV, etc.
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3-pip \
    libgl1 \
    libglib2.0-0 \
    libsm6 \
    libxrender1 \
    libxext6 \
    ffmpeg \
    wget \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# ===== Base Image (GPU) =====
FROM nvidia/cuda:${CUDA_VERSION}-cudnn${CUDNN_VERSION}-runtime-ubuntu${UBUNTU_VERSION} AS base-gpu

# Install Python and system dependencies without using PPA
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3 \
    python3-dev \
    python3-pip \
    python3-setuptools \
    python3-wheel \
    libgl1 \
    libglib2.0-0 \
    libsm6 \
    libxrender1 \
    libxext6 \
    ffmpeg \
    wget \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# Set Python aliases
RUN ln -sf /usr/bin/python3 /usr/bin/python && \
    ln -sf /usr/bin/pip3 /usr/bin/pip

# ===== Final Image Selection =====
FROM base-${BASE} AS final

# ===== Application Structure =====
RUN mkdir -p /app/src /app/logs

# Set working directory
WORKDIR /app

# Copy requirements first to leverage Docker cache
COPY src/requirements.txt /app/requirements.txt

# ===== Python Dependencies =====
# Install base Python packages
RUN pip install --no-cache-dir --upgrade pip setuptools wheel

# Install PyTorch with appropriate dependencies
ARG PYTORCH_VERSION=2.0.1
ARG PYTORCH_CUDA=cpu
ARG TORCH_VISION_VERSION=0.15.2
ARG TORCH_AUDIO_VERSION=2.0.2

# Install torch GPU or CPU version based on args
RUN if [ "$PYTORCH_CUDA" = "cpu" ]; then \
        pip install --no-cache-dir torch==${PYTORCH_VERSION} \
                                   torchvision==${TORCH_VISION_VERSION} \
                                   torchaudio==${TORCH_AUDIO_VERSION} \
                                   --extra-index-url https://download.pytorch.org/whl/cpu; \
    elif [ "$PYTORCH_CUDA" = "cu118" ]; then \
        pip install --no-cache-dir torch==${PYTORCH_VERSION} \
                                   torchvision==${TORCH_VISION_VERSION} \
                                   torchaudio==${TORCH_AUDIO_VERSION} \
                                   --extra-index-url https://download.pytorch.org/whl/cu118; \
    else \
        pip install --no-cache-dir torch torchvision torchaudio; \
    fi

# Install all requirements from requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

# ===== Copy Application Files =====
COPY src/ /app/src/

# ===== Download ML Models if not already present =====
RUN mkdir -p /app/src/models && \
    wget -q https://github.com/ultralytics/assets/releases/download/v0.0.0/yolov8n.pt -O /app/src/models/yolov8n.pt && \
    wget -q https://github.com/ultralytics/assets/releases/download/v0.0.0/yolov8s.pt -O /app/src/models/yolov8s.pt

# ===== Set port =====
EXPOSE 8000

# ===== Set Environment Variables =====
ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1
ENV LOG_LEVEL=INFO

# ===== Runtime detection for GPU availability =====
COPY docker/container-startup.sh /app/
RUN chmod +x /app/container-startup.sh

# ===== Add a healthcheck =====
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
  CMD curl --fail http://localhost:8000/_stcore/health || exit 1

# ===== Run Application =====
ENTRYPOINT ["/app/container-startup.sh"] 