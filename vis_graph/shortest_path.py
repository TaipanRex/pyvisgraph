"""
The MIT License (MIT)

Copyright (c) 2016 Christian August Reksten-Monsen

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
from graph import Point, Edge, Graph
from visible_vertices import edge_distance


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
