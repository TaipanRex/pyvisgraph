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
import matplotlib.pyplot as plt
import time
from vis_graph.graph import Graph, Point, Edge
from vis_graph.shortest_path import shortest_path
from vis_graph.vis_graph import vis_graph, visible_vertices


def test_country():
    #sf = shapefile.Reader("examples/shapefiles/ne_110m_coastline.shp")
    sf = shapefile.Reader("examples/shapefiles/GSHHS_c_L1.dbf")
    shapes = sf.shapes()
    polys = []
    counter = 0
    #for c, shape in enumerate(shapes):
    #    if len(shape.points) > 100:
    #        print c
    #        counter = counter + 1
    #print counter

    for i in range(0, len(shapes)):
        polys.append([Point(a[0], a[1]) for a in shapes[i].points])

    #polys.append([Point(a[0], a[1]) for a in shapes[0].points])
    '''
    for a in shapes[3].points:
        p = Point(a[0], a[1])
        if p.x > -86.0 and p.x <-78.0 and p.y>20.0 and p.y<35.0:
            polys.append(p)
    polys = [polys]
    polys[0].append(polys[0][0])
    '''
    graph = Graph(polys)
    print "Graph points: {} edges: {}".format(len(graph.graph), len(graph.get_edges()))

    t0 = time.clock()
    op_net = vis_graph(graph)
    t1 = time.clock()
    print "Time to create visibility graph: {}".format(t1 - t0)

    #t2 = time.clock()
    #origin = Point(-50, -40)
    #destination = Point(-50, 10)
    #for v in visible_vertices(origin, graph, destination=destination):
    #    op_net.add_edge(Edge(origin, v))
    #for v in visible_vertices(destination, graph, origin=origin):
    #    op_net.add_edge(Edge(destination, v))
    #t3 = time.clock()
    #print "Time to update vis graph with origin/dest: {}".format(t3 - t2)
    #print "visibility graph edges: {}".format(len(op_net.get_edges()))

    #t4 = time.clock()
    #shortest = shortest_path(op_net, origin, destination)
    #t5 = time.clock()
    #print "Shorest path hops: {}".format(len(shortest))
    #print "Time to calculate shortest path: {}".format(t5 - t4)

    t6 = time.clock()
    fig = plt.figure(1, figsize=(10, 10), dpi=90)
    ax = fig.add_subplot(111)
    # Draw the country
    for poly in polys:
        x = [a.x for a in poly]
        y = [a.y for a in poly]
        ax.plot(x, y, color='black', alpha=0.7, linewidth=1,
                solid_capstyle='round', zorder=2)
#    for poly in polys:
#        for p in poly:
#            if p.x > -73.7 and p.x < -71.9:
#                if p.y > 68.0 and p.y < 70.5:
#            ax.annotate('{:.2f},{:.2f}'.format(p.x, p.y), xytext=(p.x, p.y), xy=(p.x, p.y))

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
    #ax.annotate('Destination', xytext=(destination.x, destination.y), xy=(destination.x, destination.y))
    fig.savefig("poly.png", bbox_inches='tight')
    t7 = time.clock()
    print "Time to draw graph: {}".format(t7 - t6)

if __name__ == "__main__":
    test_country()
