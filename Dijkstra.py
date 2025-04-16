import heapq

class Dijkstra:
    def __init__(self, graph):
        self.graph = graph

    def run(self, start):
        # Use node.id for the distance mapping
        distances = {node.id: float('inf') for node in self.graph.nodes}
        distances[start.id] = 0

        steps = []
        heap = [(0, start)]
        while heap:
            current_distance, current_node = heapq.heappop(heap)
            if current_distance > distances[current_node.id]:
                continue

            # Record this node as visited
            steps.append(('node', current_node))

            # Consider each edge outgoing from current_node
            for edge in self.graph.edges:
                if edge.node1 == current_node:
                    neighbor = edge.node2
                    new_distance = current_distance + edge.weight
                    if new_distance < distances[neighbor.id]:
                        distances[neighbor.id] = new_distance
                        heapq.heappush(heap, (new_distance, neighbor))
                        # Record the edge relaxation step
                        steps.append(('edge', (current_node, neighbor)))
        return steps
