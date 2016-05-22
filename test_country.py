import cProfile
import pstats
import shapefile
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import Polygon
from matplotlib.collections import PatchCollection
from graph import Graph, Point, Edge
from visible_vertices import (edge_intersect, point_edge_distance,
                              visible_vertices, angle)


def test_country():
    sf = shapefile.Reader("examples/GSHHS_c_L1.dbf")
    shapes = sf.shapes()

    poly1 = [Point(a[0], a[1]) for a in shapes[4].points]
    graph = Graph([poly1])
    ship = Point(-80, -30)

    fig = plt.figure(1, figsize=(10, 10), dpi=90)
    ax = fig.add_subplot(111)

    x = [a.x for a in poly1]
    y = [a.y for a in poly1]
    ax.plot(x, y, color='gray', alpha=0.7, linewidth=1,
            solid_capstyle='round', zorder=2)

    for pp in graph.get_points():
        visible = visible_vertices(pp, graph, ship, None)
        for point in visible:
            x = [pp.x, point.x]
            y = [pp.y, point.y]
            ax.plot(x, y, color='red', alpha=0.7, linewidth=1)

    ax.set_title("Python visibility graph")
    fig.savefig("poly.png", bbox_inches='tight')

cProfile.run('test_country()', 'runtime')
p = pstats.Stats('runtime')
p.sort_stats('cumulative').print_stats(10)
p.sort_stats('time').print_stats(10)
