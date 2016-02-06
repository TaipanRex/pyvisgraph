from oceanspp import Graph, Point, Edge, Polygon, shortest_path, angle
from oceanspp import edge_intersect
import pytest
from math import pi, degrees

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

    def test_point_equality_1(self):
        point = Point(0.0, 1.0)
        assert self.point_a == point

    def test_point_equality_2(self):
        point = Point(1.0, 0.0)
        assert self.point_a != point

    def test_edge_equality_1(self):
        assert self.edge_a == self.edge_b

    def test_edge_equality_2(self):
        assert self.edge_a == self.edge_a

    def test_edge_equality_3(self):
        assert self.edge_a == self.edge_c

    def test_edge_equality_4(self):
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


class TestAngleFunction:
    def setup_method(self, method):
        self.center = Point(1.0, 1.0)
        self.point_a = Point(3.0, 1.0)
        self.point_b = Point(1.0, 0)
        self.point_c = Point(0.0, 2.0)
        self.point_d = Point(2.0, 2.0)
        self.point_e = Point(2.0, 0.0)
        self.point_f = Point(0.0, 0.0)

    def test_angle_1(self):
        assert angle(self.center, self.point_a) == 0

    def test_angle_2(self):
        assert angle(self.center, self.point_b) == pi*3 / 2

    def test_angle_3(self):
        assert degrees(angle(self.center, self.point_c)) == 135

    def test_angle_4(self):
        assert degrees(angle(self.center, self.point_d)) == 45

    def test_angle_4(self):
        assert degrees(angle(self.center, self.point_e)) == 315

    def test_angle_5(self):
        assert degrees(angle(self.center, self.point_f)) == 225

class TestEdgeIntersectFunction:

    def setup_method(self, method):
        self.point_a = Point(3.0, 5.0)
        self.point_b = Point(5.0, 3.0)
        self.point_c = Point(4.0, 2.0)
        self.point_d = Point(4.0, 5.0)
        self.point_e = Point(5.0, 4.0)
        self.point_f = Point(3.0, 4.0)
        self.point_g = Point(4.0, 1.0)
        self.point_h = Point(6.0, 4.0)
        self.edge = Edge(self.point_a, self.point_b)

    def test_edge_intersect_1(self):
        assert edge_intersect(self.point_c, self.point_d, self.edge) == True

    def test_edge_intersect_2(self):
        assert edge_intersect(self.point_c, self.point_e, self.edge) == True

    def test_edge_intersect_3(self):
        assert edge_intersect(self.point_f, self.point_e, self.edge) == True

    def test_edge_intersect_4(self):
        assert edge_intersect(self.point_g, self.point_b, self.edge) == False

    def test_edge_intersect_5(self):
        assert edge_intersect(self.point_g, self.point_h, self.edge) == False

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
        assert shortest == [edge_a, edge_b, edge_c, edge_d]
