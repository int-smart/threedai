# ThreeDAI

Generate 3D models from images and text using TRELLIS.

## Installation

```bash
pip install threedai
```

## Usage

```bash
# Run the GUI application
python -m threedai
```

Or use programmatically:

```python
from threedai.direct_integration import TrellisIntegration

trellis = TrellisIntegration("path/to/model.pt")
result = trellis.generate_3d_from_image("input.jpg", "a red chair")
print(f"3D model saved to: {result['gaussian_path']}")
```
