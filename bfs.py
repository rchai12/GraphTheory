from collections import deque

class BFS:
    def __init__(self, graph):
        self.graph = graph

    def traverse(self, start_node):
        visited = set()
        queue = deque([start_node])
        steps = [('node', start_node)]

        while queue:
            current_node = queue.popleft()
            if current_node not in visited:
                visited.add(current_node)
                for neighbor in self.graph.get_neighbors(current_node):
                    if neighbor not in visited and neighbor not in queue:
                        queue.append(neighbor)
                        steps.append(('edge', (current_node, neighbor))) 
                        steps.append(('node', neighbor)) 
        return steps
