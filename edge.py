class Edge:
    def __init__(self, node1, node2, canvas):
        self.node1 = node1
        self.node2 = node2
        self.canvas = canvas
        self.id = self.canvas.create_line(
            node1.x, node1.y, node2.x, node2.y,
            fill="gray", width=2
        )
