# obj_parse.py
# Simple WaveFront Obj file parser. Currently focused only in geometry.
from pyfbsdk import *

obj_file = r'e:\01_PROJECTS\05_PYTHON\CustomPypelineTools\ch_06\knockers.obj'

def parse_obj(file):
    """
    Returns a dict containing all the OBJ data for the geometry.
    """
    object_name = None
    obj_v = []
    obj_vn = []
    obj_vt = []
    obj_f = []
    grp_name = None

    with open (file, 'r') as obj:

        for line in obj:
            if line.startswith('#'):
                continue
            if line.startswith('o'):
                object_name = str(line.split()[1])
            
            if line.startswith('g'):
                grp_name = str(line.split()[1])
            
            if line.startswith('v'):
                data = line.split()
                if data[0] == 'vn':
                    obj_vn.append(line)
                elif data[0] =='vt':
                    obj_vt.append(line)
                elif data[0] == 'v':
                    vertex = (data[1], data[2], data[3])
                    obj_v.append(vertex)

            if line.startswith('f'):
                data = line.split()
                face = data[1:]
                obj_f.append(face)
        
    model3d = {'obj': {'name': grp_name, 
                'vertices': obj_v, 
                'vertex_normals': obj_vn, 
                'vertex_texture': obj_vt,
                'faces': obj_f} }

    print(model3d)
    return(model3d)


# Create model in MotionBuilder
obj_model = parse_obj(obj_file)
ctrl_mesh = FBMesh('Cubed_Sphere')

ctrl_mesh.GeometryBegin()

# add vertices
ctrl_mesh.VertexInit(len(obj_model['obj']['vertices']), False, False, True)

for vertex in obj_model['obj']['vertices']:
    ctrl_mesh.VertexAdd(float(vertex[0]) * 100, float(vertex[1]) * 100, float(vertex[2]) * 100)  # to match original scale form Silo (m) in Mobu (cm) multply by 100

# create faces
for face in obj_model['obj']['faces']:
    ctrl_mesh.PolygonBegin()
    for data in face:
        vertex_data = data.split('/')
        ctrl_mesh.PolygonVertexAdd(int(vertex_data[0])-1)  # OBJ Face = v, vt, vn starts with index 1, that's why we substract 1.
    ctrl_mesh.PolygonEnd()


ctrl_mesh.ComputeVertexNormals(True)
ctrl_mesh.GeometryEnd()

# Add the geometry to a model
obj_model = FBModelCube(obj_model['obj']['name'])
obj_model.Geometry = ctrl_mesh
obj_model.ShadingMode = FBModelShadingMode.kFBModelShadingAll

obj_model.Visible = True
obj_model.Show = True

