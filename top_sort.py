from tkinter import messagebox

class TopSort:
    def __init__(self, graph):
        self.graph = graph
        self.visited = set()
        self.stack = []
        self.steps = []
        self.rec_stack = set()

    def traverse(self, start_node):
        if start_node:
            self._dfs(start_node)
        for node in self.graph.nodes:
            if node not in self.visited:
                self._dfs(node)
        self.stack.reverse()
        return self.steps

    def _dfs(self, node):
        self.visited.add(node)
        self.rec_stack.add(node)
        self.steps.append(('node', node))
        for neighbor in self.graph.get_neighbors(node):
            self.steps.append(('edge', (node, neighbor)))
            if neighbor in self.rec_stack:
                messagebox.showinfo("Cycle Detected!", f"Cycle detected at edge {node.id} -> {neighbor.id}")
                raise ValueError(f"Cycle detected at edge {node.id} -> {neighbor.id}")
            if neighbor not in self.visited:
                self._dfs(neighbor)
        self.rec_stack.remove(node)
        self.stack.append(node)  # ordering is built in reverse

