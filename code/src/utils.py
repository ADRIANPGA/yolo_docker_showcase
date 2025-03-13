import os
import tempfile
from pathlib import Path

def get_app_directories():
    """Get the directories used by the app"""
    # Get the current file's directory
    current_dir = Path(os.path.dirname(os.path.abspath(__file__)))
    
    # Paths for directories
    models_dir = current_dir / "models"
    resources_dir = current_dir / "resources"
    sample_images_dir = resources_dir / "sample_images"
    
    # Create a temporary directory for the current session
    temp_dir = Path(tempfile.mkdtemp())
    
    return {
        "current_dir": current_dir,
        "models_dir": models_dir,
        "resources_dir": resources_dir,
        "sample_images_dir": sample_images_dir,
        "temp_dir": temp_dir
    }

def hex_to_rgb(hex_color):
    """Convert hex color to RGB tuple"""
    # Convert hex to RGB
    return tuple(int(hex_color.lstrip('#')[i:i+2], 16) for i in (0, 2, 4))

def ensure_directories_exist(directories):
    """Ensure that all required directories exist"""
    for dir_name, dir_path in directories.items():
        if not dir_path.exists() and dir_name != "temp_dir":
            dir_path.mkdir(parents=True, exist_ok=True) 