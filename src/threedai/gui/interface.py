import os
import gradio as gr
from ..ml.hunyuan import Hunyuan

# Initialize the integration
OUTPUT_DIR = os.environ.get("OUTPUT_DIR", "outputs")

hunyuan = Hunyuan()  # Initialize Hunyuan model

def process_inputs(image, prompt, model_choice="hunyuan"):
    """Process inputs and generate 3D model"""
    # Save the input image temporarily
    temp_image_path = os.path.join(OUTPUT_DIR, "temp_input.jpg")
    image.save(temp_image_path)
    
    # Generate 3D model based on selected model
    if model_choice == "trellis":
        return ""
    else:
        output = hunyuan(temp_image_path, prompt, generate_texture=True)
        glb_path = output.export(output, "glb", os.path.join(OUTPUT_DIR, "output.ply"))
  
    # Return paths to the generated files
    return glb_path

# Create Gradio interface
with gr.Blocks(title="3D Generation") as app:
    gr.Markdown("# 3D Generation from Images and Text")
    
    with gr.Row():
        with gr.Column():
            input_image = gr.Image(label="Input Image", type="pil")
            text_prompt = gr.Textbox(label="Text Prompt (Optional)")
            generate_btn = gr.Button("Generate 3D Model")
        
        with gr.Column():
            video_output = gr.Video(label="Preview")
            model_output = gr.File(label="3D Model (PLY)")
    
    generate_btn.click(
        fn=process_inputs,
        inputs=[input_image, text_prompt],
        outputs=[video_output, model_output]
    )

def main():
    app.launch()

if __name__ == "__main__":
    main()
