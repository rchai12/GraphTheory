import tkinter as tk
import math

class GraphCanvas:
    def __init__(self, root):
        self.root = root
        self.canvas = tk.Canvas(root, width=600, height=400, bg="white")
        self.canvas.pack()

        self.node_radius = 20
        self.nodes = []
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
        r = self.node_radius
        node_id = self.canvas.create_oval(x - r, y - r, x + r, y + r, fill="skyblue", outline="black")
        self.nodes.append((x, y, node_id))

    def get_node_at(self, x, y):
        for node_x, node_y, node_id in self.nodes:
            if math.hypot(node_x - x, node_y - y) <= self.node_radius:
                return (node_x, node_y)
        return None

    def draw_edge(self, node1, node2):
        x1, y1 = node1
        x2, y2 = node2
        self.canvas.create_line(x1, y1, x2, y2, fill="gray", width=2)

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Node & Edge Canvas")
    app = GraphCanvas(root)
    root.mainloop()
