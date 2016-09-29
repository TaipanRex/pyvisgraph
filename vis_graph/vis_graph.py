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
import time


def vis_graph(graph, origin=None, destination=None):
    # TODO: Only check half circle of vertices.
    # TODO: origin and destination should not be given here. it should be part
    # of 'graph'
    visibility_graph = Graph([])
    for i, p1 in enumerate(graph.get_points()):
        t0 = time.clock()
        for p2 in visible_vertices(p1, graph, origin, destination):
            visibility_graph.add_edge(Edge(p1, p2))
        t1 = time.clock()
        print "Completed point: {} - time: {}".format(i, t1 - t0)

    return visibility_graph
