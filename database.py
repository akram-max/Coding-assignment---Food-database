#!usr/bin/python
# -*- coding: utf-8 -*-

import copy

class Database(object):

	def __init__(self, root):
		self.graph = Graph([(root,None)]) # Current and updated graph of the database
		self.images = {} # Dictionary of images and they're classes
		self.old_graph = Graph([]) # Graph before editing
		self.added_nodes = [] # Nodes added to the graph 

	def add_nodes(self, list_nodes):
		self.graph.add_nodes(list_nodes)
		self.added_nodes = list_nodes

	def add_extract(self, images):
		self.images = images
		self.old_graph = copy.deepcopy(self.graph)

	def get_extract_status(self):
		status = {} # dictionary
		nodes_set = set() # set
		nodes_set.update([node.name for node in self.graph.nodes])
		old_nodes = set()
		old_nodes.update([node.name for node in self.old_graph.nodes])

		for image in self.images.keys():

			coverage_staged_activated = False

			for image_class in self.images[image]:

				# Invalidity test
				if image_class not in nodes_set:
					status[image] = "invalid"
					break

				elif (len(nodes_set.difference(old_nodes)) != 0) and (not coverage_staged_activated):

					for node in self.added_nodes:
						# Coverage test
						for n in self.old_graph.nodes:
							if n.name == image_class:
								parent_node = n.parent
						if node[1] == parent_node:
							status[image] = "coverage_staged"
							coverage_staged_activated = True
							break

						# Granularity test
						if node[1] == image_class:
							status[image] = "granularity_staged"
							break

			if image not in status:
				status[image] = "valid"

		return status

class Node():

	def __init__(self, node_name, parent):
		self.name = node_name
		self.parent = parent


class Graph():

	def __init__(self, graph):
		self.nodes = []
		for i in graph:
			node = Node(i[0], i[1])
			(self.nodes).append(node)

	def add_nodes(self, list_nodes):
		for i in list_nodes:
			(self.nodes).append(Node(i[0], i[1]))


"""
#from database import Database

# Initial graph
build = [("core", None), ("A", "core"), ("B", "core"), ("C", "core"), ("C1", "C")]
# Extract
extract = {"img001": ["A", "B"], "img002": ["A", "C1"], "img003": ["B", "E"]}
# Graph edits
edits = [("A1", "A"), ("A2", "A"), ("C2", "C")]

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
print(status)
"""
