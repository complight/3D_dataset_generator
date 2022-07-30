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
    
    rotate_mode_c = data['rotate']['rotate_mode']
    rotate_interval_c = data['rotate']['rotate_interval']
    cam_ascend_c = data['rotate']['cam_ascend']
    cam_ascend_interval_c = data['rotate']['cam_ascend_interval']
    
    VP_mode_c = data['view_plane']['VP_mode']
    VP_camCube_c = data['view_plane']['VP_camCube']
    VP_size_x_c = data['view_plane']['VP_size_x']
    VP_size_y_c = data['view_plane']['VP_size_y']
    VP_dist_x_c = data['view_plane']['VP_dist_x']
    VP_dist_y_c = data['view_plane']['VP_dist_y']
    cam_dispersion_c = data['view_plane']['cam_dispersion']
    cam_nadir_bound_c = data['view_plane']['cam_nadir_bound']

    render_compression_c = data['global']['render_compression']
    Eevee_c = data['global']['Eevee']
    Cycles_c = data['global']['Cycles']
    GPU_c = data['global']['GPU']
    mem_tile_c = data['global']['mem_tile']
    sample_rate_c = data['global']['sample_rate']
    
    config_save = generator(
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
                        rotate_mode_c,
                        rotate_interval_c,
                        cam_ascend_c,
                        cam_ascend_interval_c,
                        VP_mode_c,
                        VP_camCube_c,
                        VP_size_x_c,
                        VP_size_y_c,
                        VP_dist_x_c,
                        VP_dist_y_c,
                        cam_dispersion_c,
                        cam_nadir_bound_c,
                        render_compression_c,
                        Eevee_c,
                        Cycles_c,
                        GPU_c,
                        mem_tile_c,
                        sample_rate_c
                        )
    with open(copy_path, "r") as conf_src, open(config_save, "w") as conf_dest:
        conf_dest.write(conf_src.read())

if __name__ == "__main__":
    main()
    