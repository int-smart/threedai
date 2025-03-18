import numpy as np
import matplotlib.pyplot as plt
import cv2
from PIL import Image
import io

def create_thumbnail(video_path, output_path=None):
    """
    Create a thumbnail from a video file
    
    Args:
        video_path: Path to the video file
        output_path: Path to save the thumbnail (if None, returns the image)
        
    Returns:
        PIL Image if output_path is None, otherwise None
    """
    cap = cv2.VideoCapture(str(video_path))
    
    # Take the middle frame
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    cap.set(cv2.CAP_PROP_POS_FRAMES, total_frames // 2)
    
    ret, frame = cap.read()
    cap.release()
    
    if not ret:
        raise Exception(f"Could not read frame from {video_path}")
    
    # Convert BGR to RGB
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    image = Image.fromarray(frame)
    
    if output_path:
        image.save(output_path)
        return None
    
    return image

def create_3d_preview(model_path, output_path=None):
    """
    Create a preview image of a 3D model
    
    Args:
        model_path: Path to the 3D model file (STEP format)
        output_path: Path to save the preview image (if None, returns the image)
        
    Returns:
        PIL Image if output_path is None, otherwise None
    """
    try:
        from OCC.Display.SimpleGui import init_display
        from OCC.Core.STEPControl import STEPControl_Reader
        from OCC.Core.IFSelect import IFSelect_RetDone
        from OCC.Core.Graphic3d import Graphic3d_NOM_JADE
        import matplotlib.pyplot as plt
        
        # Read the STEP file
        step_reader = STEPControl_Reader()
        status = step_reader.ReadFile(str(model_path))
        
        if status != IFSelect_RetDone:
            raise Exception(f"Error reading STEP file {model_path}")
            
        step_reader.TransferRoot()
        shape = step_reader.Shape()
        
        # Create a display
        display, start_display, add_menu, add_function_to_menu = init_display(size=(800, 600))
        display.DisplayShape(shape, material=Graphic3d_NOM_JADE, update=True)
        display.View_Iso()
        display.FitAll()
        
        # Capture the image
        image_data = display.GetImageData(800, 600)
        display.Repaint()
        
        # Convert to PIL Image
        image = Image.frombytes("RGB", (800, 600), image_data)
        
        if output_path:
            image.save(output_path)
            return None
            
        return image
        
    except ImportError:
        # If OCC is not available, create a dummy image
        fig = plt.figure(figsize=(8, 6))
        ax = fig.add_subplot(111)
        ax.text(0.5, 0.5, "3D Preview\n(Install PythonOCC for rendering)", 
                ha='center', va='center', fontsize=14)
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.axis('off')
        
        if output_path:
            plt.savefig(output_path)
            plt.close(fig)
            return None
            
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        plt.close(fig)
        buf.seek(0)
        return Image.open(buf)
