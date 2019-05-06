from minerva.gimmebio.kmers import MinSparseKmerSet
from minerva.gimmebio.readclouds import iterReadClouds
from itertools import combinations
import numpy as np
import sys

class End:  #define global end
	def __init__(self, val = -1):
		self.val = val

	def __str__(self):
		return self.val
	def __repr__(self):
		return str(self.val)
	def __gt__(self, other):  #over load greater than operator 
		return self.val > other.val
	def __str__(self):
		return str(self.val)
	def __index__(self):
		return self.val
	def __int__(self):
		return self.val
	def __add__(self,num):
		return self.val + num


class Node:
	def __init__(self):
		#			  a(Edge, Node)  t 				c 			g 	 
		self.atcg = [[None, None], [None, None], [None, None], [None, None]]
		# only four characters 
		self.suffixLink = None
		self.data = ""

class SuffixTree:
	def __init__(self, readList, End):
		self.root = Node()
		self.root.data = readList
		self.end = End
		self.build_tree(readList)

	def get_index(self, character):
		if character == 'A':
			return 0
		if character == 'T':
			return 1
		elif character == 'C':
			return 2
		elif character == 'G':
			return 3

	def walk_dfs(self,current,visited=None,char=""):
		if visited is None:
			visited = set()
		visited.add(current)
		counter = 0

		while(  counter < len(current.atcg) and  current.atcg[counter][1] == None):
			if(current.atcg[counter][0] != None):
				start,end = current.atcg[counter][0][0],current.atcg[counter][0][1]
				print(start,end)
				print(current.data[start:end+1])
				#while the next field is none, print all the suffixes before that
				# print(current.atcg[counter])
			counter += 1

		for i in range( len(current.atcg)):
			if(current.atcg[i][1] != None and current.atcg[i][1] not in visited):
				start,end = current.atcg[i][0][0], current.atcg[i][0][1]
				char = current.data[start:end+1]
				print(char,current.data[start:end+1],end="")
				#store the current char (this part is incomplete it would be better to store a chararray)
				# print(current.atcg[i][0],current.atcg[i][1])
				# print(current.data[start:end+1])
				self.walk_dfs(current.atcg[i][1],visited,char)
		return visited


	def build_tree(self, read):
		aNode = self.root
		aEdge = None  #active edge
		aPos = 0 # active position
		rem = 0
		for i in range(len(read)):
			print("rem:", rem)
			# print("Node:", aNode,"//Edge:", aEdge,"//Pos:", aPos)
			checking_string = read[:i+1]
			# print("checking_string",checking_string)
			edge_label = self.get_index(read[i])
			# current letter
			#get the edge index 0 =A ETC.
			rem += 1
			self.end.val += 1
			first = False
			prevNode = None

			# Start the Phase
			while rem > 0:
				if aPos == 0:
					if (aEdge == None or aEdge[0] == None) and aNode.atcg[edge_label][0] == None and aNode.atcg[edge_label][1] == None:
						# active edge = none    and active node's current letter has not been initialized
						# print("aedge[0] = ",aEdge[0])
						print("aedge= " ,aEdge)
						aNode.atcg[edge_label] = [[i, self.end], None] 
						#initialize current letter new node
						rem -= 1
					elif (aEdge == None or aEdge[0] == None) and aNode.atcg[edge_label][0] != None:
						# if node has been initialized  
						aEdge = aNode.atcg[edge_label]
						#set active edge
						aPos = 1
						if  aEdge[0][1] != self.end and aEdge[0][0] + aPos > aEdge[0][1]:
							#whats the point of checking [0][1] != end 
							# edge + apos > edge[0][1] means not valid
							print("aedge= " ,aEdge)
							aNode = aEdge[1]

							aEdge = None
							aPos = 0
							#reset
						break
					elif aEdge[0] != None:
						#has been initialized
						print("aedge= " ,aEdge)
						aPos = 1
						if  aEdge[0][1] != self.end and aEdge[0][0] + aPos > aEdge[0][1]:
							#if this is not the last node and this is not the edge that we are looking for
							aNode = aEdge[1]
							aEdge = None
							aPos = 0
							#reset
						break
				else:
					if read[aEdge[0][0]+aPos] == read[i]:
						aPos += 1
						if  aEdge[0][1] != self.end and aEdge[0][0] + aPos > aEdge[0][1]:
							aNode = aEdge[1]
							aEdge = None
							aPos = 0
						#hit rule stopper increment active position do nothing
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
						#  HAVE NO CODE FOR DEALING WITH SUFFIX LINKS AND NOT HAVING ROOT AS SUFFIXLINKS
						print("aedge= " ,aEdge)
						inserting_prefix = read[i-rem+1:i+1]
						# print("inserting prefix:", inserting_prefix)
						new_edge_label = self.get_index(inserting_prefix[-1])
						# This shouldn't be in an if loop...
						# if read[aEdge[0][0]+aPos] != inserting_prefix[-1]:
						#create internal node
						prev = aEdge[1]
						print("prev:", prev)
						aEdge[1] = Node()
						aEdge[1].data = read
						#creating a new node at active position
						aEdge[1].atcg[new_edge_label] = [[i, self.end], None]
						branch_edge_label = self.get_index(read[aEdge[0][0]+aPos])
						aEdge[1].atcg[branch_edge_label] = [[aEdge[0][0]+aPos, aEdge[0][1]], prev] 
						#changed second value from None to aEdge[1]
						aPos -= 1
						aEdge[0] = [aEdge[0][0], aEdge[0][0]+aPos]
						print(aEdge)
						if(first == False):
							first = True
							prevNode = aEdge[1]
						else:
							prevNode.suffixLink = aEdge[1] # THIS SHOULD BE prevNode.sufflink = aEdge[1]
							prevNode = aEdge[1]

						if aNode != self.root and aNode.suffixLink != None:
							aNode = aNode.suffixLink
							linked_edge_label = self.get_index(read[aEdge[0][0]])
							aEdge = aNode.atcg[linked_edge_label]
						elif aNode !=self.root and aNode.suffixLink == None:
							aNode = self.root
							switchup_edge_label = self.get_index(read[aEdge[0][0]])
							aEdge = aNode.atcg[switchup_edge_label]
						elif aNode == self.root:
							new_active_edge = self.get_index(inserting_prefix[1])
							aEdge = aNode.atcg[new_active_edge]
						print("Before:", rem)
						rem -= 1
						if(rem == 0): # should be if rem == 0
							aNode = self.root
							aEdge = None 
							aPos = 0
						print("After:", rem)

		# print("final rem:", rem)

			


end = End()
tree = SuffixTree("ATCGTTCTGC", end)
temp = tree.root.atcg
print("display root",tree.root.atcg)
print("display second node",tree.root.atcg[1][1].atcg)
print("display second node",tree.root.atcg[2][1].atcg)
print("display third node",tree.root.atcg[1][1].atcg[2][1].atcg)
result = tree.walk_dfs(tree.root)
counter = 0
length = len(tree.root.data)
print(len(tree.root.data))







