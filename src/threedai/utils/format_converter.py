import numpy as np
import tempfile
import os
from pathlib import Path

def mesh_to_stl(vertices, faces, output_path):
    """
    Convert a mesh (vertices and faces) to an STL file
    
    Args:
        vertices: numpy array of shape (n, 3) containing the vertices
        faces: numpy array of shape (m, 3) containing the faces (vertex indices)
        output_path: path to save the STL file
        
    Returns:
        bool: True if conversion was successful, False otherwise
    """
    # Validate input
    if not isinstance(vertices, np.ndarray) or vertices.ndim != 2 or vertices.shape[1] != 3:
        print("Error: vertices must be a numpy array of shape (n, 3)")
        return False
        
    if not isinstance(faces, np.ndarray) or faces.ndim != 2 or faces.shape[1] != 3:
        print("Error: faces must be a numpy array of shape (m, 3)")
        return False
    
    try:
        # Create the STL data structure
        data = np.zeros(len(faces), dtype=[
            ('normals', 'f4', (3,)),
            ('vertices', 'f4', (3, 3)),
            ('attr', 'u2', (1,)),
        ])

        # Fill the vertices
        for i, face in enumerate(faces):
            data['vertices'][i] = vertices[face]

            # Calculate face normal
            v1 = vertices[face[1]] - vertices[face[0]]
            v2 = vertices[face[2]] - vertices[face[0]]
            normal = np.cross(v1, v2)
            norm = np.linalg.norm(normal)
            if norm != 0:
                normal = normal / norm
            data['normals'][i] = normal

        # Write binary STL
        with open(output_path, 'wb') as fp:
            fp.write(b'\x00' * 80)  # Header
            fp.write(np.array(len(faces), '<i4').tobytes())
            fp.write(data.tobytes())
        
        return True
        
    except Exception as e:
        print(f"Error converting mesh to STL: {str(e)}")
        return False

def glb_to_stl(glb_path, stl_path):
    """Convert a GLB file to STL format.
    
    Args:
        glb_path: Path to the input GLB file
        stl_path: Path to save the output STL file
        
    Returns:
        bool: True if conversion was successful, False otherwise
    """
    try:
        import trimesh
        import numpy as np
        
        # Check if file exists
        if not os.path.exists(glb_path):
            print(f"Error: GLB file not found at {glb_path}")
            return False
            
        # Load the GLB file
        mesh = trimesh.load(glb_path)
        
        # Extract vertices and faces
        vertices = np.array(mesh.vertices)
        faces = np.array(mesh.faces)
        
        # Convert to STL using the mesh_to_stl function
        return mesh_to_stl(vertices, faces, stl_path)
        
    except ImportError:
        print("Warning: trimesh not available. Cannot convert GLB to STL.")
        return False
    except Exception as e:
        print(f"Error converting GLB to STL: {str(e)}")
        return False