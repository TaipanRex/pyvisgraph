from __future__ import division
import cProfile
from collections import defaultdict
import pstats
import shapefile
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import Polygon
from matplotlib.collections import PatchCollection
from vis_graph.graph import Graph, Point, Edge
from vis_graph.visible_vertices import (edge_intersect, point_edge_distance,
                                        visible_vertices, angle)
from vis_graph.shortest_path import shortest_path


def test_country():
    sf = shapefile.Reader("examples/shapefiles/GSHHS_c_L1.dbf")
    shapes = sf.shapes()

    poly1 = [Point(a[0], a[1]) for a in shapes[4].points]
    graph = Graph([poly1])
    ship = Point(-50, -40)
    port = Point(-50, 10)

    fig = plt.figure(1, figsize=(10, 10), dpi=90)
    ax = fig.add_subplot(111)

    x = [a.x for a in poly1]
    y = [a.y for a in poly1]
    ax.plot(x, y, color='black', alpha=0.7, linewidth=1,
            solid_capstyle='round', zorder=2)

    ''' When each point is checked against every other point, you will check
    for visibility between a two points that might already have been checked. '''
    visible = set()
    for point in graph.get_points():
        v = [Edge(point, p) for p in visible_vertices(point, graph, ship, port)]
        visible = visible | set(v)
    for p in visible:
        x = [p.points[0].x, p.points[1].x]
        y = [p.points[0].y, p.points[1].y]
        ax.plot(x, y, color='red', alpha=0.5, linewidth=0.5)

    ''' Hacky test of shortest path '''
    op_net = Graph([])
    tmp_dict = defaultdict(list)
    for e in visible:
        p1, p2 = e.points

        if e not in tmp_dict[p1]:
            tmp_dict[p1].append(e)

        if e not in tmp_dict[p2]:
            tmp_dict[p2].append(e)
    op_net.graph = tmp_dict
    shortest = shortest_path(op_net,ship,port)
    x = [v.x for v in shortest]
    y = [v.y for v in shortest]
    #print shortest
    ax.plot(x, y, color='green', alpha=0.7, linewidth=2.0)

    ax.set_title("Python visibility graph & shortest path")
    ax.annotate('Origin', xytext=(ship.x,ship.y), xy=(ship.x,ship.y))
    ax.annotate('Destination', xytext=(port.x,port.y), xy=(port.x,port.y))
    fig.savefig("poly.png", bbox_inches='tight')

cProfile.run('test_country()', 'runtime')
p = pstats.Stats('runtime')
p.sort_stats('cumulative').print_stats(10)
p.sort_stats('time').print_stats(10)
