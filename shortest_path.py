from graph import Point, Edge, Graph, edge_distance


# TODO: If two nodes have the same distance, will the algorithm break?
def shortest_path(graph, ship, port):
    visited = []
    not_visited = graph.get_points()
    distance = {point: float('inf') for point in not_visited}
    distance[port] = 0

    # Calculate distances
    point = None
    while point != ship:
        point = min(not_visited, key=lambda p: distance[p])
        if point == ship:
            break
        visited.append(point)
        not_visited.remove(point)

        for edge in graph[point]:
            point2 = edge.get_adjacent(point)
            if distance[point2] > distance[point] + edge_distance(point, point2):
                distance[point2] = distance[point] + edge_distance(point, point2)

    # Return the shortest path
    path = []
    point = ship
    path.append(point)

    # This won't work if the shortest path is ship->port directly
    while (point != port):
        min_edge = min(graph[point], key=lambda e: distance[e.get_adjacent(point)])
        path.append(min_edge.get_adjacent(point))
        point = min_edge.get_adjacent(point)

    return path
