import streamlit as st
import os
from pathlib import Path

# Import modules
import ui
import utils
import detection

def main():
    """Main entry point for the application"""
    # Set up page configuration
    ui.set_page_config()
    
    # Apply custom CSS
    ui.apply_custom_css()
    
    # Get app directories
    directories = utils.get_app_directories()
    utils.ensure_directories_exist(directories)
    
    # Setup sidebar and get user settings
    model_option, confidence_threshold, filter_label, box_color = ui.setup_sidebar(
        directories["resources_dir"]
    )
    
    # Convert hex color to RGB
    box_color_rgb = utils.hex_to_rgb(box_color)
    
    # Main content
    st.title("🔍 YOLO Object Detection")
    
    # Create tabs for upload and sample images
    tab1, tab2 = st.tabs(["Upload Image", "Sample Images"])
    
    # Initialize uploaded_file to None
    uploaded_file = None
    
    with tab1:
        # Display upload section
        uploaded_file = ui.display_upload_section()
    
    with tab2:
        # Display sample images
        selected_sample = ui.display_sample_images(directories["sample_images_dir"])
        if selected_sample:
            uploaded_file = selected_sample
    
    # Process the image (whether uploaded or sample)
    if uploaded_file is not None:
        # Get model path
        model_path = detection.get_model_path(model_option, directories["models_dir"])
        
        # Load model
        model = detection.load_model(model_path)
        if model is None:
            st.stop()
        
        # Prepare image
        original_image, original_image_rgb, temp_path, file_name = detection.prepare_image(uploaded_file)
        
        # Detect objects
        detected_objects, output_image_rgb = detection.detect_objects(
            model, temp_path, confidence_threshold, filter_label, box_color_rgb
        )
        
        # Display detection results
        ui.display_detection_results(original_image_rgb, output_image_rgb, detected_objects, file_name)
        
        # Create download button
        detection.create_download_button(output_image_rgb, file_name)
        
        # Clean up temporary file
        detection.cleanup_temp_file(temp_path, isinstance(uploaded_file, Path))
    else:
        # Display placeholder
        ui.display_placeholder()
    
    # Display footer
    ui.display_footer()

if __name__ == "__main__":
    main() 