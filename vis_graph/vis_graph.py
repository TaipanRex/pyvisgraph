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
from visible_vertices import visible_vertices


def vis_graph(graph=None, origin=None, destination=None):
    # TODO: Only check half circle of vertices.
    # TODO: origin and destination should not be given here. it should be part
    # of 'graph'
    visible = set()
    for point in graph.get_points():
        points_visible = visible_vertices(point, graph, origin, destination)
        v = [Edge(point, p) for p in points_visible]
        visible = visible | set(v)

    visibility_graph = Graph([])
    tmp_dict = defaultdict(list)
    for edge in visible:
        p1, p2 = edge.points

        if edge not in tmp_dict[p1]:
            tmp_dict[p1].append(edge)

        if edge not in tmp_dict[p2]:
            tmp_dict[p2].append(edge)
    visibility_graph.graph = tmp_dict

    return visibility_graph
