# threedai: 3D Image AI Generator

A Python package that creates a server running a GUI interface to a neural network, taking images as input and outputting videos and 3D object files (STEP format).

## Installation

### Basic Installation

```bash
pip install threedai
```

### Development Installation

```bash
git clone https://github.com/yourusername/threedai.git
cd threedai
pip install -e ".[dev]"
```

### 3D Model Generation Support

For full 3D model generation support (STEP files), install with:

```bash
pip install -e ".[3d]"
```

Note: This requires OpenCASCADE to be installed on your system. See [PythonOCC installation instructions](https://github.com/tpaviot/pythonocc-core) for more details.

## Usage

### Running the Full Application

The easiest way to run the application is:

```bash
python -m threedai
```

This will start both the server and GUI components.

### Running Server and GUI Separately

Start the server:

```bash
threedai-server --host 0.0.0.0 --port 5000 --model /path/to/model/weights.pth
```

Start the GUI (connecting to the server):

```bash
threedai-gui --server http://localhost:5000 --share
```

The `--share` flag creates a public URL using Gradio sharing.

### Programmatic Usage

```python
import threedai

# Run both server and GUI
threedai.run(server_port=5000, share_gui=True)

# Or run them separately
threedai.start_server(port=5000, model_path='path/to/model.pth')
threedai.start_gui(server_url='http://localhost:5000')
```

## Development

### Project Structure

- `threedai/server/`: Flask server that handles API requests
- `threedai/gui/`: Gradio-based GUI interface
- `threedai/ml/`: Neural network model and inference code
- `threedai/utils/`: Utility functions for visualization and format conversion

### Running Tests

```bash
pytest
```

## License

MIT
```

## Installation and Running Instructions

1. **Install the package**:

```bash
pip install threedai
```

2. **Run the complete application (server + GUI)**:

```bash
python -m threedai
```

3. **Run server and GUI separately**:

Server:
```bash
threedai-server --port 5000
```

GUI:
```bash
threedai-gui --server http://localhost:5000
```

4. **For development setup**:

```bash
git clone https://github.com/yourusername/threedai.git
cd threedai
pip install -e ".[dev,3d]"
