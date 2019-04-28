from minerva.gimmebio.kmers import MinSparseKmerSet
from minerva.gimmebio.readclouds import iterReadClouds
from itertools import combinations
import numpy as np
import sys

class Node:
	def __init__(self):
		#			  a(Edge, Node)  t 				c 			g 	 
		self.atcg = ((None, None), (None, None), (None, None), (None, None))
		self.suffixLink = None

class SuffixTree:
	def __init__(self, readList):
		self.root = Node()
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
		end = -1
		for i in range(len(read) +1):
			checking_string = read[:i]
			
			



tree = SuffixTree("atcg")

