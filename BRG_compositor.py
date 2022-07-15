import bpy, bmesh
import random
import numpy as np
import os
import sys
import math
from time import gmtime, strftime


# append directory
dir = os.path.dirname(bpy.data.filepath)
if not dir in sys.path:
    sys.path.append(dir )
    #print(sys.path)
    
    
import imp
# imp.reload()

plane_size = 3000

# Z-path ranger
node_range_min = 50
node_range_max = 200

cam_location = (140, 0, 36)
cam_len = 33

render_compression = 70

bpy.context.scene.view_layers["ViewLayer"].use_pass_z = True
bpy.context.scene.view_layers["ViewLayer"].use_pass_mist = True
bpy.context.scene.render.use_placeholder = True
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False, confirm=False)


# random material
def get_random_color():
    ''' generate rgb using a list comprehension '''
    r, g, b = [random.random() for i in range(3)]
    return r, g, b, 1


# rotation
def rotate(point, angle_degrees, axis=(0,1,0)):
    theta_degrees = angle_degrees
    theta_radians = math.radians(theta_degrees)

    rotated_point =  np.dot(rotation_matrix(axis, theta_radians), point)
    
    return rotated_point


def rotation_matrix(axis, theta):
    """
    Return the rotation matrix associated with counterclockwise rotation about
    the given axis by theta radians.
    """
    axis = np.asarray(axis)
    axis = axis / math.sqrt(np.dot(axis, axis))
    a = math.cos(theta / 2.0)
    b, c, d = -axis * math.sin(theta / 2.0)
    aa, bb, cc, dd = a * a, b * b, c * c, d * d
    bc, ad, ac, ab, bd, cd = b * c, a * d, a * c, a * b, b * d, c * d
    return np.array([[aa + bb - cc - dd, 2 * (bc + ad), 2 * (bd - ac)],
                     [2 * (bc - ad), aa + cc - bb - dd, 2 * (cd + ab)],
                     [2 * (bd + ac), 2 * (cd - ab), aa + dd - bb - cc]])


# create a base plane
bpy.ops.mesh.primitive_plane_add(
    size = 3000,
    calc_uvs=True, 
    enter_editmode=False, 
    align='WORLD', 
    location=(0, 0, 0), 
    scale=(scaleX*7, scaleY*7, scaleZ*7)
    )
base_plane = bpy.context.active_object

# create camera
cam_data = bpy.data.cameras.new('camera')
cam = bpy.data.objects.new('camera', cam_data)
cam.location=(140, 0, 36)
cam.data.lens = 33


constraint =cam.constraints.new(type='TRACK_TO')
constraint.target=base_plane
 
bpy.context.collection.objects.link(cam)


# Set up rendering of depth map:
bpy.context.scene.use_nodes = True
tree = bpy.context.scene.node_tree
links = tree.links

# clear default nodes
for n in tree.nodes:
    tree.nodes.remove(n)

# create input render layer node
rl = tree.nodes.new('CompositorNodeRLayers')

map = tree.nodes.new(type="CompositorNodeMapRange")
# Size is chosen kind of arbitrarily, try out until you're satisfied with resulting depth map.
map.inputs[1].default_value = 50          ##### Min value here
map.inputs[2].default_value = 200         ##### Max value here
map.inputs[3].default_value = 0.0
map.inputs[4].default_value = 1.0

links.new(rl.outputs[2], map.inputs[0])

invert = tree.nodes.new(type="CompositorNodeInvert")
links.new(map.outputs[0], invert.inputs[1])

# The viewer can come in handy for inspecting the results in the GUI
depthViewer = tree.nodes.new(type="CompositorNodeViewer")
links.new(map.outputs[0], depthViewer.inputs[0])
# Use alpha from input.
links.new(rl.outputs[1], depthViewer.inputs[1])

# The viewer can come in handy for inspecting the results in the GUI
imageViewer = tree.nodes.new(type="CompositorNodeViewer")
links.new(rl.outputs[0], imageViewer.inputs[0])
# Use alpha from input.
links.new(rl.outputs[1], imageViewer.inputs[1])

# Get absolute path:
filepath = bpy.context.scene.render.filepath
absolutepath = bpy.path.abspath(filepath)
path = bpy.data.filepath

directory = os.path.dirname(path)

generate_date = strftime("%Y-%m-%d_%H-%M-%S", gmtime())
image_path = os.path.join(directory, "output", generate_date, "image_out")
depth_path = os.path.join(directory, "output", generate_date, "depth_out")
EXR_path = os.path.join(directory, "output", generate_date, "EXR_out")

# image_path = path + "\\image_out"
# depth_path = path + "\\depth_out"

# create a file output node and set the path
Zpath_output_node = tree.nodes.new(type="CompositorNodeOutputFile")
Zpath_output_node.format.file_format = "PNG" # default is "PNG"
Zpath_output_node.format.color_mode = "BW"  # default is "BW"
Zpath_output_node.format.color_depth = "8"  # default is 8
Zpath_output_node.format.compression = 70     # default is 15
Zpath_output_node.base_path = depth_path
links.new(map.outputs[0], Zpath_output_node.inputs[0])

EXR_output_node = tree.nodes.new(type="CompositorNodeOutputFile")
EXR_output_node.format.file_format = "OPEN_EXR" # default is "PNG"
EXR_output_node.format.color_mode = "RGB"  # default is "BW"
EXR_output_node.format.color_depth = "16"  # default is 8
EXR_output_node.format.compression = 100     # default is 15
EXR_output_node.base_path = EXR_path
links.new(rl.outputs[2], EXR_output_node.inputs[0])

image_output_node = tree.nodes.new(type="CompositorNodeOutputFile")
image_output_node.format.file_format = "PNG" # default is "PNG"
image_output_node.format.color_mode = "RGB"  # default is "BW"
image_output_node.format.color_depth = "8"  # default is 8
image_output_node.format.compression = 70     # default is 15
image_output_node.base_path = image_path
links.new(rl.outputs[0], image_output_node.inputs[0])

scene = bpy.context.scene
scene.camera = cam

for angle in range(0, 360, 60):
    cam_location = cam.location
    cam.location = rotate(cam_location, 60, axis=(0,0,1))
    angle_str = str(angle)
    image_output_node.file_slots[0].path = "image_" + angle_str + "deg_"
    Zpath_output_node.file_slots[0].path = "depth_" + angle_str + "deg_"
    EXR_output_node.file_slots[0].path = "EXR_" + angle_str + "deg_"
    bpy.ops.render.render(write_still=1)
    
# bpy.ops.render.render(write_still=1)