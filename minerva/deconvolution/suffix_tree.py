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
	def __init__(self, parent=None):
		#			  a(Edge, Node)  t 				c 			g 	 			CHAR
		self.atcg = [[None, None], [None, None], [None, None], [None, None], [None, None]]
		# only four characters 
		self.suffixLink = None
		self.parent = parent

class SuffixTree:
	def __init__(self, readList):
		self.root = Node()
		self.end = End()
		self.data = readList
		self.add_endings()
		self.build_tree(self.full_string())

	def numReads(self):
		return len(self.data)

	def full_string(self):
		return ''.join(self.data)	

	def add_endings(self):
		for i in range(len(self.data)):
			if i+33 < 65:
				self.data[i] += chr(i+33)
			elif i+33 >= 65:
				self.data[i] += chr(i+95)

	def get_index(self, character):
		if character == 'A':
			return 0
		if character == 'T':
			return 1
		elif character == 'C':
			return 2
		elif character == 'G':
			return 3
		else:
			return 4

	def other_implementation(self, current, visited, full_string,depth = 0):
		visited.add(current)
		for i in range(len(current.atcg)):

			if current.atcg[i][0] != None:
				start, end = current.atcg[i][0][0], current.atcg[i][0][1] 
				char ="Terminator"
				if i == 0:
					char = "A"
				elif i == 1:
					char = "T"
				elif i == 2:
					char = "C"
				elif i == 3:
					char = "G"
				print("depth:" + str(depth) + '\t' + char + "\t", start,end, ":", full_string[start:end+1])
				if current.atcg[i][1] != None:
					depth += 1
					self.other_implementation(current.atcg[i][1], visited, full_string, depth)
					depth -= 1



	def walk_dfs(self, current, visited=None,char=""):
		if visited is None:
			visited = set()
		visited.add(current)
		counter = 0

		while(  counter < len(current.atcg) and  current.atcg[counter][1] == None):
			pew = 'A'
			if(current.atcg[counter][0] != None):
				if counter == 1:
					pew = 'T'
				elif counter == 2:
					pew = 'C'
				elif counter == 3:
					pew = 'G'

				start,end = current.atcg[counter][0][0], current.atcg[counter][0][1]
				print(pew + "\t", start,end, ":", current.data[start:end])
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
				self.walk_dfs(current.atcg[i][1], visited,char)
		return visited

	def search(self, kmer):
		if len(kmer) == 0:
			return False
		aNode = self.root
		aPos = 0
		aEdge = aNode.atcg[self.get_index(kmer[0])]
		string = self.full_string()
		for i in range(len(kmer)):
			if aEdge[0] == None or string[aEdge[0][0] + aPos] != kmer[i]:
				return False
			elif aPos + aEdge[0][0] > aEdge[0][1]:
				aNode = aEdge[1]
				aEdge = aNode.atcg[self.get_index(kmer[i])]
			else:
				aPos += 1
		return True


	def build_tree(self, read):
		aNode = self.root
		aEdge = None  #active edge
		aPos = 0 # active position
		rem = 0
		for i in range(len(read)):
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
						aNode.atcg[edge_label] = [[i, self.end], None] 
						#initialize current letter new node
						rem -= 1
						if aNode.suffixLink != None:
							aNode = aNode.suffixLink
							aEdge = None
							aPos = 0
						else:
							aNode = self.root
							if rem > 0:
								inserting_prefix = read[i-rem+1:i+1]
								aEdge = aNode.atcg[self.get_index(inserting_prefix[0])]
								for k in range(rem - 1):
									if aEdge[0][1] != self.end and aEdge[0][0] + aPos == aEdge[0][1]:
										aNode = aEdge[1]
										aEdge = aNode.atcg[self.get_index(inserting_prefix[k+1])]
										aPos = 0
									else:
										aPos += 1
					elif (aEdge == None or aEdge[0] == None) and aNode.atcg[edge_label][0] != None:
						# if node has been initialized  
						aEdge = aNode.atcg[edge_label]
						#set active edge
						aPos = 1
						if  aEdge[0][1] != self.end and aEdge[0][0] + aPos > aEdge[0][1]:
							#whats the point of checking [0][1] != end 
							# edge + apos > edge[0][1] means not valid
							aNode = aEdge[1]

							aEdge = None
							aPos = 0
							#reset
						break
					elif aEdge[0] != None:
						#has been initialized
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
						inserting_prefix = read[i-rem+1:i+1]
						# print("inserting prefix:", inserting_prefix)
						new_edge_label = self.get_index(inserting_prefix[-1])
						# This shouldn't be in an if loop...
						# if read[aEdge[0][0]+aPos] != inserting_prefix[-1]:
						#create internal node
						prev = aEdge[1]
						aEdge[1] = Node()
						#creating a new node at active position
						aEdge[1].atcg[new_edge_label] = [[i, self.end], None]
						branch_edge_label = self.get_index(read[aEdge[0][0]+aPos])
						aEdge[1].atcg[branch_edge_label] = [[aEdge[0][0]+aPos, aEdge[0][1]], prev] 
						#changed second value from None to aEdge[1]
						# I dont think im supposed to update aPos just yet here.
						aPos -= 1
						rem -=1 
						aEdge[0] = [aEdge[0][0], aEdge[0][0]+aPos]
						if(first == False):
							first = True
							prevNode = aEdge[1]
						else:
							prevNode.suffixLink = aEdge[1] # THIS SHOULD BE prevNode.sufflink = aEdge[1]
							prevNode = aEdge[1]

						if aNode != self.root and aNode.suffixLink != None:
							aPos += 1
							scanning_suffix = read[aEdge[0][0]:(aEdge[0][0] + aPos)] + read[i]
							scanning_edge_label = self.get_index(scanning_suffix[0])
							print("scanning_suffix:", scanning_suffix, aPos, read[aEdge[0][0]:aEdge[0][1]+1])
							# if read[aEdge[0][0]+aPos] == read[i]:
							# 	aPos += 1
							# 	if  aEdge[0][1] != self.end and aEdge[0][0] + aPos > aEdge[0][1]:
							# 		aNode = aEdge[1]
							# 		aEdge = None
							# 		aPos = 0
							# 	#hit rule stopper increment active position do nothing
							# 	break   
							aNode = aNode.suffixLink
							aEdge = aNode.atcg[scanning_edge_label]
							# Need to do a scan on the suffixLinked Edge
							pew = aPos
							aPos = 0
							if aEdge[0] != None:
								for k in range(len(scanning_suffix)-1):
									if aPos + aEdge[0][0] == aEdge[0][1]:
										aNode = aEdge[1]
										aEdge = aEdge = aNode.atcg[self.get_index(scanning_suffix[k+1])]
										aPos = 0
									else:
										aPos += 1
						elif aNode !=self.root and aNode.suffixLink == None:
							aNode = self.root
						if aNode == self.root:
							aPos = 0
							scanning_suffix = read[i-rem+1:i+1]
							aEdge = aNode.atcg[self.get_index(scanning_suffix[0])]
							for k in range(rem - 1):
								if aPos+aEdge[0][0] == aEdge[0][1]:
									aNode = aEdge[1]
									aEdge = aNode.atcg[self.get_index(scanning_suffix[k+1])]
									aPos = 0
								else:
									aPos += 1
						if(rem == 0): # should be if rem == 0
							aNode = self.root
							aEdge = None 
							aPos = 0
		# print("Apos:", aPos)
		# print("final rem:", rem)

			


# end = End()
# tree = SuffixTree("ATCGTTCTGC$", end)
# tree = SuffixTree(["TCATTAGTCGGTTCATCTAAAAGGAGTACATTAAGTTTATGAACAAGTAAACGCAATAAATACAGACGCTTTTGTTCTCCCCCTGAGAGTTTATAAACTTTTTTACCGTGTGTAGCGCTCGGAAATA"])
# # ATTATATTATAAAAAAAAAATATTATTA

# temp = tree.root.atcg
# print("display root",tree.root.atcg)
# # print("display second node",tree.root.atcg[1][1].atcg)
# # print("display second node",tree.root.atcg[2][1].atcg)
# # print("display third node",tree.root.atcg[1][1].atcg[2][1].atcg)
# result = tree.other_implementation(tree.root, set(),tree.full_string())
# counter = 0
# length = len(tree.data)
# print(len(tree.data))







