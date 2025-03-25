#!/bin/bash
set -e

echo "Starting YOLO Object Detection container..."

# Determine if GPU is available
if python -c "import torch; print(f'PyTorch {torch.__version__} is available. CUDA available: {torch.cuda.is_available()}')" 2>/dev/null; then
  if python -c "import torch; exit(0 if torch.cuda.is_available() else 1)" 2>/dev/null; then
    echo "CUDA is available. Running with GPU support."
    export CUDA_VISIBLE_DEVICES=0
  else
    echo "CUDA is not available. Running with CPU only."
    export CUDA_VISIBLE_DEVICES=""
  fi
else
  echo "PyTorch is not installed or not working properly. Running with CPU only."
  export CUDA_VISIBLE_DEVICES=""
fi

# Start the Streamlit application
echo "Starting Streamlit application..."
cd /app && streamlit run src/app.py --server.port=8000 --server.address=0.0.0.0 