import bpy 
import math
import sys
import os
import time
import re
# from pathlib import Path
# set the number in with and height
width = 12
height = 6
folder_path = f'{os.getcwd()}/keycaps'
# read in the folder of keycaps

def get_file_paths(folder_path):
	for obj in os.listdir(folder_path):
		if re.search(r'1u\_', obj):
			one_u = f'{folder_path}/{obj}'
		elif re.search(r'1uh\_', obj):
			one_uh = f'{folder_path}/{obj}'
		elif re.search(r'2u\_', obj):
			two_u = f'{folder_path}/{obj}'
		else:
			pass
	return [one_u, one_uh, two_u]

def get_mesh_dimensions(models):
	obj_dim = []
	for obj in models.values():
		w = bpy.data.objects[obj].dimensions[0]
		h = bpy.data.objects[obj].dimensions[2]
		name = obj
		obj_dim.append({'name': name, 'width': w, 'height': h})
	return obj_dim

def create_keycap(w, h, keycap_1u):
	bpy.ops.object.select_all(action="DESELECT")
	bpy.data.objects[keycap_1u].select_set(True)
	bpy.ops.object.duplicate(linked=False)
	keycap_1u = bpy.context.selected_objects[0].name
	bpy.data.objects[keycap_1u].location[0] = h
	bpy.data.objects[keycap_1u].location[1] = w
	return keycap_1u

def create_keycap_special(w, h, keycap, keycap_1u):
	# slecet the sepcific model for either 2u or 1uhoming
	bpy.ops.object.select_all(action="DESELECT")
	bpy.data.objects[keycap].select_set(True)
	bpy.ops.object.duplicate(linked=False)
	keycap = bpy.context.selected_objects[0].name
	bpy.data.objects[keycap].location[0] = h
	bpy.data.objects[keycap].location[1] = w
	bpy.data.objects[keycap].select_set(False)
	bpy.data.objects[keycap_1u].select_set(True)

def create_spacebar_column(mo, index, h_value, w_value, w, keycap_1u):
	height = 5
	for h in range(height):
		h_value = h_value + mo[index]['height'] 
		keycap_1u = create_keycap(w_value, h_value, keycap_1u)
	if w == 5:
		space_w = w_value + (w_value / 2)
		create_keycap_special(space_w, h, models['2u'], keycap_1u)
	height = 6
	return keycap_1u

def place_homeing_keys(mo, index, w, w_value, keycap, keycap_1u):
	for h in range(height):
		if h == 2:
			h_value = h_value + mo[index]['height']
			create_keycap_special(w, h, keycap, keycap_1u)
		else:
			h_value = h_value + mo[index]['height']
			keycap_1u = create_keycap(w_value, h_value, keycap_1u)
	return keycap_1u

def create_array(mo):
	index = 0
	w_value = 0
	keycap_1u = models['1u']
	keycap_1uh = models['1uh']
	for w in range(width):
		h_value = 0
		if w == 5 or 6:
			keycap_1u = create_spacebar_column(mo, index, h_value, w_value, w, keycap_1u)
		elif w == 4 or 7:
			keycap_1u = place_homeing_keys(mo, index, w, w_value, keycap_1uh, keycap_1u)
		else:
			for h in range(height):
				h_value = h_value + mo[index]['height']
				keycap_1u = create_keycap(w_value, h_value, keycap_1u)
		# move on to next colmun
		w_value = w_value + mo[index]['width']

def load_models(cap_file_paths):
	for m in cap_file_paths:
		try:
			bpy.ops.import_scene.obj(filepath=m)
		except Exception as e:
			print(e)
			pass

##########
## Main srcipt exec
##########
# get file paths for models
if __name__ == "__main__":
	cap_file_paths = get_file_paths(folder_path)
	# select all objects in a scene 
	bpy.ops.object.select_all(action="SELECT")
	bpy.ops.object.delete(use_global=False)
	time.sleep(1)
	load_models(cap_file_paths)
	# create a list of objects in the scene
	models = {(o[0].split('_')[0]):(o[1].name) for o in bpy.data.meshes.items() if re.search(r'1u|1uh|2u', o[0])}
	print(models)
	get_dim = get_mesh_dimensions(models)
	create_array(get_dim)
