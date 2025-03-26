#!/bin/bash

# Create and activate Python virtual environment
python -m venv threedai_env
source threedai_env/bin/activate

# Install base dependencies
pip install torch torchvision

# Install your package
pip install -e .

# Install Hunyuan3D-2
git clone https://github.com/Tencent/Hunyuan3D-2.git
cd Hunyuan3D-2
pip install -r requirements.txt
pip install -e .

# Install texture components
cd hy3dgen/texgen/custom_rasterizer
python setup.py install
cd ../../..

cd hy3dgen/texgen/differentiable_renderer
python setup.py install
cd ../../..

echo "Installation complete!"