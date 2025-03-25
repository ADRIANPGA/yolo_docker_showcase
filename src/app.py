import streamlit as st
import logging
import time
import os
import tempfile
from pathlib import Path
import io
import base64

# Configure logging first
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('yolo-app')

# Critical imports with error handling
try:
    import numpy as np
    logger.info("Successfully imported numpy")
except ImportError as e:
    logger.error(f"Failed to import numpy: {e}")
    st.error(f"Critical dependency error: {e}. The application requires numpy to function properly.")
    st.stop()

try:
    import cv2
    logger.info("Successfully imported OpenCV")
except ImportError as e:
    logger.error(f"Failed to import OpenCV: {e}")
    st.error(f"Critical dependency error: {e}. The application requires OpenCV to function properly.")
    st.stop()

try:
    from PIL import Image
    logger.info("Successfully imported PIL")
except ImportError as e:
    logger.error(f"Failed to import PIL: {e}")
    st.error(f"Critical dependency error: {e}. The application requires Pillow to function properly.")
    st.stop()

try:
    from ultralytics import YOLO
    logger.info("Successfully imported YOLO")
except ImportError as e:
    logger.error(f"Failed to import YOLO: {e}")
    st.error(f"Critical dependency error: {e}. The application requires ultralytics to function properly.")
    st.stop()

# Log app startup
logger.info("Starting YOLO Object Detection application")

# Set page configuration
st.set_page_config(
    page_title="[CDS] YOLO Showcase",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="auto"
)
logger.info("Streamlit page configuration set")

# Custom CSS to fix sidebar spacing
st.markdown("""
<style>
    .css-18e3th9 {
        padding-top: 0rem;
    }
    .css-1d391kg {
        padding-top: 0rem;
    }
    .block-container {
        padding-top: 1rem;
    }
    /* Fix sidebar title spacing */
    .css-hxt7ib h1 {
        margin-top: -0.5rem !important;
    }
</style>
""", unsafe_allow_html=True)

# Get the current file's directory
CURRENT_DIR = Path(os.path.dirname(os.path.abspath(__file__)))

# Paths for directories
MODELS_DIR = CURRENT_DIR / "models"
RESOURCES_DIR = CURRENT_DIR / "resources"
SAMPLE_IMAGES_DIR = RESOURCES_DIR / "sample_images"

# Create a temporary directory for the current session
TEMP_DIR = Path(tempfile.mkdtemp())
logger.info(f"Application directories initialized. Temp dir: {TEMP_DIR}")

# Set up sidebar
with st.sidebar:
    logger.debug("Setting up sidebar components")
    st.title("Settings")
    
    # Model selection
    model_option = st.selectbox(
        "Select YOLO Model",
        ["YOLOv8n", "YOLOv8s"],
        index=0
    )
    
    model_mapping = {
        "YOLOv8n": str(MODELS_DIR / "yolov8n.pt"),
        "YOLOv8s": str(MODELS_DIR / "yolov8s.pt")
    }
    
    selected_model = model_mapping[model_option]
    logger.info(f"Model selected: {model_option} -> {selected_model}")
    
    # Confidence threshold
    confidence_threshold = st.slider(
        "Confidence Threshold",
        min_value=0.0,
        max_value=1.0,
        value=0.25,
        step=0.05
    )
    logger.debug(f"Confidence threshold set to: {confidence_threshold}")
    
    # Filter by label
    filter_label = st.text_input("Filter by Class (leave empty for all)")
    if filter_label:
        logger.debug(f"Filter by class applied: {filter_label}")
    
    # Color customization
    box_color = st.color_picker("Bounding Box Color", "#2e7d32")
    st.markdown("---")
    
    # Convert hex to RGB
    box_color_rgb = tuple(int(box_color.lstrip('#')[i:i+2], 16) for i in (0, 2, 4))
    # OpenCV uses BGR format, so reverse the RGB tuple
    box_color_bgr = box_color_rgb[::-1]
    logger.debug(f"Bounding box color set to: {box_color} (BGR: {box_color_bgr})")
    
    # load logo at the bottom
    svg_logo = open(str(RESOURCES_DIR / "cds_logo.svg"), "rb").read()
    svg_logo_base64 = base64.b64encode(svg_logo).decode()
    st.markdown(f"""
    <div style="text-align: center;">
        <img src="data:image/svg+xml;base64,{svg_logo_base64}" width="250">
    </div>
    """, unsafe_allow_html=True)
    logger.debug("Sidebar setup complete")

# Main content
logger.info("Initializing main application content")
st.title("🔍 YOLO Object Detection")

# Create two columns for the main content
col1, col2 = st.columns([1, 1])

with col1:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("Select an Image")
    
    # Create tabs for upload and sample images
    upload_tab, sample_tab = st.tabs(["Upload Image", "Sample Images"])
    
    # Upload tab content
    with upload_tab:
        uploaded_file = st.file_uploader(
            "Upload an image (JPG, JPEG, PNG)", 
            type=["jpg", "jpeg", "png"]
        )
    
    # Sample images tab content
    with sample_tab:
        logger.debug("Loading sample images tab content")
        # Check if sample images exist
        sample_images = []
        if SAMPLE_IMAGES_DIR.exists():
            sample_images = list(SAMPLE_IMAGES_DIR.glob("*.jpg")) + list(SAMPLE_IMAGES_DIR.glob("*.jpeg")) + list(SAMPLE_IMAGES_DIR.glob("*.png"))
            # Limit to top 6 images
            sample_images = sample_images[:6]
            logger.info(f"Found {len(sample_images)} sample images")
        
        # Display sample images if available
        if sample_images:
            # Create a 3-column layout for sample images
            sample_cols = st.columns(3)
            selected_sample = None
            
            for i, img_path in enumerate(sample_images):
                with sample_cols[i % 3]:
                    img = Image.open(img_path)
                    # Resize image while maintaining aspect ratio
                    img_width, img_height = img.size
                    max_height = 150
                    
                    if img_height > max_height:
                        ratio = max_height / img_height
                        new_width = int(img_width * ratio)
                        img = img.resize((new_width, max_height), Image.LANCZOS)
                    
                    st.image(img, caption=img_path.name, use_column_width=True)
                    if st.button(f"Select", key=f"sample_{i}"):
                        selected_sample = img_path
        else:
            st.info("No sample images found. Please upload your own image.")
    
    st.markdown('</div>', unsafe_allow_html=True)

# Initialize the image source variable
image_source = None

# Determine which image to use (uploaded or sample)
if 'selected_sample' in locals() and selected_sample is not None:
    st.success(f"Using sample image: {selected_sample.name}")
    image_source = selected_sample
    logger.info(f"Using sample image: {selected_sample.name}")
elif uploaded_file is not None:
    image_source = uploaded_file
    logger.info(f"Using uploaded image: {uploaded_file.name}")

with col2:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("Detection Results")
    
    # Process the image (whether uploaded or sample)
    if image_source is not None:
        logger.info("Processing image for object detection")
        start_time = time.time()
        
        # Handle both Path and UploadFile objects
        if isinstance(image_source, Path):
            # It's a sample image
            with open(image_source, "rb") as f:
                image_bytes = f.read()
            file_name = image_source.name
            temp_path = str(image_source)
            logger.debug(f"Using sample image path: {temp_path}")
        else:
            # It's an uploaded file
            image_bytes = image_source.getvalue()
            file_name = image_source.name
            # Create a temporary file
            with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp_file:
                tmp_file.write(image_bytes)
                temp_path = tmp_file.name
            logger.debug(f"Created temporary file for uploaded image: {temp_path}")
        
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
            logger.info(f"Loading YOLO model: {model_path}")
            model = YOLO(model_path)
        except Exception as e:
            logger.error(f"Error loading model: {e}")
            st.error(f"Error loading model: {e}")
            st.stop()
        
        # Perform detection
        logger.info("Running object detection")
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
                
                # Draw bounding box and label with the selected color
                cv2.rectangle(output_image, (x1, y1), (x2, y2), box_color_bgr, 2)
                
                # Display label with background using the selected color
                label_text = f"{cls_name}: {confidence:.2f}"
                text_size, _ = cv2.getTextSize(label_text, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 2)
                cv2.rectangle(output_image, (x1, y1 - text_size[1] - 10), (x1 + text_size[0], y1), box_color_bgr, -1)
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
        
        processing_time = time.time() - start_time
        logger.info(f"Detection complete. Found {len(detected_objects)} objects in {processing_time:.2f} seconds")
        
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
                logger.debug(f"Object {i+1}: {obj['label']} (Confidence: {obj['confidence']})")
        else:
            st.info("No objects detected in the image.")
            logger.info("No objects detected in the image")
        
        # Clean up the temporary file if it was created
        if isinstance(image_source, Path) == False and os.path.exists(temp_path):
            os.unlink(temp_path)
            logger.debug(f"Removed temporary file: {temp_path}")
    else:
        # Display a placeholder when no image is uploaded
        st.markdown(
            """
            <div style="text-align: center; padding: 50px; background-color: #f1f8e9; border-radius: 10px;">
                <h3>📤 Select an image from the left panel</h3>
                <p>Detection results will appear here</p>
            </div>
            """, 
            unsafe_allow_html=True
        )
    
    st.markdown('</div>', unsafe_allow_html=True)

logger.info("Application UI rendering complete")


