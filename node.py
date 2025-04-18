import math

class Node:
    def __init__(self, x, y, canvas, node_id = 0, radius=20):
        self.x = x
        self.y = y
        self.radius = radius
        self.canvas = canvas
        self.id = node_id
        self.node_circle = self.canvas.create_oval(
            x - radius, y - radius, x + radius, y + radius,
            fill="skyblue", outline="black"
        )
        self.node_text = self.canvas.create_text(
            self.x, self.y, text=str(self.id), 
            font=('Arial', 12), fill='black'
        )

    def contains_point(self, x, y):
        return math.hypot(self.x - x, self.y - y) <= self.radius
    
    def update_position(self):
        self.canvas.coords(self.node_circle, self.x - self.radius, self.y - self.radius, self.x + self.radius, self.y + self.radius)
        self.canvas.coords(self.node_text, self.x, self.y)

    def delete_from_canvas(self):
        self.canvas.delete(self.node_circle)
        self.canvas.delete(self.node_text)
    
    def highlight(self, color):
        self.canvas.itemconfig(self.node_circle, fill=color)

    def reset_color(self):
        self.canvas.itemconfig(self.node_circle, fill="skyblue")

    def highlight_selected(self):
        self.highlight("orange")