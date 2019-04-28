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
		aNode = self.root
		aEdge = None 
		aPos = 0
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
				# print(edge_label)
				if aNode == self.root and aEdge == None and aPos == 0:
					if aNode.atcg[edge_label][0] == None and aNode.atcg[edge_label][1] == None:
						aNode.atcg[edge_label] = [[i, self.end], None]
						rem -= 1
					elif aNode.atcg[edge_label][0] != None:
						aNode = self.root
						aEdge = aNode.atcg[edge_label]
						aPos = 1
						break
				else:
					print(active)
					if read[aEdge[0][0]+aPos] == checking_string[0]:
						aPos += 1
						break  
					else:
						print(rem)
						for k in range(rem, 0, -1):
							print(k)
							inserting_prefix = read[i-k+1:i+1]
							print("inserting prefix:", inserting_prefix)
							new_edge_label = 0:
								if inserting_prefix[-1] == 't':
									new_edge_label = 1
								elif inserting_prefix[-1] == 'c':
									new_edge_label = 2
								elif inserting_prefix[-1] == 'g':
									new_edge_label = 3
							if inserting_prefix[0] == aEdge[0][0]:
								#create internal node
								aEdge[1] = Node()
								aEdge[1].atcg[new_edge_label] = [[i, self.end], None]
								aEdge[1].atcg[read[aEdge[0][0]+aPos]] = [aEdge[0][0]+aPos, aEdge[0][1], None]
								aPos -= 1
								aEdge = aNode.atcg[inserting_prefix[1]]
							


							print("inserting prefix:", inserting_prefix)

							rem -= 1

		print("rem:", rem)
			
			


end = End()
tree = SuffixTree("atcgatg", end)
print(tree.root.atcg)

