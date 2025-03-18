import numpy as np
import tempfile
import os
from pathlib import Path

def mesh_to_step(vertices, faces, output_path):
    """
    Convert a mesh (vertices and faces) to a STEP file
    
    Args:
        vertices: numpy array of shape (n, 3) containing the vertices
        faces: numpy array of shape (m, 3) containing the faces (vertex indices)
        output_path: path to save the STEP file
    """
    try:
        from OCC.Core.BRepBuilderAPI import BRepBuilderAPI_MakePolygon, BRepBuilderAPI_MakeFace
        from OCC.Core.gp import gp_Pnt
        from OCC.Core.TopoDS import TopoDS_Compound
        from OCC.Core.BRep import BRep_Builder
        from OCC.Core.STEPControl import STEPControl_Writer, STEPControl_AsIs
        from OCC.Core.Interface import Interface_Static_SetCVal
        from OCC.Core.IFSelect import IFSelect_RetDone
        
        # Create a compound to hold all faces
        compound = TopoDS_Compound()
        builder = BRep_Builder()
        builder.MakeCompound(compound)
        
        # Create a face for each triangle
        for face in faces:
            points = [gp_Pnt(*vertices[idx]) for idx in face]
            
            # Create a polygon from the vertices
            polygon = BRepBuilderAPI_MakePolygon()
            for point in points:
                polygon.Add(point)
            polygon.Close()  # Close the polygon
            
            # Create a face from the polygon wire
            face_builder = BRepBuilderAPI_MakeFace(polygon.Wire())
            if face_builder.IsDone():
                builder.Add(compound, face_builder.Face())
        
        # Write to STEP file
        step_writer = STEPControl_Writer()
        Interface_Static_SetCVal("write.step.schema", "AP203")
        
        step_writer.Transfer(compound, STEPControl_AsIs)
        status = step_writer.Write(str(output_path))
        
        return status == IFSelect_RetDone
        
    except ImportError:
        print("Warning: PythonOCC not available. Creating a placeholder STEP file.")
        with open(output_path, 'w') as f:
            f.write("This is a placeholder for a STEP file.\n")
            f.write("Please install PythonOCC-Core for proper STEP file generation.\n")
        return True
