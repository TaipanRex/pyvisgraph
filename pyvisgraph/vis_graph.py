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
from timeit import default_timer
from sys import stdout
from multiprocessing import Pool

from graph import Graph, Edge
from shortest_path import shortest_path
from visible_vertices import visible_vertices, point_in_polygon, closest_point


class VisGraph(object):

    def __init__(self):
        self.graph = None
        self.visgraph = None

    def load(self, filename):
        """Load obstacle graph and visibility graph. """
        with open(filename, 'rb') as load:
            self.graph, self.visgraph = pickle.load(load)

    def save(self, filename):
        """Save obstacle graph and visibility graph. """
        with open(filename, 'wb') as output:
            pickle.dump((self.graph, self.visgraph), output, -1)

    def build(self, input, workers=1, status=False):
        """Build visibility graph based on a list of polygons.

        The input must be a list of polygons, where each polygon is a list of
        in-order (clockwise or counter clockwise) Points. It only one polygon,
        it must still be a list in a list, i.e. [[Point(0,0), Point(2,0),
        Point(2,1)]].
        Take advantage of processors with multiple cores by setting workers to
        the number of subprocesses you want. Defaults to 1, i.e. no subprocess
        will be started.
        Set status to True to see progress information for each subprocess:
        [Points done][Points remaining][average time per Point].
        """

        self.graph = Graph(input)
        self.visgraph = Graph([])
        if status: print " " + "[Done][Rem.][Avg t] " * workers

        if workers == 1:
            for edge in _vis_graph(self.graph, self.graph.get_points(), 0, status):
                self.visgraph.add_edge(edge)
            if status: print ""
            return None

        points = self.graph.get_points()
        batch_size = int(len(points) / workers)
        batches = [(self.graph, points[i:i + batch_size], i/batch_size, status)
                   for i in xrange(0, len(points), batch_size)]
        pool = Pool(workers)
        results = pool.map_async(_vis_graph_wrapper, batches)
        for result in results.get():
            for edge in result:
                self.visgraph.add_edge(edge)
        if status: print ""

    def update(self, points, origin=None, destination=None):
        """Update visgraph by checking visibility of Points in list points."""

        for p in points:
            for v in visible_vertices(p, self.graph, origin=origin,
                                      destination=destination):
                self.visgraph.add_edge(Edge(p, v))

    # TODO(TaipanRex): visgraph is updated this way, lets find a way to avoid.
    def shortest_path(self, origin, destination):
        """Find and return shortest path between origin and destination.

        Will return in-order list of Points of the shortest path found. If
        origin or destination are not in the visibility graph, the graph will
        first be updated.
        Note that the visgraph will be updated permanently with the origin
        and destination visibility if not computed before.
        """

        origin_exists = origin in self.visgraph
        dest_exists = destination in self.visgraph
        if origin_exists and dest_exists:
            return shortest_path(self.visgraph, origin, destination)
        orgn = None if origin_exists else origin
        dest = None if dest_exists else destination
        if not origin_exists: self.update([origin], destination=dest)
        if not dest_exists: self.update([destination], origin=orgn)
        return shortest_path(self.visgraph, origin, destination)

    def point_in_polygon(self, point):
        """Return polygon_id if point in a polygon, -1 otherwise."""

        return point_in_polygon(point, self.graph)

    def closest_point(self, point, polygon_id):
        """Return closest Point outside polygon from point.

        Note method assumes point is inside the polygon, no check is
        performed.
        """

        return closest_point(point, self.graph, polygon_id)


def _vis_graph_wrapper(args):
    return _vis_graph(*args)


def _vis_graph(graph, points, worker, status):
    total_points = len(points)
    visible_edges = []
    if status:
        t0 = default_timer()
        points_done = 0
    for p1 in points:
        for p2 in visible_vertices(p1, graph, scan='half'):
            visible_edges.append(Edge(p1, p2))
        if status:
            points_done += 1
            avg_time = round((default_timer() - t0) / points_done, 3)
            time_stat = (points_done, total_points-points_done, avg_time)
            status = '\r\033[' + str(21*worker) + 'C[{:4}][{:4}][{:5.3f}] \r'
            stdout.write(status.format(*time_stat))
            stdout.flush()
    return visible_edges
