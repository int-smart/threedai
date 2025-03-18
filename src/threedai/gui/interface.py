import gradio as gr
import requests
import tempfile
import os
from pathlib import Path

class GUI:
    def __init__(self, server_url="http://localhost:5000"):
        self.server_url = server_url
        
    def process_image(self, image):
        # Convert PIL image to file
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.jpg')
        image_path = temp_file.name
        image.save(image_path)
        
        # Send to server
        with open(image_path, 'rb') as img:
            response = requests.post(
                f"{self.server_url}/api/process",
                files={"image": img}
            )
        
        os.unlink(image_path)  # Clean up temp file
        
        if response.status_code != 200:
            return "Error processing image", None, None
            
        data = response.json()
        
        # Get video
        video_response = requests.get(f"{self.server_url}{data['video_url']}")
        video_path = tempfile.NamedTemporaryFile(delete=False, suffix='.mp4').name
        with open(video_path, 'wb') as f:
            f.write(video_response.content)
        
        # Get 3D model
        model_response = requests.get(f"{self.server_url}{data['model3d_url']}")
        model_path = tempfile.NamedTemporaryFile(delete=False, suffix='.step').name
        with open(model_path, 'wb') as f:
            f.write(model_response.content)
            
        return "Processing complete!", video_path, model_path
    
    def launch(self, share=False):
        with gr.Blocks(title="3D Image AI") as demo:
            gr.Markdown("# 3D Image AI Generator")
            gr.Markdown("Upload an image to generate a video and 3D model")
            
            with gr.Row():
                with gr.Column():
                    input_image = gr.Image(label="Input Image")
                    submit_btn = gr.Button("Generate 3D Assets")
                
                with gr.Column():
                    status = gr.Textbox(label="Status")
                    output_video = gr.Video(label="Output Video")
                    model_download = gr.File(label="Download 3D Model (STEP file)")
            
            submit_btn.click(
                fn=self.process_image,
                inputs=[input_image],
                outputs=[status, output_video, model_download]
            )
        
        demo.launch(share=share)

def start_gui(server_url="http://localhost:5000", share=False):
    gui = GUI(server_url)
    gui.launch(share=share)

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Launch the 3D Image AI GUI")
    parser.add_argument("--server", default="http://localhost:5000", help="URL of the server")
    parser.add_argument("--share", action="store_true", help="Create a shareable link")
    args = parser.parse_args()
    
    start_gui(args.server, args.share)
