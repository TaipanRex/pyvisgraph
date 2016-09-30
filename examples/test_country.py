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
from __future__ import division
import shapefile
from timeit import default_timer
import pickle
from vis_graph.graph import Graph, Point, Edge
from vis_graph.vis_graph import vis_graph, visible_vertices
from utils.shortest_path import shortest_path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt


def test_country():
    #sf = shapefile.Reader("examples/shapefiles/ne_110m_coastline.shp")
    sf = shapefile.Reader("examples/shapefiles/GSHHS_c_L1.dbf")
    shapes = sf.shapes()
    polys = []

    #polys = [[Point(1,2)],[Point(3,4),Point(4,3),Point(3.5,4),Point(4,5.5),Point(3,4)],[Point(6,8),Point(7,1),Point(8,9),Point(7,3),Point(6,8)]]#[Point(7,5),Point(7.2,6),Point(7,5.5),Point(6.8,6),Point(7,5)]
    #polys.append([Point(a[0], a[1]) for a in shapes[4].points])
    '''
    for a in shapes[10].points:
        p = Point(a[0], a[1])
        if p.x<-79.0 and p.y >71.50 and p.y < 73.7:
            polys.append(p)
    polys = [polys]
    '''
    for shape in shapes:
        poly = []
        if len(shape.points) > 4:
            for a in shape.points:
                p = Point(a[0], a[1])
                poly.append(p)
            polys.append(poly)
    graph = Graph(polys)
    print "Graph points: {} edges: {}".format(len(graph.graph), len(graph.get_edges()))

    t0 = default_timer()
    op_net = None
    #with open('visgraph.pk1', 'rb') as load:
    #    op_net = pickle.load(load)
    op_net = vis_graph(graph)
    t1 = default_timer()
    print "Time to create visibility graph: {}".format(t1 - t0)
    print "visibility graph edges: {}".format(len(op_net.get_edges()))
    #with open('visgraph.pk1', 'wb') as output:
    #    pickle.dump(op_net, output, -1)
    '''
    t2 = default_timer()
    origin = Point(60.0, 0.0)
    destination = Point(40.0, 70.0)
    for v in visible_vertices(origin, graph, destination=destination):
        op_net.add_edge(Edge(origin, v))
    for v in visible_vertices(destination, graph, origin=origin):
        op_net.add_edge(Edge(destination, v))
    t3 = default_timer()
    print "Time to update vis graph with origin/dest: {}".format(t3 - t2)
    print "visibility graph edges: {}".format(len(op_net.get_edges()))

    t4 = default_timer()
    shortest = shortest_path(op_net, origin, destination)
    t5 = default_timer()
    print "Shorest path hops: {}".format(len(shortest))
    print "Time to calculate shortest path: {}".format(t5 - t4)
    '''
    t6 = default_timer()
    fig = plt.figure(1, figsize=(10, 10), dpi=90)
    ax = fig.add_subplot(111)
    # Draw the country
    for poly in polys:
        x = [a.x for a in poly]
        y = [a.y for a in poly]
        ax.plot(x, y, color='black', alpha=0.7, linewidth=1,
                solid_capstyle='round', zorder=2)

    # Draw the visibility graph
    for e in op_net.get_edges():
        x = [e.points[0].x, e.points[1].x]
        y = [e.points[0].y, e.points[1].y]
        ax.plot(x, y, color='red', alpha=0.5, linewidth=0.5)
    #x = [v.x for v in shortest]
    #y = [v.y for v in shortest]
    # Draw the shortest path
    #ax.plot(x, y, color='green', alpha=0.7, linewidth=2.0)
    # Annotate
    ax.set_title("Python visibility graph & shortest path")
    #ax.annotate('Origin', xytext=(origin.x, origin.y), xy=(origin.x, origin.y))
    a#x.annotate('Destination', xytext=(destination.x, destination.y), xy=(destination.x, destination.y))
    fig.savefig("poly.png", bbox_inches='tight')
    t7 = default_timer()
    print "Time to draw graph: {}".format(t7 - t6)

if __name__ == "__main__":
    test_country()
