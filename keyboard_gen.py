import bpy 
import math
import sys
import os
import time
import re
# from pathlib import Path
# set the number in with and height
width = 12
height = 5
folder_path = ''

# read in the command line args
for arg in sys.argv:
	if 'f=' in arg:
		folder_path = arg.split('=')[1]
	elif 'w=' in arg:
		width = arg.split('=')[1]
	elif 'h=' in arg:
		height = arg.split('=')[1]
	else:
		pass
# read in the folder of keycaps
if folder_path == '':
	print('you didnt supply a folder path for the keycap models')
	sys.exit(1)

def get_file_paths():
	file_name_lst = []
	for filename in os.walk(folder_path):
		file_name_lst.append(filename)

	for obj in file_name_lst[0][2]:
		try:
			if re.search(r'1u\_', obj):
				one_u = file_name_lst[0][0] + '/' + obj
				bpy.ops.import_scene.obj(one_u)
			elif re.search(r'1uh\_', obj):
				one_uh = file_name_lst[0][0] + '/' + obj
				bpy.ops.import_scene.obj(one_uh)
			elif re.search(r'2u\_', obj):
				two_u = file_name_lst[0][0] + '/' + obj
				bpy.ops.import_scene.obj(two_u)
			else:
				pass
		except Exception as e:
			print(e)
	return [one_u, one_uh, two_u]

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

def create_keycap_special(w, h, keycap, keycap_1u):
	# slecet the sepcific model for either 2u or 1uhoming
	bpy.ops.object.select_all(action="DESELECT")
	bpy.data.objects[keycap].select_set(True)
	bpy.ops.object.duplicate(linked=False)
	bpy.context.object.location[0] = h
	bpy.context.object.location[1] = w
	bpy.data.objects[keycap].select_set(False)
	bpy.data.objects[keycap_1u].select_set(True)

def create_spacebar_column(mo, index, h_value, w_value, w):
	height = 4
	for h in range(height):
		h_value = h_value + mo[index]['height']
		create_keycap(w_value, h_value)
	if w == 5:
		space_w = w_value + (w_value / 2)
		create_keycap_special(space_w, h, models['2u'], models['1u'])
	height = 5

#TODO write specific to place selected keycap
def place_homeing_keys(mo, index, w, w_value, keycap, keycap_1u):
	for h in range(height):
		if h == 2:
			h_value = h_value + mo[index]['height']
			create_keycap_special(w, h, keycap, keycap_1u)
		else:
			h_value = h_value + mo[index]['height']
			create_keycap(w_value, h_value)

def create_array(mo):
	index = 0
	w_value = 0
	for w in range(width):
		h_value = 0
		if w == 5 or 6:
			create_spacebar_column(mo, index, h_value, w_value, w)
		elif w == 4 or 7:
			place_homeing_keys(mo, index, w, w_value, models['1uh'], models['1u'])
		else:
			for h in range(height):
				h_value = h_value + mo[index]['height']
				create_keycap(w_value, h_value)
		# move on to next colmun
		w_value = w_value + mo[index]['width']

def load_models(cap_file_paths):
	for m in cap_file_paths:
		try:
			bpy.ops.import_scene.obj(filepath=m)
		except Exception as e:
			print(e)


##########
## Main srcipt exec
##########
# get file paths for models
cap_file_paths = get_file_paths()
# select all objects in a scene 
bpy.ops.object.select_all(action="SELECT")
bpy.ops.object.delete(use_global=False)
time.sleep(1)
load_models(cap_file_paths)
# create a list of objects in the scene
objects = [bpy.data.objects[i].name for i in range(len(bpy.data.objects))]
models = {o.split('_')[0]:o for o in objects if re.search(r'1u|1uh|2u', o)}
get_dim = get_mesh_dimensions()
create_array(get_dim)
