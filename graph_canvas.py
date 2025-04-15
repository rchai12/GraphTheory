import tkinter as tk
from node import Node
from edge import Edge
from graph import Graph
from edge_dialogue import EdgeDialog
from bfs import BFS
import math
from tkinter import messagebox
from dfs import DFS
from top_sort import TopSort

class GraphCanvas:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1280x760")
        self.canvas = tk.Canvas(root, width=1280, height=720, bg="white")
        self.canvas.pack()

        self.graph = Graph()
        self.selected_nodes_for_edge = []
        self.dragging_node = None
        self.node_counter = 0
        self.delete_mode = False

        self.canvas.bind("<Button-1>", self.on_left_click)
        self.canvas.bind("<ButtonRelease-1>", self.on_release)
        self.canvas.bind("<Button-3>", self.on_right_click)
        self.canvas.bind("<B3-Motion>", self.on_drag)

        self.left_pressed = False
        self.right_pressed = False

        self.button_frame = tk.Frame(root)
        self.button_frame.pack(pady=1)
        self.delete_button = tk.Button(root, text="Toggle Delete Mode", command=self.toggle_delete_mode)
        self.delete_button.pack(side=tk.LEFT, padx=5)
        self.clear_button = tk.Button(root, text="Clear Canvas", command=self.clear_canvas)
        self.clear_button.pack(side=tk.LEFT, padx=5)
        self.reset_colors_button = tk.Button(root, text="Reset Colors", command=self.reset_colors)
        self.reset_colors_button.pack(side=tk.LEFT, padx=5)
        self.bfs_button = tk.Button(root, text="Run Breadth-First Search", command=self.run_bfs)
        self.bfs_button.pack(side=tk.LEFT, padx=5)
        self.dfs_button = tk.Button(root, text="Run Depth-First Search", command=self.run_dfs)
        self.dfs_button.pack(side=tk.LEFT, padx=5)
        self.topSort_button = tk.Button(root, text="Run Topological Sort", command=self.run_top_sort)
        self.topSort_button.pack(side=tk.LEFT, padx=5)

    def on_left_click(self, event):
        if self.delete_mode:
            edge = self.get_edge_at(event.x, event.y)
            if edge:
                self.delete_edge(edge)
                return
            node = self.get_node_at(event.x, event.y)
            if node:
                self.delete_node(node)
                return 
        
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
        node = Node(x, y, self.canvas, self.node_counter)
        self.graph.add_node(node)
        self.node_counter += 1

    def draw_edge(self, node1, node2):
        dialog = EdgeDialog(self.root)
        print(f"EdgeDialog: result set to {dialog.result}")
        if dialog.result is None:
            print("Dialog was canceled.")
            return
        weight, directed = dialog.result
        edge = Edge(node1, node2, self.canvas, weight, directed)
        self.graph.add_edge(edge)
        
    def delete_node(self, node):
        print(f"Deleting node {node.id}")
        self.graph.remove_node(node) 

    def delete_edge(self, edge):
        print(f"Deleting edge from {edge.node1.id} to {edge.node2.id}")
        self.graph.remove_edge(edge)

    def get_node_at(self, x, y):
        for node in self.graph.nodes:
            if node.contains_point(x, y):
                return node
        return None

    def get_edge_at(self, x, y):
        for edge in self.graph.edges:
            if self.is_point_near_edge(x, y, edge):
                return edge
        return None
    
    def is_point_near_edge(self, x, y, edge):
        tolerance = 10 
        x1, y1 = edge.node1.x, edge.node1.y
        x2, y2 = edge.node2.x, edge.node2.y
        num = abs((y2 - y1) * x - (x2 - x1) * y + x2 * y1 - y2 * x1)
        den = math.hypot(y2 - y1, x2 - x1)
        distance = num / den if den != 0 else float('inf')
        return distance <= tolerance

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
        self.graph.delete_graph()
        self.node_counter = 0

    def run_bfs(self):
        self.canvas.bind("<Button-1>", self.select_bfs_start)
        messagebox.showinfo("Pick a Node", f"Click on a node to start BFS traversal...")

    def select_bfs_start(self, event):
        print(f"Clicked at ({event.x}, {event.y})") 
        node = self.get_node_at(event.x, event.y)
        if node:
            print(f"Selected node {node.id} for BFS")
            bfs = BFS(self.graph)
            steps = bfs.traverse(node)
            traversal_ids = [step[1].id for step in steps if step[0] == 'node']
            self.animate_traversal(steps, lambda: self.show_bfs_result(traversal_ids))
            messagebox.showinfo("BFS Traversal", f"Order: {traversal_ids}")
            self.canvas.unbind("<Button-1>")
            self.canvas.bind("<Button-1>", self.on_left_click)

    def animate_traversal(self, steps, on_complete=None, index=0):
        if index >= len(steps):
            if on_complete:
                on_complete()
            return
        step_type, item = steps[index]
        if step_type == 'node':
            item.highlight("red")
        elif step_type == 'edge':
            node1, node2 = item
            edge = self.find_edge_between(node1, node2)
            if edge:
                edge.highlight("green")
        self.canvas.after(750, lambda: self.animate_traversal(steps, on_complete, index + 1))
    
    def find_edge_between(self, node1, node2):
        for edge in self.graph.edges:
            if (edge.node1 == node1 and edge.node2 == node2) or (edge.node1 == node2 and edge.node2 == node1):
                return edge
        return None
    
    def run_dfs(self):
        self.canvas.bind("<Button-1>", self.select_dfs_start)
        messagebox.showinfo("Pick a Node", f"Click on a node to start DFS traversal...")

    def select_dfs_start(self, event):
        print(f"Clicked at ({event.x}, {event.y})") 
        node = self.get_node_at(event.x, event.y)
        if node:
            print(f"Selected node {node.id} for BFS")
            dfs = DFS(self.graph)
            steps = dfs.traverse(node)
            traversal_ids = [step[1].id for step in steps if step[0] == 'node']
            self.animate_traversal(steps, lambda: self.show_dfs_result(traversal_ids))
            messagebox.showinfo("DFS Traversal", f"Order: {traversal_ids}")
            self.canvas.unbind("<Button-1>")
            self.canvas.bind("<Button-1>", self.on_left_click)

    def run_top_sort(self):
        self.canvas.bind("<Button-1>", self.select_top_sort_start)
        messagebox.showinfo("Pick a Node", f"Click on a node to start Topological Sort...")

    def select_top_sort_start(self, event):
        print(f"Clicked at ({event.x}, {event.y})") 
        node = self.get_node_at(event.x, event.y)
        if node:
            print(f"Selected node {node.id} for Topological Sort")
            top_sort = TopSort(self.graph)
            steps = top_sort.traverse(node)
            traversal_ids = [step[1].id for step in steps if step[0] == 'node']
            sorted_ids = [node.id for node in top_sort.stack]
            self.animate_traversal(steps, lambda: self.show_top_sort_result(traversal_ids))
            messagebox.showinfo("Topological Sort Traversal", f"Order: {traversal_ids}\nTopological Sort Result: {sorted_ids}")
            self.canvas.unbind("<Button-1>")
            self.canvas.bind("<Button-1>", self.on_left_click)

    def reset_colors(self):
        for node in self.graph.nodes:
            node.reset_color()
        for edge in self.graph.edges:
            edge.reset_color()
