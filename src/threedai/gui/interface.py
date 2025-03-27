import os
import gradio as gr
import configparser
import imageio
# from ..ml.hunyuan import Hunyuan

# Initialize the integration
OUTPUT_DIR = os.environ.get("OUTPUT_DIR", "outputs")
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Determine which model is installed
def get_installed_model():
    config_path = os.path.expanduser("~/.threedai/config.ini")
    if os.path.exists(config_path):
        config = configparser.ConfigParser()
        try:
            # For simple key=value format without section headers
            with open(config_path, 'r') as f:
                config_string = '[DEFAULT]\n' + f.read()
            config.read_string(config_string)
            return config['DEFAULT'].get('model', 'hunyuan')
        except Exception as e:
            print(f"Error reading config: {e}")
    return "hunyuan"  # Default if config doesn't exist or can't be read

# hunyuan = Hunyuan()  # Initialize Hunyuan model
# Get the installed model
INSTALLED_MODEL = get_installed_model()
def process_inputs(image_path, prompt, model_choice=INSTALLED_MODEL):
    """Process inputs and generate 3D model"""
    glb_path = None
    print(f"Using {INSTALLED_MODEL}")
    # Generate 3D model based on selected model
    if model_choice == "trellis":
        from PIL import Image
        from trellis.pipelines import TrellisImageTo3DPipeline
        from trellis.utils import render_utils, postprocessing_utils
        os.environ['ATTN_BACKEND'] = 'xformers'

        # Load a pipeline from a model folder or a Hugging Face model hub.
        pipeline = TrellisImageTo3DPipeline.from_pretrained("JeffreyXiang/TRELLIS-image-large")
        pipeline.cuda()

        # Load an image
        print("image_path is ", image_path)
        if isinstance(image_path, Image.Image):
            image = image_path
        else:
            image = Image.open(image_path)
        # Run the pipeline
        outputs = pipeline.run(
            image,
            seed=1,
        )

        # Generate video output
        video = render_utils.render_video(outputs['gaussian'][0])['color']
        video_path = os.path.join(OUTPUT_DIR, "output_video.mp4")
        imageio.mimsave(video_path, video, fps=30)

        # Generate GLB model
        glb = postprocessing_utils.to_glb(
            outputs['gaussian'][0],
            outputs['mesh'][0],
            simplify=0.95,
            texture_size=1024,
        )
        glb_path = os.path.join(OUTPUT_DIR, "output.glb")
        glb.export(glb_path)

        # Return paths and status
        return video_path, glb_path, "Generation completed successfully!"    # else:
    #     output = hunyuan(image_path, prompt, generate_texture=True)
    #     glb_path = hunyuan.export(output, "glb", os.path.join(OUTPUT_DIR, "output.ply"))
  
    # Return paths to the generated files
    return ""

# Get the path to the CSS file
def get_css_path():
    try:
        # When installed as a package
        css_path = pkg_resources.resource_filename('threedai', 'gui/assets/style.css')
    except:
        # When running from source
        current_dir = os.path.dirname(os.path.abspath(__file__))
        css_path = os.path.join(current_dir, 'assets', 'style.css')
    
    if not os.path.exists(css_path):
        # Fallback to a relative path
        css_path = os.path.join(os.path.dirname(__file__), 'assets', 'style.css')
    
    return css_path

def load_css():
    css_path = get_css_path()
    if os.path.exists(css_path):
        with open(css_path, 'r') as f:
            return f.read()
    else:
        print(f"Warning: CSS file not found at {css_path}")
        return ""


# Load CSS from file
custom_css = load_css()

with gr.Blocks(title="3D Generation", css=custom_css) as app:
    with gr.Column(elem_classes="container"):
        # Header
        with gr.Column(elem_classes="header"):
            gr.Markdown("# 3D Generation from Images and Text")
            gr.Markdown("Transform your 2D images into detailed 3D models with AI")
        
        # Main content
        with gr.Row(elem_classes="content-row"):
            # Input column
            with gr.Column(elem_classes="content-column"):
                with gr.Group():
                    gr.Markdown("### Input")
                    input_image = gr.Image(
                        label="Upload Image", 
                        type="pil",
                        elem_id="input-image",
                        height=300
                    )
                    
                    # Changed Radio to Dropdown
                    model_choice = gr.Dropdown(
                        choices=["hunyuan", "trellis"],
                        value="hunyuan",
                        label="Select 3D Generation Model",
                        info="Choose the AI model for 3D generation"
                    )
                    
                    text_prompt = gr.Textbox(
                        label="Text Prompt (Optional)",
                        placeholder="Describe additional details for the 3D model...",
                        lines=3
                    )
                    
                    generate_btn = gr.Button(
                        "Generate 3D Model", 
                        variant="primary",
                        elem_classes="generate-btn"
                    )
            
            # Output column
            with gr.Column(elem_classes="content-column"):
                with gr.Group(elem_classes="output-container"):
                    gr.Markdown("### Output")
                    with gr.Tab("3D Preview"):
                        # Force the video output to a certain height for consistency
                        video_output = gr.Video(
                            label="3D Model Preview", 
                            height=300
                        )
                    with gr.Tab("Download"):
                        # File display usually doesn’t need much space, 
                        # but giving it a height helps keep the tabs consistent
                        model_output = gr.File(
                            label="Download 3D Model (PLY)",
                            file_count="single"
                        )
                    
                    status_output = gr.Textbox(
                        label="Status",
                        placeholder="Generation status will appear here...",
                        interactive=False
                    )
        
        # Examples section
        with gr.Column():
            gr.Markdown("### Examples")
            example_images = [
                ["data/example1.jpg", "A red chair with wooden legs"],
                ["data/example2.jpg", "A modern desk lamp"],
                ["data/example3.jpg", "A ceramic vase with floral pattern"]
            ]
            gr.Examples(
                examples=example_images,
                inputs=[input_image, text_prompt],
            )
        
        # Footer
        with gr.Column(elem_classes="footer"):
            gr.Markdown("Powered by ThreeDAI | [GitHub](https://github.com/int-smart/threedai)")
    
    # Event handlers
    generate_btn.click(
        fn=process_inputs,
        inputs=[input_image, text_prompt, model_choice],
        outputs=[video_output, model_output, status_output]
    )

def main(share=True):
    app.launch(share=share)

if __name__ == "__main__":
    main()
