# -*- coding: utf-8 -*-
"""
Created on Thu Jan  7 09:29:24 2021

@author: Li long long
"""

# Python3 Program to print BFS traversal
# from a given source vertex. BFS(int s)
# traverses vertices reachable from s.
from collections import defaultdict

# This class represents a directed graph
# using adjacency list representation
class Graph:

	# Constructor
	def __init__(self):

		# default dictionary to store graph
		self.graph = defaultdict(list)

	# function to add an edge to graph
	def addEdge(self,u,v):
		self.graph[u].append(v)

	# Function to print a BFS of graph
	def BFS(self, s):

		# Mark all the vertices as not visited
		visited = [False] * (max(self.graph) + 1)

		# Create a queue for BFS
		queue = []

		# Mark the source node as 
		# visited and enqueue it
		queue.append(s)
		visited[s] = True

		while queue:
			# Dequeue a vertex from
			# queue and print it
			Adj = []
			s = queue.pop(0)
			Adj.append(s)
			print (s, end = " ")

			# Get all adjacent vertices of the
			# dequeued vertex s. If a adjacent
			# has not been visited, then mark it
			# visited and enqueue it
			for i in self.graph[s]:
				if visited[i] == False:
					queue.append(i)
					visited[i] = True
			

# Driver code

# Create a graph given in
# the above diagram
# g = Graph()
# g.addEdge(0, 1)
# g.addEdge(0, 2)
# g.addEdge(1, 2)
# g.addEdge(2, 0)
# g.addEdge(2, 3)
# g.addEdge(3, 3)

# print ("Following is Breadth First Traversal"
# 				" (starting from vertex 2)")
# g.BFS(2)

# This code is contributed by Neelam Yadav

f = open("0.edges", "r")
G = Graph()
lines = f.readlines()
for line in lines:
    tmp = line.strip().split(' ')
    G.addEdge(int(tmp[0]), int(tmp[1]))
print ("Following is Breadth First Traversal"
				" (starting from vertex 1)")
G.BFS(1)