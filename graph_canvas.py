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
from Dijkstra import Dijkstra
from bellmanFord import BellmanFord
from edit_edge_dialogue import EditEdgeDialog
import json

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
        self.edit_mode = False


        self.canvas.bind("<Button-1>", self.on_left_click)
        self.canvas.bind("<ButtonRelease-3>", self.on_release)
        self.canvas.bind("<Button-3>", self.on_right_click)
        self.canvas.bind("<B3-Motion>", self.on_drag)

        self.left_pressed = False
        self.right_pressed = False

        self.button_frame = tk.Frame(root)
        self.button_frame.pack(pady=1)
        self.delete_button = tk.Button(root, text="Toggle Delete Mode", command=self.toggle_delete_mode)
        self.delete_button.pack(side=tk.LEFT, padx=5)
        self.edit_button = tk.Button(root, text="Toggle Edit Mode", command=self.toggle_edit_mode)
        self.edit_button.pack(side=tk.LEFT, padx=5)
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
        self.dijkstra_button = tk.Button(root, text="Run Dijkstra's Algorithm", command=self.run_dijkstra)
        self.dijkstra_button.pack(side=tk.LEFT, padx=5)
        self.bellman_ford_button = tk.Button(root, text="Run Bellman Ford's Algorithm", command=self.run_bellman_ford)
        self.bellman_ford_button.pack(side=tk.LEFT, padx=5)
        # add save button
        self.save_button = tk.Button(root, text="Save Graph", command=self.save_graph)
        self.save_button.pack(side=tk.LEFT, padx=5)
def on_left_click(self, event):
        # ... existing code ...
        pass  # existing implementation

    # ... other existing methods ...

    def toggle_edit_mode(self):
        self.edit_mode = not self.edit_mode
        status = "ON" if self.edit_mode else "OFF"
        self.edit_button.config(text=f"Edit Mode: {status}")

    def save_graph(self):
        """
        Save the current graph (nodes and edges) to a JSON file.
        """
        graph_data = {
            "nodes": [
                {"id": node.id, "x": node.x, "y": node.y}
                for node in self.graph.nodes
            ],
            "edges": [
                {
                    "from": edge.node1.id,
                    "to": edge.node2.id,
                    "weight": edge.weight,
                    "directed": edge.directed
                }
                for edge in self.graph.edges
            ]
        }

        file_path = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json")],
            title="Save Graph As..."
        )

        if not file_path:
            return

        with open(file_path, "w") as f:
            json.dump(graph_data, f, indent=4)

        messagebox.showinfo("Save Successful", f"Graph saved to {file_path}")

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
        if self.edit_mode:
            edge = self.get_edge_at(event.x, event.y)
            if edge:
                self.edit_edge(edge)
                return
        node = self.get_node_at(event.x, event.y)
        if not node:
            self.create_node(event.x, event.y)
        elif len(self.selected_nodes_for_edge) == 0:
            self.selected_nodes_for_edge.append(node)
            node.highlight_selected()
        elif len(self.selected_nodes_for_edge) == 1:
            self.selected_nodes_for_edge.append(node)
            node.highlight_selected()
            self.draw_edge(self.selected_nodes_for_edge[0], self.selected_nodes_for_edge[1])
            self.selected_nodes_for_edge[0].reset_color()
            node.reset_color()
            self.selected_nodes_for_edge.clear()  

    def on_right_click(self, event):
        node = self.get_node_at(event.x, event.y)
        if node:
            node.highlight_selected()
            self.dragging_node = node

    def on_drag(self, event):
        if self.dragging_node:
            self.dragging_node.x = event.x
            self.dragging_node.y = event.y
            self.update_canvas()

    def on_release(self, event):
        if self.dragging_node:
            self.dragging_node.reset_color()
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
            try:
                steps = top_sort.traverse(node)
                traversal_ids = [step[1].id for step in steps if step[0] == 'node']
                sorted_ids = [node.id for node in top_sort.stack]
                self.animate_traversal(steps, lambda: self.show_top_sort_result(traversal_ids))
                messagebox.showinfo("Topological Sort Traversal", f"Order: {traversal_ids}\nTopological Sort Result: {sorted_ids}")
            except ValueError as e:
                messagebox.showerror("Cycle Detected", str(e)) 
                print("Cycle detected during topological sort, aborting operation.")
            self.canvas.unbind("<Button-1>")
            self.canvas.bind("<Button-1>", self.on_left_click)

    def run_dijkstra(self):
        self.canvas.bind("<Button-1>", self.select_dijkstra_start)
        messagebox.showinfo("Pick a Node", "Click on a node to start Dijkstra's Algorithm...")


    def select_dijkstra_start(self, event):
        print(f"Dijkstra: Click at ({event.x}, {event.y})")
        node = self.get_node_at(event.x, event.y)
        if node:
            print(f"Selected node {node.id} for Dijkstra")
            dijkstra = Dijkstra(self.graph)
            try: 
                steps, distances = dijkstra.run(node)
                traversal_ids = [step[1].id for step in steps if step[0] == 'node']
                self.animate_traversal(steps, lambda: messagebox.showinfo("Dijkstra Traversal", f"Visit Order: {traversal_ids}"))
                dist_str = "\n".join(f"Node {nid}: {dist:.2f}" for nid, dist in distances.items())
                messagebox.showinfo(f"Minimum Distances for {node.id}", f"{dist_str}")
            except ValueError as e:
                messagebox.showerror("Error Detected", str(e)) 
                print("Error detected during Dijkstra's algorithm, aborting operation.")
            self.canvas.unbind("<Button-1>")
            self.canvas.bind("<Button-1>", self.on_left_click)

    def run_bellman_ford(self):
        self.canvas.bind("<Button-1>", self.select_bellman_ford_start)
        messagebox.showinfo("Pick a Node", "Click on a node to start Bellman Ford's Algorithm...")


    def select_bellman_ford_start(self, event):
        print(f"Bellman Ford: Click at ({event.x}, {event.y})")
        node = self.get_node_at(event.x, event.y)
        if node:
            print(f"Selected node {node.id} for Bellman Ford")
            bellmanFord = BellmanFord(self.graph)
            try:
                steps, distances = bellmanFord.run(node)
                traversal_ids = [step[1].id for step in steps if step[0] == 'node']
                self.animate_traversal(steps, lambda: messagebox.showinfo("Bellman Ford's Traversal", f"Visit Order: {traversal_ids}"))
                dist_str = "\n".join(f"Node {nid}: {dist:.2f}" for nid, dist in distances.items())
                messagebox.showinfo(f"Minimum Distances for {node.id}", f"{dist_str}")
            except ValueError as e:
                messagebox.showerror("Error Detected", str(e)) 
                print("Error detected during Bellman Ford's algorithm, aborting operation.")
            self.canvas.unbind("<Button-1>")
            self.canvas.bind("<Button-1>", self.on_left_click)

    def reset_colors(self):
        for node in self.graph.nodes:
            node.reset_color()
        for edge in self.graph.edges:
            edge.reset_color()

    def toggle_edit_mode(self):
        self.edit_mode = not self.edit_mode
        status = "ON" if self.edit_mode else "OFF"
        self.edit_button.config(text=f"Edit Mode: {status}")

    def edit_edge(self, edge):
        edge.highlight_selected()
        edit_dialog = EditEdgeDialog(self.root, edge)
        if edit_dialog.result is not None:
            weight, directed = edit_dialog.result
            edge.weight = weight
            edge.directed = directed
            self.update_canvas() 
        edge.reset_color()