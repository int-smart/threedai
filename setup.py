from setuptools import setup, find_packages

setup(
    name="threedai",
    version="0.1.0",
    package_dir={"": "src"},  # Tell setuptools packages are under src
    packages=find_packages(where="src"),  # Find packages in src directory
    include_package_data=True,
    package_data={
        "threedai": ["gui/assets/*.css"],
    },
    install_requires=[
        "gradio>=3.0.0",
        "torch",
        "torchvision",
        "numpy>=1.19.0",
        "pillow>=8.0.0",
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
            "threedai-gui=threedai.gui.interface:main",
        ],
    },
)