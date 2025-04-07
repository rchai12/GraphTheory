import tkinter as tk
from node import Node
from edge import Edge

class GraphCanvas:
    def __init__(self, root):
        self.root = root
        self.canvas = tk.Canvas(root, width=600, height=400, bg="white")
        self.canvas.pack()

        self.nodes = []
        self.edges = []
        self.selected_nodes = []

        self.canvas.bind("<Button-1>", self.on_click)

    def on_click(self, event):
        clicked_node = self.get_node_at(event.x, event.y)
        
        if clicked_node:
            self.selected_nodes.append(clicked_node)
            if len(self.selected_nodes) == 2:
                self.draw_edge(self.selected_nodes[0], self.selected_nodes[1])
                self.selected_nodes.clear()
        else:
            self.create_node(event.x, event.y)

    def create_node(self, x, y):
        node = Node(x, y, self.canvas)
        self.nodes.append(node)

    def get_node_at(self, x, y):
        for node in self.nodes:
            if node.contains_point(x, y):
                return node
        return None

    def draw_edge(self, node1, node2):
        edge = Edge(node1, node2, self.canvas)
        self.edges.append(edge)

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Node & Edge Canvas")
    app = GraphCanvas(root)
    root.mainloop()
