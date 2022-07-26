import bpy, bmesh
import random
import numpy as np
import os
import sys
import math
import time


# append directory
dir = os.path.dirname(bpy.data.filepath)
if not dir in sys.path:
    sys.path.append(dir )
    #print(sys.path)
   
import imp

import utils  
imp.reload(utils)

from utils import *


def generator(
    cubeSize_conf, 
    scaleX_conf, 
    scaleY_conf, 
    scaleZ_conf, 
    light_base1_conf, 
    light_base2_conf, 
    exTime_conf, 
    extrDistanceMax_conf, 
    extrDistanceMin_conf, 
    randomStep_conf, 
    shrink_P_conf, 
    shrink_val_conf, 
    inset_P_conf, 
    inset_thickness_conf, 
    offset_P_conf, 
    offset_val_conf, 
    plane_S_conf, 
    node_range_min_conf, 
    node_range_max_conf, 
    cam_location_X_conf, 
    cam_location_Y_conf, 
    cam_location_Z_conf, 
    cam_len_conf, 
    rotate_interval_conf, 
    cam_ascend_conf,
    cam_ascend_interval_conf,
    render_compression_conf, 
    Eevee_conf, 
    Cycles_conf, 
    GPU_conf,
    mem_tile_conf,
    sample_rate_conf
    ):
        
    # variables for cube
    cubeSize = cubeSize_conf            # cube size, blender default 2
    scaleX = scaleX_conf              # x sacel in object creation
    scaleY = scaleY_conf              # y sacel in object creation
    scaleZ = scaleZ_conf              # z sacel in object creation

    # light
    light_base1 = light_base1_conf #
    light_base2 = light_base2_conf #

    # position
    arr = np.random.randint(-100,100,size = (300,3))

    # variables for the itteration
    exTime = exTime_conf       # how many time will extrued the object 7
    extrDistanceMax = extrDistanceMax_conf    # max distance of extrution in m 15
    extrDistanceMin = extrDistanceMin_conf     # min distance of extrution in m 2
    randomStep = randomStep_conf          # step between values in random 3
    shrink_P = shrink_P_conf            # 0
    shrink_val = shrink_val_conf          # 2
    inset_P = inset_P_conf
    inset_thickness = inset_thickness_conf
    offset_P = offset_P_conf
    offset_val = offset_val_conf
    plane_S = plane_S_conf

    # Z-path ranger
    node_range_min = node_range_min_conf
    node_range_max = node_range_max_conf

    cam_location_X = cam_location_X_conf
    cam_location_Y = cam_location_Y_conf
    cam_location_Z = cam_location_Z_conf
    
    cam_ascend = cam_ascend_conf
    cam_ascend_interval = cam_ascend_interval_conf


    cam_location = (cam_location_X, cam_location_Y, cam_location_Z)
    cam_len = cam_len_conf
    rotate_interval = rotate_interval_conf

    render_compression = render_compression_conf
    
    Eevee = Eevee_conf
    Cycles = Cycles_conf
    GPU = GPU_conf
    sample_rate = sample_rate_conf
    mem_tile = mem_tile_conf
    
    bpy.context.scene.view_layers["ViewLayer"].use_pass_z = True
    bpy.context.scene.view_layers["ViewLayer"].use_pass_mist = True
    bpy.context.scene.render.use_placeholder = True
    bpy.ops.object.select_all(action='SELECT')
    if Eevee:
        bpy.context.scene.render.engine = 'BLENDER_EEVEE'
    elif Cycles:
        bpy.context.scene.render.engine = 'CYCLES'
        if GPU:
            bpy.context.scene.cycles.device = 'GPU'
            bpy.context.scene.cycles.use_auto_tile = True
            bpy.context.scene.cycles.tile_size = mem_tile
    else:
        bpy.context.scene.render.engine = 'BLENDER_EEVEE'
        
    bpy.context.scene.cycles.samples = sample_rate
    bpy.ops.object.delete(use_global=False, confirm=False)


    # Create light datablock
    light_data = bpy.data.lights.new(name="my-light-data", type='SUN')
    light_data.energy = 30

    # Create new object, pass the light data 
    light_object = bpy.data.objects.new(name="my-light", object_data=light_data)

    # Link object to collection in context
    bpy.context.collection.objects.link(light_object)




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
        size = plane_S,
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
            if random.randint(0,100) < shrink_P:
                bpy.ops.transform.shrink_fatten(value=shrink_val, 
                                                use_even_offset=False, 
                                                mirror=True, 
                                                use_proportional_edit=False, 
                                                proportional_edit_falloff='SMOOTH', 
                                                proportional_size=1, 
                                                use_proportional_connected=False,
                                                use_proportional_projected=False, 
                                                release_confirm=True)
                                                
            if random.randint(0,100) < inset_P:                                    
                bpy.ops.mesh.inset(thickness=inset_thickness, depth=0, release_confirm=True)

            if n == (exTime - 1):                                  
                if random.randint(0,100) < offset_P:                                    
                    bpy.ops.mesh.bevel(offset=offset_val,
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
    cam.location = cam_location
    cam.data.lens = cam_len
    cam.data.clip_end = 10000



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
    # Size is chosen arbitrarily, try out until you're satisfied with resulting depth map
    map.inputs[1].default_value = node_range_min          ##### Min value here
    map.inputs[2].default_value = node_range_max         ##### Max value here
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

    generate_date = strftime("%Y-%m-%d_%H-%M-%S", time.localtime())
    
    log_name = generate_date + "_log.txt"
    config_name = generate_date + "_config.json"
    image_path = os.path.join(directory, "output", generate_date, "image_out")
    depth_path = os.path.join(directory, "output", generate_date, "depth_out")
    EXR_path = os.path.join(directory, "output", generate_date, "EXR_out")
    copy_path = os.path.join(directory, "output", generate_date, "scene_copy.blend")
    log_path = os.path.join(directory, "log", log_name)
    config_path = os.path.join(directory, "log", config_name)

    # image_path = path + "\\image_out"
    # depth_path = path + "\\depth_out"

    # create a file output node and set the path
    Zpath_output_node = tree.nodes.new(type="CompositorNodeOutputFile")
    Zpath_output_node.format.file_format = "PNG" # default is "PNG"
    Zpath_output_node.format.color_mode = "BW"  # default is "BW"
    Zpath_output_node.format.color_depth = "8"  # default is 8
    Zpath_output_node.format.compression = render_compression     # default is 15
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
    image_output_node.format.compression = render_compression     # default is 15
    image_output_node.base_path = image_path
    links.new(rl.outputs[0], image_output_node.inputs[0])

    scene = bpy.context.scene
    scene.camera = cam
    Z_ascend = cam_location_Z
    
    for ascend in range(0, cam_ascend + 1, cam_ascend_interval):
        Z_ascend = cam_location_Z + ascend
        
        cam.location = (cam_location_X, cam_location_Y, Z_ascend)
        print(cam_location)
    
        for angle in range(0, 360, rotate_interval):
            cam_location = cam.location
            cam.location = rotate(cam_location, rotate_interval, axis=(0,0,1))
            angle_str = str(angle)
            image_output_node.file_slots[0].path = "image_" + angle_str + "deg_" + "Z" + str(Z_ascend) + "_"
            Zpath_output_node.file_slots[0].path = "depth_" + angle_str + "deg_" + "Z" + str(Z_ascend) + "_"
            EXR_output_node.file_slots[0].path = "EXR_" + angle_str + "deg_" + "Z" + str(Z_ascend) + "_"
            
            image_name = "\n" + angle_str + " deg - Z " + str(Z_ascend) + ": \n"
            cam_info = "    location: " + " , ".join(str(x) for x in cam.location) + "\n    rotation: " + " , ".join(str(x) for x in cam.rotation_euler)
            log_file = open(log_path, 'a')
            print(image_name)
            print(cam_info)
            log_file.write(image_name)
            log_file.write(cam_info)
            log_file.close()
            
            bpy.ops.render.render(write_still=1)
        
    # bpy.ops.render.render(write_still=1)
    bpy.ops.wm.save_as_mainfile(filepath = copy_path, copy = True)
    
    return config_path
# generator()

