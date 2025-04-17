class BellmanFord:
    def __init__(self, graph):
        self.graph = graph

    def run(self, start_node):
        steps = []
        distances = {node.id: float('inf') for node in self.graph.nodes}
        distances[start_node.id] = 0

        steps.append(('node', start_node))

        for _ in range(len(self.graph.nodes) - 1):
            for edge in self.graph.edges:
                u, v = edge.node1, edge.node2
                weight = edge.weight

                # Relax the edge
                if distances[u.id] + weight < distances[v.id]:
                    distances[v.id] = distances[u.id] + weight
                    steps.append(('node', v))
                    steps.append(('edge', (u, v)))

                if edge.directed and distances[v.id] + weight < distances[u.id]:
                    distances[u.id] = distances[v.id] + weight
                    steps.append(('node', u))
                    steps.append(('edge', (v, u)))

        # Check for negative cycles
        for edge in self.graph.edges:
            u, v = edge.node1, edge.node2
            weight = edge.weight
            if distances[u.id] + weight < distances[v.id] or \
               (edge.directed and distances[v.id] + weight < distances[u.id]):
                raise ValueError("Graph contains a negative weight cycle")

        return steps, distances
