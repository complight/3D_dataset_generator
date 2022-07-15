import bpy
import numpy as np
import os
import sys
import json


# append directory
dir = os.path.dirname(bpy.data.filepath)
if not dir in sys.path:
    sys.path.append(dir)
    #print(sys.path)
   
import imp

import BRG_generator  
imp.reload(BRG_generator)

from BRG_generator import *

def main():
    path_M = bpy.data.filepath
    directory_M  = os.path.dirname(path_M )
    copy_path = os.path.join(directory_M , "config.json")
    with open(copy_path) as config_file:
        data = json.load(config_file)

    width = data['cube']['cubeSize']
    height = data['cube']['scaleX']

    # cube
    cubeSize_c = data['cube']['cubeSize']           # cube size, blender default 2
    scaleX_c = data['cube']['scaleX']               # x sacel in object creation
    scaleY_c = data['cube']['scaleY']               # y sacel in object creation
    scaleZ_c = data['cube']['scaleZ']               # z sacel in object creation

    # light
    light_base1_c = data['light']['light_base1']
    light_base2_c = data['light']['light_base2']

    # generation
    exTime_c = data['generation']['exTime']
    extrDistanceMax_c = data['generation']['extrDistanceMax']
    extrDistanceMin_c = data['generation']['extrDistanceMin']
    randomStep_c = data['generation']['randomStep']
    shrink_P_c = data['generation']['shrink_P']
    shrink_val_c = data['generation']['shrink_val']
    inset_P_c = data['generation']['inset_P']
    inset_thickness_c = data['generation']['inset_thickness']
    offset_P_c = data['generation']['offset_P']
    offset_val_c = data['generation']['offset_val']
    plane_S_c = data['generation']['plane_S']

    # Z-path ranger
    node_range_min_c = data['node']['node_range_min']
    node_range_max_c = data['node']['node_range_max']

    cam_location_X_c = data['camera']['cam_location_X']
    cam_location_Y_c = data['camera']['cam_location_Y']
    cam_location_Z_c = data['camera']['cam_location_Z']

    cam_len_c = data['camera']['cam_len']
    rotate_interval_c = data['camera']['rotate_interval']

    render_compression_c = data['global']['render_compression']
    
    Eevee_c = data['global']['Eevee']
    Cycles_c = data['global']['Cycles']
    GPU_c = data['global']['GPU']
    mem_tile_c = data['global']['mem_tile']
    sample_rate_c = data['global']['sample_rate']
    
    generator(
            cubeSize_c,
            scaleX_c,
            scaleY_c,
            scaleZ_c,
            light_base1_c,
            light_base2_c,
            exTime_c,
            extrDistanceMax_c,
            extrDistanceMin_c,
            randomStep_c,
            shrink_P_c,
            shrink_val_c,
            inset_P_c,
            inset_thickness_c,
            offset_P_c,
            offset_val_c,
            plane_S_c,
            node_range_min_c,
            node_range_max_c,
            cam_location_X_c,
            cam_location_Y_c,
            cam_location_Z_c,
            cam_len_c,
            rotate_interval_c,
            render_compression_c,
            Eevee_c,
            Cycles_c,
            GPU_c,
            mem_tile_c,
            sample_rate_c
            )

if __name__ == "__main__":
    main()
    