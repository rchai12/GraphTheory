class BellmanFord:
    def __init__(self, graph):
        self.graph = graph

    def traverse(self, start_node):
        distance = {node: float('inf') for node in self.graph.get_nodes()}
        distance[start_node] = 0
        steps = [('node', start_node)]

        for _ in range(len(self.graph.get_nodes()) - 1):
            for u, v, w in self.graph.get_edges():
                if distance[u] + w < distance[v]:
                    distance[v] = distance[u] + w
                    steps.append(('edge', (u, v)))
                    steps.append(('node', v))

        # Optional: Detect negative-weight cycles
        for u, v, w in self.graph.get_edges():
            if distance[u] + w < distance[v]:
                raise ValueError("Graph contains a negative-weight cycle")

        return steps