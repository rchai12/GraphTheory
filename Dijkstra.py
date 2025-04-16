import heapq

class Dijkstra:
    def __init__(self, graph):
        self.graph = graph

    def run(self, start):
        # Use node.id to avoid hashing issues.
        distances = {node.id: float('inf') for node in self.graph.nodes}
        distances[start.id] = 0

        steps = []
        # Use a tie-breaker (node.id) in the heap tuple.
        heap = [(0, start.id, start)]
        
        while heap:
            current_distance, _, current_node = heapq.heappop(heap)
            
            if current_distance > distances[current_node.id]:
                continue
            
            # Record that we've "visited" this node.
            steps.append(('node', current_node))
            
            # Iterate over all edges in the graph.
            for edge in self.graph.edges:
                # Check for an outgoing edge: current_node is node1
                if edge.node1 == current_node:
                    neighbor = edge.node2
                    new_distance = current_distance + edge.weight
                    if new_distance < distances[neighbor.id]:
                        distances[neighbor.id] = new_distance
                        heapq.heappush(heap, (new_distance, neighbor.id, neighbor))
                        steps.append(('edge', (current_node, neighbor)))
                        
                # If the edge is undirected, also check for current_node as node2.
                if not edge.directed and edge.node2 == current_node:
                    neighbor = edge.node1
                    new_distance = current_distance + edge.weight
                    if new_distance < distances[neighbor.id]:
                        distances[neighbor.id] = new_distance
                        heapq.heappush(heap, (new_distance, neighbor.id, neighbor))
                        steps.append(('edge', (current_node, neighbor)))
                        
        return steps
