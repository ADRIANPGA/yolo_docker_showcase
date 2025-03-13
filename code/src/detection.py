import cv2
import numpy as np
import os
import tempfile
from pathlib import Path
from PIL import Image
import io
import base64
from ultralytics import YOLO
import streamlit as st

def load_model(model_path):
    """Load the YOLO model"""
    try:
        model = YOLO(model_path)
        return model
    except Exception as e:
        st.error(f"Error loading model: {e}")
        return None

def get_model_path(model_option, models_dir):
    """Get the path to the selected model"""
    model_mapping = {
        "YOLOv8n": str(models_dir / "yolov8n.pt"),
        "YOLOv8s": str(models_dir / "yolov8s.pt"),
        "YOLOv8m": "yolov8m.pt"  # This will use the default path
    }
    
    selected_model = model_mapping[model_option]
    
    # Check if ONNX model exists, if not use PT model
    model_base_name = os.path.splitext(os.path.basename(selected_model))[0]
    onnx_model_path = models_dir / f"{model_base_name}.onnx"
    
    if onnx_model_path.exists():
        return str(onnx_model_path)
    else:
        return selected_model

def prepare_image(uploaded_file):
    """Prepare the image for detection"""
    # Handle both Path and UploadFile objects
    if isinstance(uploaded_file, Path):
        # It's a sample image
        with open(uploaded_file, "rb") as f:
            image_bytes = f.read()
        file_name = uploaded_file.name
        temp_path = str(uploaded_file)
    else:
        # It's an uploaded file
        image_bytes = uploaded_file.getvalue()
        file_name = uploaded_file.name
        # Create a temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp_file:
            tmp_file.write(image_bytes)
            temp_path = tmp_file.name
    
    # Read the image for display
    original_image = cv2.imread(temp_path)
    original_image_rgb = cv2.cvtColor(original_image, cv2.COLOR_BGR2RGB)
    
    return original_image, original_image_rgb, temp_path, file_name

def detect_objects(model, image_path, confidence_threshold, filter_label, box_color_rgb):
    """Perform object detection on the image"""
    # Perform detection
    results = model(image_path, conf=confidence_threshold)
    
    # Read the original image
    original_image = cv2.imread(image_path)
    
    # Process results
    detected_objects = []
    
    # Create a copy of the original image for drawing
    output_image = original_image.copy()
    
    for r in results:
        for box, cls_id, conf in zip(r.boxes.xyxy, r.boxes.cls, r.boxes.conf):
            x1, y1, x2, y2 = map(int, box.tolist())
            cls_name = r.names[int(cls_id.item())]
            confidence = float(conf.item())
            
            # Skip if filtering by label and this doesn't match
            if filter_label and filter_label.lower() != cls_name.lower():
                continue
                
            detected_objects.append({
                "label": cls_name,
                "confidence": round(confidence, 2),
                "box": [x1, y1, x2, y2]
            })
            
            # Draw bounding box and label
            cv2.rectangle(output_image, (x1, y1), (x2, y2), box_color_rgb, 2)
            
            # Display label with background
            label_text = f"{cls_name}: {confidence:.2f}"
            text_size, _ = cv2.getTextSize(label_text, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 2)
            cv2.rectangle(output_image, (x1, y1 - text_size[1] - 10), (x1 + text_size[0], y1), box_color_rgb, -1)
            cv2.putText(output_image, label_text, (x1, y1 - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
    
    # Convert output image to RGB for display
    output_image_rgb = cv2.cvtColor(output_image, cv2.COLOR_BGR2RGB)
    
    return detected_objects, output_image_rgb

def create_download_button(output_image_rgb, file_name):
    """Create a download button for the processed image"""
    result_img = Image.fromarray(output_image_rgb)
    buf = io.BytesIO()
    result_img.save(buf, format="JPEG")
    byte_im = buf.getvalue()
    
    return st.download_button(
        label="Download Processed Image",
        data=byte_im,
        file_name=f"detected_{file_name}",
        mime="image/jpeg",
    )

def cleanup_temp_file(temp_path, is_sample_image):
    """Clean up temporary files"""
    if not is_sample_image and os.path.exists(temp_path):
        os.unlink(temp_path) 