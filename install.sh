#!/bin/bash

# Check if model argument is provided
if [ $# -eq 0 ]; then
    echo "Please provide a model argument (e.g., hunyuan)"
    exit 1
fi

MODEL=$1

# Create and activate Python virtual environment
python -m venv threedai_env
source threedai_env/bin/activate

# Install base dependencies
pip install torch torchvision

# Install your package
pip install -e .

# Install specific model based on argument
if [ "$MODEL" = "hunyuan" ]; then
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
elif [ "$MODEL" = "trellis" ]; then
    git clone --recurse-submodules https://github.com/microsoft/TRELLIS.git
    cd TRELLIS
    pip install torch==2.4.0 torchvision==0.19.0 --extra-index-url https://download.pytorch.org/whl/cu118
    . ./setup.sh --basic --xformers --diffoctreerast --spconv --mipgaussian --kaolin --nvdiffrast
    pip install xformers==0.0.27.post2
    pip install kaolin==0.17.0 -f https://nvidia-kaolin.s3.us-east-2.amazonaws.com/torch-2.4.0_cu118.html
fi

echo "Installation complete!"