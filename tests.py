from oceanspp import Graph, Point, Edge, Polygon, shortest_path, angle
from oceanspp import edge_intersect, point_edge_distance, visible_vertices
import pytest
from math import pi, degrees
from matplotlib import pyplot as plt

'''
setup_module(module): only run once when file is executed
teardown_module(module):
setup_function(function):

In a class:
setup(self): gets run last when a method is called
setup_class(cls):
setup_method(self, method):

'''

class TestUndirectedGraph:

    def setup_method(self, method):
        self.point_a = Point(0.0, 1.0)
        self.point_b = Point(1.0, 2.0)
        self.point_c = Point(0.0, 1.0)
        self.point_d = Point(1.0, 2.0)
        self.edge_a = Edge(self.point_a, self.point_b)
        self.edge_b = Edge(self.point_b, self.point_a)
        self.edge_c = Edge(self.point_c, self.point_d)
        self.edge_d = Edge(self.point_d, self.point_c)

    def test_point_equality(self):
        assert self.point_a == Point(0.0, 1.0)
        assert self.point_a != Point(1.0, 0.0)
        assert self.edge_a == self.edge_b
        assert self.edge_a == self.edge_a
        assert self.edge_a == self.edge_c
        assert self.edge_a == self.edge_d

    def test_polygon_duplicate_edges(self):
        polygon = Polygon([self.point_a, self.point_b],
            [self.edge_a, self.edge_b])
        assert len(polygon.edges) == 1

    def test_polygon_duplicate_points(self):
        polygon = Polygon([self.point_a, self.point_b, self.point_a], [])
        assert len(polygon.points) == 2

    def test_print_graph(self):
        polygon = Polygon([self.point_a, self.point_b], [self.edge_a])
        graph = Graph([polygon])
        assert str(graph) == "Polygon 0\nPoints: (0.0, 1.0), (1.0, 2.0)\nEdges: ((0.0, 1.0), (1.0, 2.0))"

def test_angle_function():
    center = Point(1.0, 1.0)
    point_a = Point(3.0, 1.0)
    point_b = Point(1.0, 0)
    point_c = Point(0.0, 2.0)
    point_d = Point(2.0, 2.0)
    point_e = Point(2.0, 0.0)
    point_f = Point(0.0, 0.0)
    assert angle(center, point_a) == 0
    assert angle(center, point_b) == pi*3 / 2
    assert degrees(angle(center, point_c)) == 135
    assert degrees(angle(center, point_d)) == 45
    assert degrees(angle(center, point_e)) == 315
    assert degrees(angle(center, point_f)) == 225

def test_edge_intersect_function():
    point_a = Point(3.0, 5.0)
    point_b = Point(5.0, 3.0)
    point_c = Point(4.0, 2.0)
    point_d = Point(4.0, 5.0)
    point_e = Point(5.0, 4.0)
    point_f = Point(3.0, 4.0)
    point_g = Point(4.0, 1.0)
    point_h = Point(6.0, 4.0)
    edge = Edge(point_a, point_b)
    assert edge_intersect(point_c, point_d, edge) == True
    assert edge_intersect(point_c, point_e, edge) == True
    assert edge_intersect(point_f, point_e, edge) == True
    assert edge_intersect(point_g, point_b, edge) == False
    assert edge_intersect(point_g, point_h, edge) == False

def test_point_edge_distance_function():
    point_a = Point(3.0, 1.0)
    point_b = Point(3.0, 5.0)
    point_c = Point(2.0, 2.0)
    point_d = Point(4.0, 4.0)
    point_e = Point(1.0, 1.0)
    point_f = Point(1.0, 2.0)
    point_g = Point(3.0, 4.0)
    point_h = Point(2.0, 5.0)
    point_i = Point(4.0, 4.0)
    edge = Edge(point_a, point_b)
    edge2 = Edge(point_c, point_d)
    edge3 = Edge(point_e, point_b)
    assert point_edge_distance(point_c, point_d, edge) == 1.4142135623730951
    assert point_edge_distance(point_a, point_b, edge2) == 2.0
    assert point_edge_distance(point_f, point_g, edge3) == 1.4142135623730951
    assert point_edge_distance(point_h, point_g, edge3) ==  0.9428090415820635


class TestVisibleVertices:

    def test_visible_vertices_1(self):
        point_a = Point(1.0, 1.0)
        point_b = Point(3.0, 1.0)
        point_c = Point(1.0, 3.0)
        point_d = Point(3.0, 4.0)
        point_e = Point(4.0, 3.0)
        edge_a = Edge(point_a, point_c)
        edge_b = Edge(point_a, point_b)
        edge_c = Edge(point_b, point_e)
        edge_d = Edge(point_c, point_d)
        edge_e = Edge(point_d, point_e)
        polygon = Polygon([point_a, point_b, point_c, point_d, point_e],
                                [edge_a, edge_b, edge_c, edge_d, edge_e])
        graph = Graph([polygon])

        ship = Point(2.0, 5.0)
        visible = visible_vertices(point_a, graph, ship, None)
        assert visible == [point_b, point_c]
        visible = visible_vertices(point_b, graph, ship, None)
        assert visible == [point_e, point_a]
        visible = visible_vertices(point_c, graph, ship, None)
        assert visible == [point_d, ship, point_a]
        visible = visible_vertices(point_d, graph, ship, None)
        assert visible == [ship, point_c, point_e]
        #This also tests collinearity
        visible = visible_vertices(point_e, graph, ship, None)
        assert visible == [point_d, point_b]
        #This also tests collinearity
        visible = visible_vertices(ship, graph, ship, None)
        assert visible == [point_c, point_d]

    def test_visible_vertices_2(self):
        point_a = Point(0.0, 1.0)
        point_b = Point(1.0, 1.0)
        point_c = Point(1.0, 2.0)

        point_d = Point(5.0, 6.0)
        point_e = Point(6.0, 6.0)
        point_f = Point(6.0, 7.0)

        edge_a = Edge(point_a, point_b)
        edge_b = Edge(point_b, point_c)
        edge_c = Edge(point_c, point_a)

        edge_d = Edge(point_d, point_e)
        edge_e = Edge(point_e, point_f)
        edge_f = Edge(point_f, point_d)
        polygon_a = Polygon([point_a, point_b, point_c],
                                [edge_a, edge_b, edge_c])
        polygon_b = Polygon([point_d, point_e, point_f],
                                [edge_d, edge_e, edge_f])
        graph = Graph([polygon_a, polygon_b])

        ship = Point(4.0, 5.0)
        #visible = visible_vertices(ship, graph, ship, None)
        #assert visible == [point_f, point_e]
        visible = visible_vertices(ship, graph, ship, None)
        #assert visible == [point_f, point_e]
        for v in visible:
            print str(v) + ", "

class TestShortestPaths:

    def setup_method(self, method):
        # test obstacle A
        self.point_a = Point(1.0, 2.0)
        self.point_b = Point(4.0, 2.5)
        self.point_c = Point(5.0, 3.0)
        self.point_d = Point(4.5, 5.0)
        self.point_e = Point(3.0, 5.0)
        self.point_f = Point(3.0, 7.0)
        self.point_g = Point(4.0, 7.0)
        self.point_h = Point(4.0, 8.0)
        self.point_i = Point(1.0, 8.0)
        self.points = [self.point_a, self.point_b, self.point_c, self.point_d,
            self.point_e, self.point_f, self.point_g, self.point_h,
            self.point_i]

        self.edges = []
        self.edges.append(Edge(self.point_a, self.point_b))
        self.edges.append(Edge(self.point_a, self.point_i))
        self.edges.append(Edge(self.point_b, self.point_a))
        self.edges.append(Edge(self.point_b, self.point_c))
        self.edges.append(Edge(self.point_c, self.point_b))
        self.edges.append(Edge(self.point_c, self.point_d))
        self.edges.append(Edge(self.point_d, self.point_c))
        self.edges.append(Edge(self.point_d, self.point_e))
        self.edges.append(Edge(self.point_e, self.point_d))
        self.edges.append(Edge(self.point_e, self.point_f))
        self.edges.append(Edge(self.point_f, self.point_e))
        self.edges.append(Edge(self.point_f, self.point_g))
        self.edges.append(Edge(self.point_g, self.point_f))
        self.edges.append(Edge(self.point_g, self.point_h))
        self.edges.append(Edge(self.point_h, self.point_g))
        self.edges.append(Edge(self.point_h, self.point_i))
        self.edges.append(Edge(self.point_i, self.point_a))
        self.edges.append(Edge(self.point_i, self.point_h))

        self.polygon_a = Polygon(self.points, self.edges)

        # test obstacle B
        self.point_a = Point(6.0, 1.0)
        self.point_b = Point(7.0, 2.0)
        self.point_c = Point(8.0, 6.0)
        self.point_d = Point(10.0, 1.5)
        self.points = [self.point_a, self.point_b, self.point_c, self.point_d]

        self.edges = []
        self.edges.append(Edge(self.point_a, self.point_b))
        self.edges.append(Edge(self.point_a, self.point_d))
        self.edges.append(Edge(self.point_b, self.point_a))
        self.edges.append(Edge(self.point_b, self.point_c))
        self.edges.append(Edge(self.point_c, self.point_b))
        self.edges.append(Edge(self.point_c, self.point_d))
        self.edges.append(Edge(self.point_d, self.point_a))
        self.edges.append(Edge(self.point_d, self.point_c))

        self.polygon_b = Polygon(self.points, self.edges)

        # test operating network
        self.point_a = Point(1.0, 2.0)
        self.point_b = Point(4.0, 2.5)
        self.point_c = Point(5.0, 3.0)
        self.point_d = Point(4.5, 5.0)
        self.point_e = Point(4.0, 8.0)
        self.point_f = Point(1.0, 8.0)
        self.point_g = Point(6.0, 1.0)
        self.point_h = Point(8.0, 6.0)
        self.point_i = Point(10.0, 1.5)
        self.point_j = Point(4.0, 7.0)
        self.points = [self.point_a, self.point_b, self.point_c, self.point_d,
            self.point_e, self.point_f, self.point_g, self.point_h,
            self.point_i, self.point_j]

        self.edges = []
        self.edges.append(Edge(self.point_a, self.point_b))
        self.edges.append(Edge(self.point_a, self.point_f))
        self.edges.append(Edge(self.point_a, self.point_g))
        self.edges.append(Edge(self.point_b, self.point_a))
        self.edges.append(Edge(self.point_b, self.point_c))
        self.edges.append(Edge(self.point_c, self.point_b))
        self.edges.append(Edge(self.point_c, self.point_g))
        self.edges.append(Edge(self.point_c, self.point_h))
        self.edges.append(Edge(self.point_c, self.point_d))
        self.edges.append(Edge(self.point_d, self.point_c))
        self.edges.append(Edge(self.point_d, self.point_e))
        self.edges.append(Edge(self.point_d, self.point_g))
        self.edges.append(Edge(self.point_e, self.point_d))
        self.edges.append(Edge(self.point_e, self.point_f))
        self.edges.append(Edge(self.point_e, self.point_j))
        self.edges.append(Edge(self.point_e, self.point_h))
        self.edges.append(Edge(self.point_f, self.point_a))
        self.edges.append(Edge(self.point_f, self.point_e))
        self.edges.append(Edge(self.point_g, self.point_a))
        self.edges.append(Edge(self.point_g, self.point_c))
        self.edges.append(Edge(self.point_g, self.point_d))
        self.edges.append(Edge(self.point_g, self.point_h))
        self.edges.append(Edge(self.point_g, self.point_i))
        self.edges.append(Edge(self.point_h, self.point_c))
        self.edges.append(Edge(self.point_h, self.point_e))
        self.edges.append(Edge(self.point_h, self.point_g))
        self.edges.append(Edge(self.point_h, self.point_i))
        self.edges.append(Edge(self.point_i, self.point_h))
        self.edges.append(Edge(self.point_i, self.point_g))
        self.edges.append(Edge(self.point_j, self.point_e))

        self.op_network = Polygon(self.points, self.edges)
        self.graph = Graph([self.polygon_a, self.polygon_b])
        self.op_graph = Graph([self.op_network])

    def test_shortest_path_1(self):
        ship = Point(10.0, 5.5)
        port = Point(1.0, 2.0)
        shortest = shortest_path(self.op_graph, ship, port)
        edge_a = Edge(ship, Point(8.0, 6.0))
        edge_b = Edge(Point(8.0, 6.0), Point(5.0, 3.0))
        edge_c = Edge(Point(5.0, 3.0), Point(4.0, 2.5))
        edge_d = Edge(Point(4.0, 2.5), Point(1.0, 2.0))

        #Draw the obstacles and operating network
        fig = plt.figure(1, figsize=(5,5), dpi=90)
        ax = fig.add_subplot(111)

        #Draw the obstacles
        for polygon in self.graph.polygons:
            for edge in polygon.edges:
                x = [edge.points[0].x, edge.points[1].x]
                y = [edge.points[0].y, edge.points[1].y]
                ax.plot(x, y, color='blue', alpha=0.7, linewidth=3, solid_capstyle='round', zorder=2)

        #Draw the operating network
        for edge in self.op_graph.get_edges():
            x = [edge.points[0].x, edge.points[1].x]
            y = [edge.points[0].y, edge.points[1].y]
            ax.plot(x, y, color='red', alpha=0.7, linewidth=1)

        #draw shortest path
        #x,y = zip(*shortest)
        #ax.plot(x, y, color='green', alpha=0.7, linewidth=2)

        ax.set_title("ocean shortest path test")
        xrange = [0, 11]
        yrange = [0, 9]
        ax.set_xlim(*xrange)
        ax.set_xticks(range(*xrange) + [xrange[-1]])
        ax.set_ylim(*yrange)
        ax.set_yticks(range(*yrange) + [yrange[-1]])
        ax.set_aspect(1)
        fig.savefig("poly.png")

        assert shortest == [edge_a, edge_b, edge_c, edge_d]
