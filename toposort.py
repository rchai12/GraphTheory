class TopoSort:
    def __init__(self, graph):
        self.graph = graph
        self.visited = set()
        self.stack = []
        self.steps = []

    def traverse(self):
        for node in self.graph.nodes:
            if node not in self.visited:
                self._dfs(node)
        self.stack.reverse()
        return self.steps

    def _dfs(self, node):
        self.visited.add(node)
        self.steps.append(('node', node))

        for neighbor in self.graph.get_neighbors(node):
            self.steps.append(('edge', (node, neighbor)))
            if neighbor not in self.visited:
                self._dfs(neighbor)

        self.stack.append(node)  # ordering is built in reverse

