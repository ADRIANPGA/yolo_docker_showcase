import streamlit as st
from pathlib import Path
import os

def set_page_config():
    """Configure the Streamlit page settings"""
    st.set_page_config(
        page_title="YOLO Object Detection",
        page_icon="🔍",
        layout="wide",
        initial_sidebar_state="expanded"
    )

def apply_custom_css():
    """Apply custom CSS styling to the app"""
    st.markdown("""
    <style>
        .main {
            background-color: #f8f9fa;
        }
        .stApp {
            max-width: 1200px;
            margin: 0 auto;
        }
        h1, h2, h3 {
            color: #2e7d32;
        }
        .stButton button {
            background-color: #2e7d32;
            color: white;
        }
        .stButton button:hover {
            background-color: #1b5e20;
            color: white;
        }
        .upload-section {
            padding: 20px;
            border-radius: 10px;
            background-color: white;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            margin-bottom: 20px;
        }
        .results-section {
            padding: 20px;
            border-radius: 10px;
            background-color: white;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }
        .stImage {
            border-radius: 5px;
            border: 1px solid #e0e0e0;
        }
        /* Fix for sidebar positioning */
        [data-testid="stSidebar"] {
            background-color: #f1f8e9;
            min-width: 300px;
            max-width: 300px;
        }
        .download-button {
            background-color: #43a047;
            color: white;
            padding: 10px 20px;
            text-align: center;
            text-decoration: none;
            display: inline-block;
            font-size: 16px;
            margin: 4px 2px;
            border-radius: 5px;
        }
        .sample-images {
            display: flex;
            flex-wrap: wrap;
            gap: 10px;
            margin-top: 10px;
        }
        .sample-image-card {
            border: 1px solid #e0e0e0;
            border-radius: 5px;
            padding: 5px;
            text-align: center;
            cursor: pointer;
            transition: all 0.3s;
        }
        .sample-image-card:hover {
            border-color: #2e7d32;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        }
        .sample-image-card img {
            max-width: 100px;
            max-height: 100px;
            object-fit: cover;
        }
        .sample-images-container {
            background-color: white;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            margin-bottom: 20px;
        }
        .sample-image-item {
            text-align: center;
            margin-bottom: 10px;
        }
        /* Logo size adjustment */
        .sidebar-logo img {
            max-width: 200px;
            margin: 0 auto;
            display: block;
        }
    </style>
    """, unsafe_allow_html=True)

def setup_sidebar(resources_dir):
    """Set up the sidebar with logo and controls"""
    with st.sidebar:
        # Make logo smaller with custom class
        st.markdown('<div class="sidebar-logo">', unsafe_allow_html=True)
        st.image(str(resources_dir / "cds_logo.png"), use_column_width=False)
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.title("YOLO Detection Settings")
        
        # Model selection
        model_option = st.selectbox(
            "Select YOLO Model",
            ["YOLOv8n", "YOLOv8s", "YOLOv8m"],
            index=0
        )
        
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
        
        return model_option, confidence_threshold, filter_label, box_color

def display_upload_section():
    """Display the upload section"""
    st.markdown("""
    <div class="upload-section">
        <h3>Upload an Image</h3>
        <p>Select an image to perform object detection. The system will identify objects in the image and display bounding boxes around them.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Regular file uploader
    return st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

def display_sample_images(sample_images_dir):
    """Display sample images for selection"""
    st.markdown("""
    <div class="sample-images-container">
        <h3>Sample Test Images</h3>
        <p>Select one of our sample images to perform object detection.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Check if sample images exist
    sample_images = []
    if sample_images_dir.exists():
        sample_images = list(sample_images_dir.glob("*.jpg")) + list(sample_images_dir.glob("*.jpeg")) + list(sample_images_dir.glob("*.png"))
        # Limit to top 5 images
        sample_images = sample_images[:5]
    
    # Display sample images if available
    selected_sample = None
    if sample_images:
        # Create a 3-column layout for sample images
        cols = st.columns(3)
        
        for i, img_path in enumerate(sample_images):
            with cols[i % 3]:
                st.markdown(f"<div class='sample-image-item'>", unsafe_allow_html=True)
                st.image(str(img_path), width=200, caption=img_path.name)
                if st.button(f"Use this image", key=f"sample_{i}"):
                    selected_sample = img_path
                st.markdown("</div>", unsafe_allow_html=True)
        
        if selected_sample:
            st.success(f"Using sample image: {selected_sample.name}")
    else:
        st.info("No sample images found. Please upload your own image.")
    
    return selected_sample

def display_placeholder():
    """Display a placeholder when no image is uploaded"""
    st.markdown("""
    <div style="text-align: center; padding: 50px; background-color: #f1f8e9; border-radius: 10px;">
        <h3>📤 Upload an image or select a sample image to get started</h3>
        <p>Supported formats: JPG, JPEG, PNG</p>
    </div>
    """, unsafe_allow_html=True)

def display_results_section():
    """Display the results section header"""
    st.markdown("""
    <div class="results-section">
        <h3>Detection Results</h3>
    </div>
    """, unsafe_allow_html=True)

def display_footer():
    """Display the footer"""
    st.markdown("""
    <div style="text-align: center; margin-top: 30px; padding: 20px; color: #666;">
        <p>YOLO Object Detection System with Streamlit UI</p>
    </div>
    """, unsafe_allow_html=True)

def display_detection_results(original_image_rgb, output_image_rgb, detected_objects, file_name):
    """Display detection results with side-by-side comparison"""
    display_results_section()
    
    # Create columns for side-by-side comparison
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Original Image")
        st.image(original_image_rgb, use_column_width=True)
    
    with col2:
        st.subheader("Detected Objects")
        st.image(output_image_rgb, use_column_width=True)
    
    # Show detection details
    if detected_objects:
        st.markdown(f"### Detected {len(detected_objects)} objects:")
        
        for i, obj in enumerate(detected_objects):
            st.markdown(
                f"""
                <div style="padding: 10px; margin: 5px 0; background-color: #f1f8e9; border-radius: 5px;">
                    <strong>Object {i+1}:</strong> {obj['label']} (Confidence: {obj['confidence']})
                </div>
                """, 
                unsafe_allow_html=True
            )
    else:
        st.info("No objects detected in the image.") 