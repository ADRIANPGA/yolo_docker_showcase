# Resources Directory

This directory contains static resources for the YOLO Object Detection application.

## Contents

- `sample_images/`: Sample images for testing object detection
- `icons/`: UI icons and graphics
- `css/`: Custom CSS files
- `js/`: JavaScript files for enhanced UI functionality

## Usage

Place any static assets that your application needs in this directory. The directory is mounted as a volume in the Docker container, so any changes you make here will be immediately available to the application.

## Sample Images

The Docker container comes pre-loaded with some sample images from the Ultralytics repository:
- `zidane.jpg`: A sample image of a person
- `bus.jpg`: A sample image of a bus

You can add your own sample images to this directory for testing purposes. 