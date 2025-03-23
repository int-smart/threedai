from .gui.interface import main as start_gui

__version__ = '0.1.0'

def run(share_gui=False):
    """
    Run the GUI application
    
    Args:
        share_gui: Whether to create a shareable link for the GUI
    """
    # Start the GUI directly
    start_gui(share=share_gui)
