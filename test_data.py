#!usr/bin/python
# -*- coding: utf-8 -*-

import json
from database import Database

#########################################
#### Data extraction from json files ####
#########################################

# Extract data of the graph
with open('graph_build.json') as json_file:
    data = json.load(json_file)
    data_graph = []
    for node in data:
    	data_graph.append(tuple(node))

# Extract data of the images
with open('img_extract.json') as json_file:
    data_images = json.load(json_file)

# Extract data to edit the graph
with open('graph_edits.json') as json_file:
    data = json.load(json_file)
    data_edit = []
    for node in data:
    	data_edit.append(tuple(node))

#################################
#### Evaluation of the graph ####
#################################

# Initial graph
build = data_graph
# Extract
extract = data_images
# Graph edits
edits = data_edit

# Get status
status = {}
if len(build) > 0:
	# Build graph
	db = Database(build[0][0])
	if len(build) > 1:
		db.add_nodes(build[1:])
	# Add extract
	db.add_extract(extract)
	# Graph edits
	db.add_nodes(edits)
	# Update status
	status = db.get_extract_status()


######################################
#### Writing results in json file ####
######################################

with open('status.json', 'w') as st:
    json.dump(status, st)


