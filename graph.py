from node import Node
from edge import Edge

class Graph:
    def __init__(self):
        self.nodes = []
        self.edges = [] 

    def add_node(self, node):
        self.nodes.append(node)

    def add_edge(self, node1, node2):
        self.edges.append((node1, node2))

    def get_neighbors(self, node):
        return [n2 for n1, n2 in self.edges if n1 == node] + [n1 for n1, n2 in self.edges if n2 == node]
