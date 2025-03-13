import streamlit as st
import cv2
import numpy as np
import os
import tempfile
from pathlib import Path
from PIL import Image
import io
import base64
from ultralytics import YOLO

# Set page configuration
st.set_page_config(
    page_title="YOLO Showcase",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Get the current file's directory
CURRENT_DIR = Path(os.path.dirname(os.path.abspath(__file__)))

# Paths for directories
MODELS_DIR = CURRENT_DIR / "models"
RESOURCES_DIR = CURRENT_DIR / "resources"
SAMPLE_IMAGES_DIR = RESOURCES_DIR / "sample_images"

# Create a temporary directory for the current session
TEMP_DIR = Path(tempfile.mkdtemp())

# Set up sidebar
with st.sidebar:
    st.image(str(RESOURCES_DIR / "cds_logo.png"), use_column_width=True)
    st.title("Detection Settings")
    
    # Model selection
    model_option = st.selectbox(
        "Select YOLO Model",
        ["YOLOv8n", "YOLOv8s", "YOLOv8m"],
        index=0
    )
    
    model_mapping = {
        "YOLOv8n": str(MODELS_DIR / "yolov8n.pt"),
        "YOLOv8s": str(MODELS_DIR / "yolov8s.pt"),
        "YOLOv8m": "yolov8m.pt"  # This will use the default path
    }
    
    selected_model = model_mapping[model_option]
    
    # Confidence threshold
    confidence_threshold = st.slider(
        "Confidence Threshold",
        min_value=0.0,
        max_value=1.0,
        value=0.25,
        step=0.05
    )
    
    # Filter by label
    filter_label = st.text_input("Filter by Class (leave empty for all)")
    
    # Color customization
    box_color = st.color_picker("Bounding Box Color", "#2e7d32")
    # Convert hex to RGB
    box_color_rgb = tuple(int(box_color.lstrip('#')[i:i+2], 16) for i in (0, 2, 4))
    
    st.markdown("---")
    st.markdown("### Navigation Tips:")
    st.markdown("- Adjust detection settings above\n- Upload images or choose samples\n- Customize colors and filters")

# Main content
st.title("🔍 YOLO Object Detection")

# Create two columns for the main content
col1, col2 = st.columns([1, 1])

with col1:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("Upload Image")
    st.markdown('<div class="upload-area">', unsafe_allow_html=True)
    st.markdown("### Drag & Drop Image Here")
    st.markdown("Supported formats: JPG, JPEG, PNG")
    uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"], label_visibility="collapsed")
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Sample images section
    st.subheader("Or Choose a Sample Image")
    
    # Check if sample images exist
    sample_images = []
    if SAMPLE_IMAGES_DIR.exists():
        sample_images = list(SAMPLE_IMAGES_DIR.glob("*.jpg")) + list(SAMPLE_IMAGES_DIR.glob("*.jpeg")) + list(SAMPLE_IMAGES_DIR.glob("*.png"))
        # Limit to top 6 images
        sample_images = sample_images[:6]
    
    # Display sample images if available
    if sample_images:
        st.markdown('<div class="sample-grid">', unsafe_allow_html=True)
        
        # Create a 3-column layout for sample images
        sample_cols = st.columns(3)
        selected_sample = None
        
        for i, img_path in enumerate(sample_images):
            with sample_cols[i % 3]:
                st.markdown('<div class="sample-image-container">', unsafe_allow_html=True)
                img = Image.open(img_path)
                # Resize image while maintaining aspect ratio
                img_width, img_height = img.size
                max_height = 150
                
                if img_height > max_height:
                    ratio = max_height / img_height
                    new_width = int(img_width * ratio)
                    img = img.resize((new_width, max_height), Image.LANCZOS)
                
                st.image(img, use_column_width=True)
                st.markdown(f'<div class="sample-image-caption">{img_path.name}</div>', unsafe_allow_html=True)
                if st.button(f"Use this", key=f"sample_{i}"):
                    selected_sample = img_path
                st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        if selected_sample:
            st.success(f"Using sample image: {selected_sample.name}")
            # Set as the current file (will be processed below)
            uploaded_file = selected_sample
    else:
        st.info("No sample images found. Please upload your own image.")
    
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("Detection Results")
    
    # Process the image (whether uploaded or sample)
    if uploaded_file is not None:
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
        
        # Check if ONNX model exists, if not use PT model
        model_base_name = os.path.splitext(os.path.basename(selected_model))[0]
        onnx_model_path = MODELS_DIR / f"{model_base_name}.onnx"
        
        if onnx_model_path.exists():
            model_path = str(onnx_model_path)
        else:
            model_path = selected_model
        
        # Load YOLO model
        try:
            model = YOLO(model_path)
        except Exception as e:
            st.error(f"Error loading model: {e}")
            st.stop()
        
        # Perform detection
        results = model(temp_path, conf=confidence_threshold)
        
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
        
        # Display original and processed images
        result_cols = st.columns(2)
        
        with result_cols[0]:
            st.markdown("**Original Image**")
            st.image(original_image_rgb, use_column_width=True)
        
        with result_cols[1]:
            st.markdown("**Detected Objects**")
            st.image(output_image_rgb, use_column_width=True)
        
        # Create download button for the result image
        result_img = Image.fromarray(output_image_rgb)
        buf = io.BytesIO()
        result_img.save(buf, format="JPEG")
        byte_im = buf.getvalue()
        
        st.download_button(
            label="Download Processed Image",
            data=byte_im,
            file_name=f"detected_{file_name}",
            mime="image/jpeg",
        )
        
        # Show detection details
        if detected_objects:
            st.markdown(f"### Detected {len(detected_objects)} objects:")
            
            for i, obj in enumerate(detected_objects):
                st.markdown(
                    f"""
                    <div class="detection-item">
                        <strong>Object {i+1}:</strong> {obj['label']} (Confidence: {obj['confidence']})
                    </div>
                    """, 
                    unsafe_allow_html=True
                )
        else:
            st.info("No objects detected in the image.")
        
        # Clean up the temporary file if it was created
        if isinstance(uploaded_file, Path) == False and os.path.exists(temp_path):
            os.unlink(temp_path)
    else:
        # Display a placeholder when no image is uploaded
        st.markdown(
            """
            <div style="text-align: center; padding: 50px; background-color: #f1f8e9; border-radius: 10px;">
                <h3>📤 Upload an image or select a sample image</h3>
                <p>Detection results will appear here</p>
            </div>
            """, 
            unsafe_allow_html=True
        )
    
    st.markdown('</div>', unsafe_allow_html=True)


