class DFS:
    def __init__(self, graph):
        self.graph = graph

    def traverse(self, start_node):
        visited = set()
        steps = [('node', start_node)]

        def dfs(node):
            visited.add(node)
            for neighbor in self.graph.get_neighbors(node):
                if neighbor not in visited:
                    steps.append(('edge', (node, neighbor)))
                    steps.append(('node', neighbor))
                    dfs(neighbor)

        dfs(start_node)
        return steps
