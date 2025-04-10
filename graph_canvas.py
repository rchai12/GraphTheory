import tkinter as tk
from tkinter import simpledialog
from node import Node
from edge import Edge
from graph import Graph
from edge_dialogue import EdgeDialog

class GraphCanvas:
    def __init__(self, root):
        self.root = root
        self.canvas = tk.Canvas(root, width=600, height=400, bg="white")
        self.canvas.pack()

        self.graph = Graph()
        self.selected_nodes_for_edge = []
        self.dragging_node = None

        self.canvas.bind("<Button-1>", self.on_left_click)
        self.canvas.bind("<B1-Motion>", self.on_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_release)
        self.canvas.bind("<Button-3>", self.on_right_click)
        self.canvas.bind("<B3-Motion>", self.on_drag)

        self.left_pressed = False
        self.right_pressed = False

    def check_for_delete(self, event):
        if event.num == 1:
            self.left_pressed = True
        elif event.num == 3:
            self.right_pressed = True

        if self.left_pressed and self.right_pressed:
            node = self.get_node_at(event.x, event.y)
            if node:
                self.delete_node(node)
        self.root.after(100, self.reset_buttons)

    def on_left_click(self, event):
        node = self.get_node_at(event.x, event.y)
        
        if not node:
            self.create_node(event.x, event.y)
        elif len(self.selected_nodes_for_edge) == 0:
            self.selected_nodes_for_edge.append(node)
        elif len(self.selected_nodes_for_edge) == 1:
            self.selected_nodes_for_edge.append(node)
            self.draw_edge(self.selected_nodes_for_edge[0], self.selected_nodes_for_edge[1])
            self.selected_nodes_for_edge.clear()  

    def on_right_click(self, event):
        node = self.get_node_at(event.x, event.y)
        if node:
            self.dragging_node = node

    def on_drag(self, event):
        if self.dragging_node:
            self.dragging_node.x = event.x
            self.dragging_node.y = event.y
            self.update_canvas()

    def on_release(self, event):
        self.dragging_node = None

    def create_node(self, x, y):
        node = Node(x, y, self.canvas)
        self.graph.add_node(node)

    def draw_edge(self, node1, node2):
        dialog = EdgeDialog(self.root)
        weight = getattr(dialog, 'weight', 1)
        directed = getattr(dialog, 'directed', False)
        edge = Edge(node1, node2, self.canvas, weight, directed)
        self.graph.add_edge(edge)

    def delete_node(self, node):
        edges_to_remove = [
            edge for edge in self.graph.edges
            if edge.node1 == node or edge.node2 == node
        ]
        for edge in edges_to_remove:
            self.canvas.delete(edge.id)
            self.canvas.delete(edge.weight_text_id)
            self.graph.remove_edge(edge)
        self.canvas.delete(node.id)
        self.graph.remove_node(node)

    def get_node_at(self, x, y):
        for node in self.graph.nodes:
            if node.contains_point(x, y):
                return node
        return None

    def update_canvas(self):
        for edge in self.graph.edges:
            self.canvas.coords(
                edge.id,
                edge.node1.x, edge.node1.y,
                edge.node2.x, edge.node2.y
            )

            mid_x = (edge.node1.x + edge.node2.x) / 2
            mid_y = (edge.node1.y + edge.node2.y) / 2
            self.canvas.coords(edge.weight_text_id, mid_x, mid_y)

        for node in self.graph.nodes:
            self.canvas.coords(
                node.id,
                node.x - node.radius, node.y - node.radius,
                node.x + node.radius, node.y + node.radius
            )

    def reset_buttons(self):
        self.left_pressed = False
        self.right_pressed = False