import tkinter as tk
from graph_canvas import GraphCanvas

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Node & Edge Canvas")
    app = GraphCanvas(root)
    root.mainloop()
