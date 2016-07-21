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
from vis_graph.graph import Graph, Point, Edge
from vis_graph.visible_vertices import (edge_intersect, point_edge_distance,
                                        visible_vertices, angle, ccw)
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
def test_subscribe_when_already_registered():
    # GIVEN a user is already subscribed to a newsletter
    # WHEN a user subscribes to the newsletter
    # THEN no changes are made to the email list
    # and the user is told they already are subscribed
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

    def test_print_graph(self):
        graph = Graph([[self.point_a, self.point_b]])
        result = "\n(0.0, 1.0): ((0.0, 1.0), (1.0, 2.0))"
        result += "\n(1.0, 2.0): ((0.0, 1.0), (1.0, 2.0))"
        assert str(graph) == result


def test_angle_function():
    center = Point(1.0, 1.0)
    point_a = Point(3.0, 1.0)
    point_b = Point(1.0, 0)
    point_c = Point(0.0, 2.0)
    point_d = Point(2.0, 2.0)
    point_e = Point(2.0, 0.0)
    point_f = Point(0.0, 0.0)
    assert angle(center, point_a) == 0
    assert angle(center, point_b) == pi * 3 / 2
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
    assert edge_intersect(point_c, point_d, edge) is True
    assert edge_intersect(point_c, point_e, edge) is True
    assert edge_intersect(point_f, point_e, edge) is True
    assert edge_intersect(point_g, point_b, edge) is False
    assert edge_intersect(point_g, point_h, edge) is False


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
    assert point_edge_distance(point_h, point_g, edge3) == 0.9428090415820635


class TestVisibleVertices:

    def test_visible_vertices_1(self):
        point_a = Point(1.0, 1.0)
        point_b = Point(3.0, 1.0)
        point_c = Point(4.0, 3.0)
        point_d = Point(3.0, 4.0)
        point_e = Point(1.0, 3.0)
        ship = Point(2.0, 5.0)
        graph = Graph([[point_a, point_b, point_c, point_d, point_e]])

        visible = visible_vertices(point_a, graph, ship, None)
        assert visible == [point_b, point_e]
        visible = visible_vertices(point_b, graph, ship, None)
        assert visible == [point_c, point_a]
        visible = visible_vertices(point_d, graph, ship, None)
        assert visible == [ship, point_e, point_c]
        # This also tests collinearity
        visible = visible_vertices(point_c, graph, ship, None)
        assert visible == [point_d, point_b]
        # This also tests collinearity
        visible = visible_vertices(ship, graph, ship, None)
        assert visible == [point_e, point_d]
        # Tests collinearity of point_in_polygon
        visible = visible_vertices(point_e, graph, ship, None)
        assert visible == [point_d, ship, point_a]

    def test_visible_vertices_2(self):
        point_a = Point(0.0, 1.0)
        point_b = Point(1.0, 1.0)
        point_c = Point(1.0, 2.0)

        point_d = Point(5.0, 6.0)
        point_e = Point(6.0, 6.0)
        point_f = Point(6.0, 7.0)
        graph = Graph([[point_a, point_b, point_c],
                       [point_d, point_e, point_f]])
        ship = Point(4.0, 5.0)

        visible = visible_vertices(point_d, graph, ship, None)
        assert visible == [point_e, point_f, ship, point_b]
        visible = visible_vertices(ship, graph, ship, None)
        assert visible == [point_e, point_d, point_c, point_b]
        ship = Point(7.0, 8.0)
        visible = visible_vertices(ship, graph, ship, None)
        assert visible == [point_f, point_e]
        ship = Point(6.0, 5.0)
        visible = visible_vertices(ship, graph, ship, None)
        assert visible == [point_e, point_d, point_c, point_b]

    def test_visible_vertices_3(self):
        point_a = Point(0.0, 1.0)
        point_b = Point(2.0, 1.0)
        point_c = Point(1.0, 2.0)

        point_d = Point(3.0, 1.0)
        point_e = Point(5.0, 1.0)
        point_f = Point(4.0, 2.0)
        graph = Graph([[point_a, point_b, point_c],
                       [point_d, point_e, point_f]])

        ship = Point(6.0, 1.0)
        visible = visible_vertices(ship, graph, ship, None)
        assert visible == [point_f, point_e]
        ship = Point(2.5, 3.5)
        visible = visible_vertices(ship, graph, ship, None)
        assert visible == [point_c, point_b, point_d, point_f]
