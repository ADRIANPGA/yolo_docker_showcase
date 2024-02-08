

## <div align="center">Documentation</div>

See below for a quickstart installation and usage example, and see the [YOLOv8 Docs](https://docs.ultralytics.com) for full documentation on training, validation, prediction and deployment.

<details open>
<summary>Install</summary>

Pip install the ultralytics package including all [requirements](https://github.com/ultralytics/ultralytics/blob/main/pyproject.toml) in a [**Python>=3.8**](https://www.python.org/) environment with [**PyTorch>=1.8**](https://pytorch.org/get-started/locally/).

[![PyPI version](https://badge.fury.io/py/ultralytics.svg)](https://badge.fury.io/py/ultralytics) [![Downloads](https://static.pepy.tech/badge/ultralytics)](https://pepy.tech/project/ultralytics)

```bash
pip install ultralytics
```

For alternative installation methods including [Conda](https://anaconda.org/conda-forge/ultralytics), [Docker](https://hub.docker.com/r/ultralytics/ultralytics), and Git, please refer to the [Quickstart Guide](https://docs.ultralytics.com/quickstart).

</details>

<details open>
<summary>Usage</summary>

### CLI

YOLOv8 may be used directly in the Command Line Interface (CLI) with a `yolo` command:

```bash
yolo predict model=yolov8n.pt source='https://ultralytics.com/images/bus.jpg'
```

`yolo` can be used for a variety of tasks and modes and accepts additional arguments, i.e. `imgsz=640`. See the YOLOv8 [CLI Docs](https://docs.ultralytics.com/usage/cli) for examples.

### Python
### YOLO Model Convert to ONNX and usage

YOLOv8 may also be used directly in a Python environment, and accepts the same [arguments](https://docs.ultralytics.com/usage/cfg/) as in the CLI example above:


```python

from ultralytics import YOLO

model = YOLO('yolov8n.pt')  
model.export(format='onnx')

print("Model exported to ONNX format successfully.")

# Load the YOLO model
onnx_model = YOLO(onnx_model_path, task='detect')
source = str("bus.jpg")

# Perform object detection
# results image saving
result = onnx_model(source, save=True)

```

See YOLOv8 [Python Docs](https://docs.ultralytics.com/usage/python) for more examples.

</details>

