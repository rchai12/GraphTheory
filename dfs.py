def dfs(graph, start, visited=None, traversal=None):
    if visited is None:
        visited = set()
    if traversal is None:
        traversal = []

    if start not in visited:
        visited.add(start)
        traversal.append(start)
        for neighbor in graph.get(start, []):
            dfs(graph, neighbor, visited, traversal)

    return traversal
