from .server.app import start_server
from .gui.interface import start_gui

__version__ = '0.1.0'

def run(server_host='0.0.0.0', server_port=5000, gui_server_url=None, share_gui=False):
    """
    Run both the server and GUI in one command
    
    Args:
        server_host: Host to run the server on
        server_port: Port to run the server on
        gui_server_url: URL to the server (if None, will use http://{server_host}:{server_port})
        share_gui: Whether to create a shareable link for the GUI
    """
    import threading
    import time
    
    # Start the server in a separate thread
    server_thread = threading.Thread(
        target=start_server, 
        args=(server_host, server_port, None),
        daemon=True
    )
    server_thread.start()
    
    # Wait for the server to start
    time.sleep(2)
    
    # Set the GUI server URL if not provided
    if gui_server_url is None:
        gui_server_url = f"http://{server_host}:{server_port}"
        
    # Start the GUI
    start_gui(gui_server_url, share_gui)
