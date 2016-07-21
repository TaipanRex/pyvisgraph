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
from collections import defaultdict
from graph import Graph, Point, Edge
from visible_vertices import visible_vertices, edge_intersect


def vis_graph(graph, origin=None, destination=None):
    # TODO: Only check half circle of vertices.
    # TODO: origin and destination should not be given here. it should be part
    # of 'graph'
    visibility_graph = Graph([])
    for point1 in graph.get_points():
        for point2 in visible_vertices(point1, graph, origin, destination):
            edge = Edge(point1, point2)
            visibility_graph.graph[point1].add(edge)
            visibility_graph.graph[point2].add(edge)

    graph_edges = graph.get_edges()
    for edge in visibility_graph.get_edges():
        p1 = edge.points[0]
        p2 = edge.points[1]
        if point_in_polygon(p1, p2, graph_edges):
            visibility_graph[p1].remove(edge)
            visibility_graph[p2].remove(edge)
            if len(visibility_graph[p1]) == 0:
                visibility_graph.graph.pop(p1)
            if len(visibility_graph[p2]) == 0:
                visibility_graph.graph.pop(p2)

    return visibility_graph


def point_in_polygon(p1, p2, graph_edges):
    mid_point = Point((p1.x + p2.x) / 2, (p1.y + p2.y) / 2)
    mid_point_end = Point(float('inf'), mid_point.y)
    intersect_count = 0
    for edge in graph_edges:
        # TODO: Implement a Polygon class. Pull edges from that and not
        # from the whole graph as below.
        if edge.points[0].polygon_id == p1.polygon_id:
            if edge_intersect(mid_point, mid_point_end, edge):
                intersect_count += 1
    if intersect_count % 2 == 0:
        return True
    return False
