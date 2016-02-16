from graph import Point, Edge, Polygon, Graph, edge_distance


# TODO: If two nodes have the same distance, will the algorithm break?
def shortest_path(graph, ship, port):
    visited = []
    not_visited = graph.get_points()
    not_visited.append(ship)
    distance = {point: float('inf') for point in not_visited}
    distance[port] = 0

    # Calculate distances
    point = None
    while point != ship:
        point = min(not_visited, key=lambda p: distance[p])
        visited.append(point)
        not_visited.remove(point)

        # Cut off edges to the ship when there is one that is better
        if distance[point] + edge_distance(point, ship) < distance[ship]:
            # TODO: Check visibility between vertex and ship
            if point == Point(8.0, 6.0) or point == Point(10.0, 1.5):
                graph.polygons[0].add_edge(Edge(point, ship))  # TODO: Ugly, add separate Edges?
            # Distance update
            for edge in graph.get_point_edges(point):
                point2 = edge.get_adjacent(point)
                if distance[point2] > distance[point] + edge_distance(point, point2):
                    distance[point2] = distance[point] + edge_distance(point, point2)

    # Return the shortest path
    path = []
    point = ship

    while point != port:
        min_edge = min(graph.get_point_edges(point), key=lambda e: distance[edge.get_adjacent(point)])
        path.append(min_edge)
        point = min_edge.get_adjacent(point)
    return path
