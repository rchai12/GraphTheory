import tkinter as tk
import math

class Edge:
    def __init__(self, node1, node2, canvas, weight=1, directed = True):
        self.node1 = node1
        self.node2 = node2
        self.canvas = canvas
        self.weight = weight
        self.directed = directed

        print(f"Drawing edge from ({node1.x}, {node1.y}) to ({node2.x}, {node2.y})")
        self.id = self.canvas.create_line(
            node1.x, node1.y, node2.x, node2.y,
            fill="gray", width=2,
            arrow=tk.LAST if self.directed else None
        )
        print(f"Edge ID: {self.id}")

        mid_x = (node1.x + node2.x) / 2
        mid_y = (node1.y + node2.y) / 2
        self.weight_text_id = self.canvas.create_text(
            mid_x, mid_y,
            text=str(self.weight),
            fill="black",
            font=("Arial", 10)
        )
        print(f"Weight text ID: {self.weight_text_id}")
    
    def is_point_near(self, x, y, tolerance=10):
        x1, y1 = self.node1.x, self.node1.y
        x2, y2 = self.node2.x, self.node2.y
        num = abs((y2 - y1) * x - (x2 - x1) * y + x2 * y1 - y2 * x1)
        den = math.hypot(y2 - y1, x2 - x1)
        distance = num / den if den != 0 else float('inf')
        return distance <= tolerance

    def update_edge(self):
        self.canvas.coords(self.id, self.node1.x, self.node1.y, self.node2.x, self.node2.y)
        
        mid_x = (self.node1.x + self.node2.x) / 2
        mid_y = (self.node1.y + self.node2.y) / 2
        self.canvas.coords(self.weight_text_id, mid_x, mid_y)

    def delete_from_canvas(self):
        self.canvas.delete(self.id)
        self.canvas.delete(self.weight_text_id)
    
    def highlight(self, color):
        self.canvas.itemconfig(self.id, fill=color)
        self.canvas.itemconfig(self.weight_text_id, fill=color)

    def reset_color(self):
        self.canvas.itemconfig(self.id, fill = "grey")
        self.canvas.itemconfig(self.weight_text_id, fill = "black")

    def update(self, new_weight=None, new_directed=None):
        if new_weight is not None:
            self.weight = new_weight
            self.canvas.itemconfig(self.weight_text_id, text=str(self.weight))
        if new_directed is not None:
            self.directed = new_directed
            self.canvas.delete(self.id)
            self.canvas.delete(self.weight_text_id)
            self.id = self.canvas.create_line(
                self.node1.x, self.node1.y, self.node2.x, self.node2.y,
                fill="gray", width=2,
                arrow=tk.LAST if self.directed else None
            )
            mid_x = (self.node1.x + self.node2.x) / 2
            mid_y = (self.node1.y + self.node2.y) / 2
            self.weight_text_id = self.canvas.create_text(
                mid_x, mid_y,
                text=str(self.weight),
                fill="black",
                font=("Arial", 10)
            )

    def highlight_selected(self):
        self.highlight("orange")