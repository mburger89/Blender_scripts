import bpy 
import math

# set the number in with and height
width = 12
height = 5

models = bpy.context.selected_objects

def get_mesh_dimensions():
    obj_dim = []
    for obj in models:
        w = obj.dimensions[0]
        h = obj.dimensions[2]
        name = obj.name
        obj_dim.append({'name': name, 'width': w, 'height': h})
    return obj_dim

def create_keycap(w,h):
    bpy.ops.object.duplicate(linked=False)
    bpy.context.object.location[0] = h
    bpy.context.object.location[1] = w

def create_array(mo):
    for index in range(len(mo)):
        w_value = 0
        for w in range(width):
            h_value = 0
            for h in range(height):
                h_value = h_value + mo[index]['height']
                create_keycap(w_value, h_value)
            # move on to next colmun
            w_value = w_value + mo[index]['width']
            
get_dim = get_mesh_dimensions()

create_array(get_dim)
