import math

class Node:
    def __init__(self, x, y, canvas, radius=20):
        self.x = x
        self.y = y
        self.radius = radius
        self.canvas = canvas
        self.id = self.canvas.create_oval(
            x - radius, y - radius, x + radius, y + radius,
            fill="skyblue", outline="black"
        )

    def contains_point(self, x, y):
        return math.hypot(self.x - x, self.y - y) <= self.radius
