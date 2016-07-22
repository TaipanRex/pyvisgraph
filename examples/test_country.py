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
#import matplotlib.pyplot as plt
from vis_graph.graph import Graph, Point, Edge
from vis_graph.shortest_path import shortest_path
from vis_graph.vis_graph import vis_graph


def test_country():
    sf = shapefile.Reader("examples/shapefiles/GSHHS_c_L1.dbf")
    shapes = sf.shapes()
    poly1 = [Point(a[0], a[1]) for a in shapes[4].points]

    graph = Graph([poly1])
    ship = Point(-50, -40)
    port = Point(-50, 10)
    op_net = vis_graph(graph, ship, port)
    print "Operating network size: {}".format(len(op_net.get_edges()))
    '''
    fig = plt.figure(1, figsize=(10, 10), dpi=90)
    ax = fig.add_subplot(111)

    # Draw the country
    x = [a.x for a in poly1]
    y = [a.y for a in poly1]
    ax.plot(x, y, color='black', alpha=0.7, linewidth=1,
            solid_capstyle='round', zorder=2)

    # Draw the visibility graph
    for e in op_net.get_edges():
        x = [e.points[0].x, e.points[1].x]
        y = [e.points[0].y, e.points[1].y]
        ax.plot(x, y, color='red', alpha=0.5, linewidth=0.5)

    # Hacky test of shortest path
    shortest = shortest_path(op_net, ship, port)
    print "Shorest path hops: {}".format(len(shortest))
    x = [v.x for v in shortest]
    y = [v.y for v in shortest]
    # Draw the shortest path
    ax.plot(x, y, color='green', alpha=0.7, linewidth=2.0)

    ax.set_title("Python visibility graph & shortest path")
    ax.annotate('Origin', xytext=(ship.x, ship.y), xy=(ship.x, ship.y))
    ax.annotate('Destination', xytext=(port.x, port.y), xy=(port.x, port.y))
    fig.savefig("poly.png", bbox_inches='tight')
    '''

if __name__ == "__main__":
    test_country()
