from node import Node
from edge import Edge

class Graph:
    def __init__(self):
        self.nodes = []
        self.edges = [] 

    def add_node(self, node):
        self.nodes.append(node)

    def add_edge(self, edge):
        self.edges.append(edge)

    def get_neighbors(self, node):
        neighbors = []
        for edge in self.edges:
            if edge.node1 == node:
                neighbors.append(edge.node2) 
            elif not edge.directed and edge.node2 == node:
                neighbors.append(edge.node1)
        return neighbors

    def remove_edge(self, edge):
        edge.delete_from_canvas()
        if edge in self.edges:
            self.edges.remove(edge)
    
    def remove_node(self, node):
        edges_to_remove = [
            edge for edge in self.edges
            if edge.node1 == node or edge.node2 == node
        ]
        for edge in edges_to_remove:
            edge.delete_from_canvas()
            self.remove_edge(edge)
        node.delete_from_canvas()
        self.nodes.remove(node)

    def delete_graph(self):
        for edge in self.edges:
            edge.delete_from_canvas()
        for node in self.nodes:
            node.delete_from_canvas()
        self.nodes.clear()
        self.edges.clear()