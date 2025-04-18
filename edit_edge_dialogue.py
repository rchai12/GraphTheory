import tkinter as tk
from tkinter import simpledialog

class EditEdgeDialog(simpledialog.Dialog):
    def __init__(self, parent, edge):
        self.edge = edge 
        super().__init__(parent) 

    def body(self, master):
        self.title("Edit Edge")

        tk.Label(master, text="Edge Weight:").grid(row=0, column=0, sticky="w")
        self.weight_entry = tk.Entry(master)
        self.weight_entry.insert(0, str(self.edge.weight)) 
        self.weight_entry.grid(row=0, column=1)

        self.directed_var = tk.IntVar(value=1 if self.edge.directed else 0) 
        self.directed_checkbox = tk.Checkbutton(
            master, text="Directed", variable=self.directed_var
        )
        self.directed_checkbox.grid(row=1, columnspan=2, sticky="w")

        return self.weight_entry 

    def apply(self):
        try:
            self.weight = float(self.weight_entry.get()) 
        except ValueError:
            self.weight = self.edge.weight 

        self.directed = bool(self.directed_var.get())
        
        self.edge.update(self.weight, self.directed)
        self.result = (self.weight, self.directed)
        
        print(f"EditEdgeDialog: result set to {self.result}") 
