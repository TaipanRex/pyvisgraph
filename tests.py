from oceanspp import Graph, Point, Edge, Polygon#, shortest_path
import pytest

'''
setup_module(module): only run once when file is executed
teardown_module(module):
setup_function(function):

In a class:
setup(self): gets run last when a method is called
setup_class(cls):
setup_method(self, method):

'''
# test obstacle A
point_a = Point(1.0, 2.0)
point_b = Point(4.0, 2.5)
point_c = Point(5.0, 3.0)
point_d = Point(4.5, 5.0)
point_e = Point(3.0, 5.0)
point_f = Point(3.0, 7.0)
point_g = Point(4.0, 7.0)
point_h = Point(4.0, 8.0)
point_i = Point(1.0, 8.0)
points = [point_a, point_b, point_c, point_d, point_e, point_f, point_g, point_h, point_i]

edges = []
edges.append(Edge(point_a, point_b))
edges.append(Edge(point_a, point_i))
edges.append(Edge(point_b, point_a))
edges.append(Edge(point_b, point_c))
edges.append(Edge(point_c, point_b))
edges.append(Edge(point_c, point_d))
edges.append(Edge(point_d, point_c))
edges.append(Edge(point_d, point_e))
edges.append(Edge(point_e, point_d))
edges.append(Edge(point_e, point_f))
edges.append(Edge(point_f, point_e))
edges.append(Edge(point_f, point_g))
edges.append(Edge(point_g, point_f))
edges.append(Edge(point_g, point_h))
edges.append(Edge(point_h, point_g))
edges.append(Edge(point_h, point_i))
edges.append(Edge(point_i, point_a))
edges.append(Edge(point_i, point_h))

polygon_a = Polygon(points, edges)

# test obstacle B
point_a = Point(6.0, 1.0)
point_b = Point(7.0, 2.0)
point_c = Point(8.0, 6.0)
point_d = Point(10.0, 1.5)
points = [point_a, point_b, point_c, point_d]

edges = []
edges.append(Edge(point_a, point_b))
edges.append(Edge(point_a, point_d))
edges.append(Edge(point_b, point_a))
edges.append(Edge(point_b, point_c))
edges.append(Edge(point_c, point_b))
edges.append(Edge(point_c, point_d))
edges.append(Edge(point_d, point_a))
edges.append(Edge(point_d, point_c))

polygon_b = Polygon(points, edges)

# test operating network
point_a = Point(1.0, 2.0)
point_b = Point(4.0, 2.5)
point_c = Point(5.0, 3.0)
point_d = Point(4.5, 5.0)
point_e = Point(4.0, 8.0)
point_f = Point(1.0, 8.0)
point_g = Point(6.0, 1.0)
point_h = Point(8.0, 6.0)
point_i = Point(10.0, 1.5)
point_j = Point(4.0, 7.0)
points = [point_a, point_b, point_c, point_d, point_e, point_f, point_g, point_h, point_i, point_j]

edges = []
edges.append(Edge(point_a, point_b))
edges.append(Edge(point_a, point_f))
edges.append(Edge(point_a, point_g))
edges.append(Edge(point_b, point_a))
edges.append(Edge(point_b, point_c))
edges.append(Edge(point_c, point_b))
edges.append(Edge(point_c, point_g))
edges.append(Edge(point_c, point_h))
edges.append(Edge(point_c, point_d))
edges.append(Edge(point_d, point_c))
edges.append(Edge(point_d, point_e))
edges.append(Edge(point_d, point_g))
edges.append(Edge(point_e, point_d))
edges.append(Edge(point_e, point_f))
edges.append(Edge(point_e, point_j))
edges.append(Edge(point_e, point_h))
edges.append(Edge(point_f, point_a))
edges.append(Edge(point_f, point_e))
edges.append(Edge(point_g, point_a))
edges.append(Edge(point_g, point_c))
edges.append(Edge(point_g, point_d))
edges.append(Edge(point_g, point_h))
edges.append(Edge(point_g, point_i))
edges.append(Edge(point_h, point_c))
edges.append(Edge(point_h, point_e))
edges.append(Edge(point_h, point_g))
edges.append(Edge(point_h, point_i))
edges.append(Edge(point_i, point_h))
edges.append(Edge(point_i, point_g))
edges.append(Edge(point_j, point_e))

op_network = Polygon(points, edges)

class TestUndirectedGraph:

    def test_point_equality(self):
        point_a = Point(0.0, 1.0)
        point_b = Point(0.0, 1.0)
        assert point_a == point_b

        point_c = Point(1.0, 0.0)
        assert point_b != point_c

    '''
    Test that Polygon Edge Point order does not matter, i.e
    (point a, point b) == (point b, point a)
    '''
    def test_polygon_duplicate_edges(self):
        point_a = (0.0, 1.0)
        point_b = (2.0, 3.0)
        edge_a = Edge(point_a, point_b)
        edge_b = Edge(point_b, point_a)
        polygon = Polygon([point_a, point_b], [edge_a, edge_b])
        assert len(polygon.edges) == 1

    def test_polygon_duplicate_points(self):
        point_a = (0.0, 1.0)
        point_b = (2.0, 3.0)
        polygon = Polygon([point_a, point_b, point_a], [])
        assert len(polygon.points) == 2

    def test_graph_duplicate_points_edges(self):
        graph = Graph([polygon_a, polygon_b])
        assert len(graph.get_edges()) == 13
        assert len(graph.get_points()) == 13
        
'''
class TestShortestPaths:

    def setup_method(self, method):
        self.graph = Graph(obstacle_a, obstacle_b)
        self.op_network = Graph(self.op_graph)

    def test_shortest_path_1(self):
        ship = (10.0, 5.5)
        port = (1.0, 2.0)
        shortest = shortest_path(self.op_network, ship, port)
        assert str(shortest) == '[(10.0, 5.5), (8.0, 6.0), (5.0, 3.0), (4.0, 2.5), (1.0, 2.0)]'

    #def test_visible_vertices(self):
    #    v = (1.0,2.0)
    #    self.op_network.visible_vertices(v, self.graph)
'''
