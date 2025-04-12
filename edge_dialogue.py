import tkinter as tk
from tkinter import simpledialog

class EdgeDialog(simpledialog.Dialog):
    def body(self, master):
        self.title("Add Edge")

        tk.Label(master, text="Edge Weight:").grid(row=0, column=0, sticky="w")
        self.weight_entry = tk.Entry(master)
        self.weight_entry.insert(0, "1")
        self.weight_entry.grid(row=0, column=1)

        self.directed_var = tk.IntVar()
        self.directed_checkbox = tk.Checkbutton(
            master, text="Directed", variable=self.directed_var
        )
        self.directed_checkbox.grid(row=1, columnspan=2, sticky="w")

        return self.weight_entry

    def apply(self):
        try:
            self.weight = float(self.weight_entry.get())
        except ValueError:
            self.weight = 1 

        self.directed = bool(self.directed_var.get())
        self.result = (self.weight, self.directed)
        print(f"EdgeDialog: result set to {self.result}")