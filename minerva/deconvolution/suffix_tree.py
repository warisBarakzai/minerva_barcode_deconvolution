from minerva.gimmebio.kmers import MinSparseKmerSet
from minerva.gimmebio.readclouds import iterReadClouds
from itertools import combinations
import numpy as np
import sys

class End:
	def __init__(self):
		self.val = -1

	def __str__(self):
		return self.val
	def __repr__(self):
		return str(self.val)


class Node:
	def __init__(self):
		#			  a(Edge, Node)  t 				c 			g 	 
		self.atcg = [[None, None], [None, None], [None, None], [None, None]]
		self.suffixLink = None

class SuffixTree:
	def __init__(self, readList, End):
		self.root = Node()
		self.end = End
		self.build_tree(readList)


	def build_tree(self, read):
		# active = (self.root, None, 0)
		# rem = 0
		# end = -1
		# #primary steps, i.e no repeats of characters. The easy part
		# for i in range(len(list)):
		# 	rem += 1
		# 	end += 1
		# 	while rem > 0:
		# 		if active == (self.root, None, 0):
		# 			if self.root.atcg[0] == (None, None):
		# Naive implementation
		cursor = self.root
		rem = 0
		for i in range(len(read)):
			checking_string = read[i:]
			print(checking_string)
			rem += 1
			self.end.val += 1
			while rem > 0:
				edge_label = 0
				if checking_string[0] == 't':
					edge_label = 1
				elif checking_string[0] == 'c':
					edge_label = 2
				elif checking_string[0] == 'g':
					edge_label = 3
				print(edge_label)
				if cursor.atcg[edge_label][0] == None and cursor.atcg[edge_label][1] == None:
					cursor.atcg[edge_label] = [[0, self.end], None]
					rem = 0
			
			


end = End()
tree = SuffixTree("atcg", end)
print(tree.root.atcg)

