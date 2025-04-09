import tkinter as tk

class Edge:
    def __init__(self, node1, node2, canvas, weight=1, directed = True):
        self.node1 = node1
        self.node2 = node2
        self.canvas = canvas
        self.weight = weight
        self.directed = directed


        self.id = self.canvas.create_line(
            node1.x, node1.y, node2.x, node2.y,
            fill="gray", width=2,
            arrow=tk.LAST if self.directed else None
        )

        mid_x = (node1.x + node2.x) / 2
        mid_y = (node1.y + node2.y) / 2
        self.weight_text_id = self.canvas.create_text(
            mid_x, mid_y,
            text=str(self.weight),
            fill="black",
            font=("Arial", 10)
        )
