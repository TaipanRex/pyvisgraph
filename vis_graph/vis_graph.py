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
import cPickle as pickle
from graph import Graph, Edge
from visible_vertices import visible_vertices
from timeit import default_timer
import sys
from utils.shortest_path import shortest_path
from multiprocessing import Pool


# TODO: add update_visgraph(point), so you can to shortest([p1,p2,p3], point)
class VisGraph(object):

    def __init__(self):
        self.graph = None
        self.visgraph = None

    def load(self, filename):
        with open(filename, 'rb') as load:
            self.graph, self.visgraph = pickle.load(load)

    def save(self, filename):
        with open(filename, 'wb') as output:
            pickle.dump((self.graph, self.visgraph), output, -1)

    # TODO: build the obstacle graph on various inputs, list of polys,
    # shapefile (given index points where coordinates are)
    def build(self, input, workers=1):
        self.graph = Graph(input)
        self.visgraph = Graph([])
        print " " + "[Done][Rem.][Avg t] " * workers
        if workers == 1:
            for edge in _vis_graph(self.graph, self.graph.get_points(), 0):
                self.visgraph.add_edge(edge)
            print ""
            return

        points = self.graph.get_points()
        # Perhaps better to use smaller batch size, if one process is slower..
        batch_size = int(len(points) / workers)
        point_batches = [(self.graph, points[i:i + batch_size], i/batch_size)
                         for i in xrange(0, len(points), batch_size)]
        pool = Pool(workers)
        results = pool.map_async(_vis_graph_wrapper, point_batches)
        for result in results.get():
            for edge in result:
                self.visgraph.add_edge(edge)
        print ""

    def shortest_path(self, origin, destination):
        updated_visgraph = Graph([])
        updated_visgraph.graph = self.visgraph.graph.copy()
        for p in visible_vertices(origin, self.graph, destination=destination):
            updated_visgraph.add_edge(Edge(origin, p))
        for p in visible_vertices(destination, self.graph, origin=origin):
            updated_visgraph.add_edge(Edge(destination, p))
        return shortest_path(updated_visgraph, origin, destination)


def _vis_graph_wrapper(args):
    return _vis_graph(*args)


def _vis_graph(graph, points, worker):
    total_points = len(points)
    points_done = 0
    visible_edges = []
    t0 = default_timer()
    for i, p1 in enumerate(points):
        for p2 in visible_vertices(p1, graph, scan='half'):
            visible_edges.append(Edge(p1, p2))
        points_done += 1
        avg_time = round((default_timer() - t0) / points_done, 3)
        time_stat = (points_done, total_points-points_done, avg_time)
        status = '\r\033[' + str(21*worker) + 'C[{:4}][{:4}][{:5.3f}] \r'
        sys.stdout.write(status.format(*time_stat))
        sys.stdout.flush()
    return visible_edges
