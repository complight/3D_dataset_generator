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


# variables for cube
cubeSize = 3            # cube size, blender default 2
scaleX = 1              # x sacel in object creation
scaleY = 1              # y sacel in object creation
scaleZ = 1              # z sacel in object creation

# light
light_base1 = 200
light_base2 = 300

# position
arr = np.random.randint(-100,100,size = (300,3))

# variables for the itteration
exTime = 7       # how many time will extrued the object
extrDistanceMax = 15    # max distance of extrution in m
extrDistanceMin = 2     # min distance of extrution in m
randomStep = 3          # step between values in random
shrink_chance = 0
shrink_val = 2
inset_chance = 10
inset_thickness = 1
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


# Create light datablock
light_data = bpy.data.lights.new(name="my-light-data", type='SUN')
light_data.energy = 30

# Create new object, pass the light data 
light_object = bpy.data.objects.new(name="my-light", object_data=light_data)

# Link object to collection in context
bpy.context.collection.objects.link(light_object)


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

# Change light position

if random.randint(1,2) == 1:
    light_x = random.randint(light_base1, light_base2)
    if random.randint(1,2) == 1:
        light_y = random.randint(light_base1, light_base2)
    else:
        light_y = random.randint(-light_base2, -light_base1)
else:
    light_x = random.randint(light_base1, light_base2)
    if random.randint(1,2) == 1:
        light_y = random.randint(light_base1, light_base2)
    else:
        light_y = random.randint(-light_base2, -light_base1)
    
light_z = random.randint(light_base1, light_base2)

light_object.location = (light_x, light_y, light_z)

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

# variables that will reset in each itteration
# value that updates with each extrution, 6 for a cube
faceCount =  6

for i in range(len(arr)):

    # create a cube and go in to edit mode
    bpy.ops.mesh.primitive_cube_add(
        size= cubeSize, 
        enter_editmode=False, 
        align='WORLD', 
        location=(arr[i][0], arr[i][1], (abs(arr[i][2])%7)), 
        scale=(scaleX, scaleY, scaleZ)
        )

    # selet faces
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_mode(type="FACE")
    bpy.ops.object.mode_set(mode='OBJECT')

    # sets active object for face count after each extrution
    obj = bpy.context.active_object
    
    
    matName = "cube_mat" + str(i)
    new_mat = bpy.data.materials.new(matName)
    new_mat.use_nodes = True
    principled = new_mat.node_tree.nodes['Principled BSDF']
    principled.inputs['Base Color'].default_value = (get_random_color())
    obj.data.materials.append(new_mat)
    
    for n in range(exTime):
        
        # finds out how many faces there are
        objData = obj.data 
        faceCount = len(objData.polygons)
        
        # deselcts all the faces 
        for i in range(faceCount):
            obj.data.polygons[i].select = False

        # extrution
        obj.data.polygons[random.randrange(0, faceCount)].select = True
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.extrude_faces_move(TRANSFORM_OT_shrink_fatten = 
                                        {"value":random.randrange(extrDistanceMin,
                                                                extrDistanceMax,
                                                                randomStep)})
        if random.randint(0,100) < 0:
            bpy.ops.transform.shrink_fatten(value=2, 
                                            use_even_offset=False, 
                                            mirror=True, 
                                            use_proportional_edit=False, 
                                            proportional_edit_falloff='SMOOTH', 
                                            proportional_size=1, 
                                            use_proportional_connected=False,
                                            use_proportional_projected=False, 
                                            release_confirm=True)
        if random.randint(0,100) < 10:                                    
            bpy.ops.mesh.inset(thickness=1, depth=0, release_confirm=True)

        if n == (exTime - 1):                                  
            if random.randint(0,100) < 90:                                    
                bpy.ops.mesh.bevel(offset=1,
                            offset_pct=0, 
                            release_confirm=True)                                
                                
        bpy.ops.object.mode_set(mode='OBJECT')     # goes back to object mode
        
    
    # removes doubles from the object
    bpy.ops.object.mode_set(mode='EDIT')       # goes in to edit mode
    bpy.ops.mesh.select_mode(type="FACE")      # choose faces as selection 
    bpy.ops.mesh.select_all(action='SELECT')   # selects all the faces
    bpy.ops.mesh.remove_doubles()              # removes doubles
    bpy.ops.object.mode_set(mode='OBJECT')     # goes back to object mode


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