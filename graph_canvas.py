import tkinter as tk
from tkinter import simpledialog
from node import Node
from edge import Edge
from graph import Graph
from edge_dialogue import EdgeDialog

class GraphCanvas:
    def __init__(self, root):
        self.root = root
        self.canvas = tk.Canvas(root, width=1920, height=1080, bg="white")
        self.canvas.pack()

        self.graph = Graph()
        self.selected_nodes_for_edge = []
        self.dragging_node = None
        self.node_counter = 0
        self.delete_mode = False

        self.canvas.bind("<Button-1>", self.on_left_click)
        self.canvas.bind("<B1-Motion>", self.on_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_release)
        self.canvas.bind("<Button-3>", self.on_right_click)
        self.canvas.bind("<B3-Motion>", self.on_drag)

        self.left_pressed = False
        self.right_pressed = False

        self.delete_button = tk.Button(root, text="Toggle Delete Mode", command=self.toggle_delete_mode)
        self.delete_button.pack()
        self.clear_button = tk.Button(root, text="Clear Canvas", command=self.clear_canvas)
        self.clear_button.pack(side=tk.TOP, pady=10)

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
        
        if self.delete_mode:
            if node:
                self.delete_node(node)
            return 

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
        node = Node(x, y, self.canvas, self.node_counter)
        self.graph.add_node(node)
        self.node_counter += 1

    def draw_edge(self, node1, node2):
        dialog = EdgeDialog(self.root)
        if dialog.result == 'cancel':
            return
        weight = getattr(dialog, 'weight', 1)
        directed = getattr(dialog, 'directed', False)
        edge = Edge(node1, node2, self.canvas, weight, directed)
        self.graph.add_edge(edge)
        
    def delete_node(self, node):
        print(f"Deleting node {node.id}")
        self.graph.remove_node(node) 
        node.delete_from_canvas()

    def get_node_at(self, x, y):
        for node in self.graph.nodes:
            if node.contains_point(x, y):
                return node
        return None

    def update_canvas(self):
        for edge in self.graph.edges:
            edge.update_edge()
        for node in self.graph.nodes:
            node.update_position()

    def reset_buttons(self):
        self.left_pressed = False
        self.right_pressed = False

    def toggle_delete_mode(self):
        self.delete_mode = not self.delete_mode
        status = "ON" if self.delete_mode else "OFF"
        self.delete_button.config(text=f"Delete Mode: {status}")
    
    def clear_canvas(self):
        for edge in self.graph.edges:
            edge.delete_from_canvas()
        for node in self.graph.nodes:
            node.delete_from_canvas()
        self.graph.nodes.clear()
        self.graph.edges.clear()
        self.node_counter = 0

