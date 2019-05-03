from minerva.gimmebio.kmers import MinSparseKmerSet
from minerva.gimmebio.readclouds import iterReadClouds
from itertools import combinations
import numpy as np
import sys

class End:
	def __init__(self, val = -1):
		self.val = val

	def __str__(self):
		return self.val
	def __repr__(self):
		return str(self.val)
	def __gt__(self, other):
		return self.val > other.val


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

	def get_index(self, character):
		if character == 'a':
			return 0
		if character == 't':
			return 1
		elif character == 'c':
			return 2
		elif character == 'g':
			return 3

	def build_tree(self, read):
		aNode = self.root
		aEdge = None 
		aPos = 0
		rem = 0
		for i in range(len(read)):
			print("rem:", rem)
			# print("Node:", aNode,"//Edge:", aEdge,"//Pos:", aPos)
			checking_string = read[i:]
			edge_label = self.get_index(checking_string[0])
			rem += 1
			self.end.val += 1
			first = False
			preNode = None
			# Start the Phase
			while rem > 0:
				if aPos == 0:
					if aNode.atcg[edge_label][0] == None and aNode.atcg[edge_label][1] == None:
						aNode.atcg[edge_label] = [[i, self.end], None]
						rem -= 1
					elif aNode.atcg[edge_label][0] != None:
						aNode = self.root
						aEdge = aNode.atcg[edge_label]
						aPos = 1
						break
				else:
					if aEdge[0][1] != self.end and aEdge[0][0] + aPos > aEdge[0][1]:
						print("read:", read[aEdge[1].atcg[edge_label][0][0]], "OG:", checking_string[0])
						if aEdge[1] != None and read[aEdge[1].atcg[edge_label][0][0]] == checking_string[0]:
							aNode = aEdge[1]
							aEdge = aNode.atcg[edge_label]
							aPos = 1
							break
					elif read[aEdge[0][0]+aPos] == checking_string[0]:
						aPos += 1
						break  
					# Commented code - This is never going to happen because if the second is end Edge+position < end
					# elif aEdge[0][1] == self.end and End(aEdge[0][0] + aPos) > aEdge[0][1]:
					# 	checking_edge_label = self.get_index(checking_string[0])
					# 	if aEdge[1] != None and read[aEdge[1].atcg[checking_edge_label][0][0]] == checking_string[0]:
					# 		aNode = aEdge[1]
					# 		aEdge = aNode.atcg[checking_edge_label]
					# 		aPos = 1
					# 		break
					else:
						# for k in range(rem, 0, -1):
						inserting_prefix = read[i-rem+1:i+1]
						print("inserting prefix:", inserting_prefix)
						new_edge_label = self.get_index(inserting_prefix[-1])
						# This shouldn't be in an if loop...
						if read[aEdge[0][0]+aPos] != inserting_prefix[0]:
							#create internal node
							aEdge[1] = Node()
							aEdge[1].atcg[new_edge_label] = [[i, self.end], None]
							branch_edge_label = self.get_index(read[aEdge[0][0]+aPos])
							aEdge[1].atcg[branch_edge_label] = [[aEdge[0][0]+aPos, aEdge[0][1]], None]
							aPos -= 1
							aEdge[0] = [aEdge[0][0], aEdge[0][0]+aPos]
							if(first == False):
								first = True
								prevNode = aEdge[1]
							else:
								aEdge[1].suffixLink = prevNode
								prevNode = aEdge[1]
							if aNode != self.root and aNode.suffixLink != None:
								aNode = aNode.suffixLink
							elif aNode !=self.root and aNode.suffixLink == None:
								aNode = self.root
								switchup_edge_label = self.get_index(read[aEdge[0][0]])
								aEdge = aNode.atcg[switchup_edge_label]
							elif aNode == self.root:
								new_active_edge = self.get_index(inserting_prefix[1])
								aEdge = aNode.atcg[new_active_edge]
						elif read[aEdge[0][0]+aPos] == inserting_prefix[0]:
							continue_on = True
							break
						rem -= 1
						if(rem == 1):
							aNode = self.root
							aEdge = None 
							aPos = 0

		print("final rem:", rem)
			
			


end = End()
tree = SuffixTree("atgatgcatgcatgactgac", end)
print(tree.root.atcg)

