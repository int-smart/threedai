from setuptools import setup, find_packages

setup(
    name="threedai",
    version="0.1.0",
    package_dir={"": "src"},  # Tell setuptools packages are under src
    packages=find_packages(where="src"),  # Find packages in src directory
    include_package_data=True,
    install_requires=[
        "flask>=2.0.0",
        "flask-cors>=3.0.10",
        "gradio>=3.0.0",
        "torch>=1.9.0",
        "torchvision>=0.10.0",
        "numpy>=1.19.0",
        "pillow>=8.0.0",
        "requests>=2.25.0",
        "opencv-python>=4.5.0",
        "matplotlib>=3.4.0",
    ],
    extras_require={
        "dev": [
            "pytest>=6.0.0",
            "black>=21.5b2",
            "flake8>=3.9.0",
        ],
        "3d": [
            "PythonOCC-Core>=7.4.0",  # For STEP file generation
        ]
    },
    entry_points={
        "console_scripts": [
            "threedai-server=threedai.server.app:start_server",
            "threedai-gui=threedai.gui.interface:start_gui",
        ],
    },
)