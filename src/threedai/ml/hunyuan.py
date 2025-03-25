from hy3dgen.texgen import Hunyuan3DPaintPipeline
from hy3dgen.shapegen import Hunyuan3DDiTFlowMatchingPipeline

class Hunyuan:
    def __init__(self):
        # Load a pipeline from a model folder or a Hugging Face model hub.
        self.flow_pipeline = Hunyuan3DDiTFlowMatchingPipeline.from_pretrained('tencent/Hunyuan3D-2')
        self.paint_pipeline = Hunyuan3DPaintPipeline.from_pretrained('tencent/Hunyuan3D-2')

    def __call__(self, image_path, prompt, generate_texture, **kwds):
        self.flow_pipeline.cuda()
        self.paint_pipeline.cuda()

        # Run the pipeline
        output = self.flow_pipeline(
            image=image_path
        )

        if generate_texture:
            output = self.paint_pipeline(output, image=image_path)

        return output

    def export(self, mesh, type, output_path):
        if type == "glb":
            mesh.export(output_path)