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
from pyvisgraph.graph import Graph, Point, Edge
from pyvisgraph.visible_vertices import edge_intersect, point_edge_distance
from pyvisgraph.visible_vertices import visible_vertices, angle, point_in_polygon
from pyvisgraph.visible_vertices import intersect_point, edge_distance
from math import pi, degrees, cos, sin
import pyvisgraph as vg

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
    point_i = Point(4.0, 4.0)
    edge = Edge(point_a, point_b)
    assert edge_intersect(point_c, point_d, edge) is True
    assert edge_intersect(point_c, point_e, edge) is True
    assert edge_intersect(point_f, point_e, edge) is True
    assert edge_intersect(point_g, point_b, edge) is True
    assert edge_intersect(point_c, point_h, edge) is True
    assert edge_intersect(point_h, point_i, edge) is True


def test_point_edge_distance_function():
    point_a = Point(3.0, 1.0)
    point_b = Point(3.0, 5.0)
    point_c = Point(2.0, 2.0)
    point_d = Point(4.0, 4.0)
    point_e = Point(1.0, 1.0)
    point_f = Point(1.0, 2.0)
    point_g = Point(3.0, 4.0)
    point_h = Point(2.0, 5.0)
    edge = Edge(point_a, point_b)
    edge2 = Edge(point_c, point_d)
    edge3 = Edge(point_e, point_b)
    assert point_edge_distance(point_c, point_d, edge) == 1.4142135623730951
    assert point_edge_distance(point_a, point_b, edge2) == 2.0
    assert point_edge_distance(point_f, point_g, edge3) == 1.4142135623730951
    assert point_edge_distance(point_h, point_g, edge3) == 0.9428090415820635


def test_point_in_polygon():
    g = vg.VisGraph()
    point_a = Point(0,0)
    point_b = Point(4,0)
    point_c = Point(2,4)
    point_d = Point(1,0.5)
    g.build([[point_a, point_b, point_c]])
    assert g.point_in_polygon(point_d) != -1


class TestClosestPoint:

    def setup_method(self, method):
        self.g = vg.VisGraph()
        self.point_a = Point(0,0)
        self.point_b = Point(4,0)
        self.point_c = Point(2,4)
        self.point_d = Point(1,0.5)
        self.g.build([[self.point_a, self.point_b, self.point_c]])

    def test_closest_point(self):
        pid = self.g.point_in_polygon(self.point_d)
        cp = self.g.closest_point(self.point_d, pid)
        assert self.g.point_in_polygon(cp) == -1

    def test_closest_point_length(self):
        pid = self.g.point_in_polygon(self.point_d)
        cp = self.g.closest_point(self.point_d, pid, length=0.5)
        ip = intersect_point(self.point_d, cp, Edge(self.point_a, self.point_b))
        assert edge_distance(ip, cp) == 0.5

    def test_closest_point_edge_point(self):
        """Test where the cp is a end-point of a polygon edge. Can end up with
        cp extending into polygon instead of outside it."""
        g = vg.VisGraph()
        g.build([[Point(0,1), Point(2,0), Point(1,1), Point(2,2)]])
        p = Point(1,0.9)
        pid = g.point_in_polygon(p)
        cp = g.closest_point(p, pid, length=0.001)
        assert g.point_in_polygon(cp) == -1


class TestCollinear:

    def setup_method(self, method):
        self.point_a = Point(0.0, 1.0)
        self.point_b = Point(1.0, 0.0)
        self.point_c = Point(2.0, 3.0)
        self.point_d = Point(3.0, 2.0)
        self.point_e = Point(3.5, 0.5)
        self.point_f = Point(4.5, 3.5)

    def test_collin1(self):
        graph = Graph([[self.point_a, self.point_b, self.point_c],
                       [self.point_d, self.point_e, self.point_f]])
        visible = visible_vertices(Point(1,4), graph, None, None)
        assert visible == [self.point_a, self.point_c, self.point_d, self.point_f]

    def test_collin2(self):
        self.point_g = Point(2.0, 5.0)
        self.point_h = Point(3.0, 5.0)
        graph = Graph([[self.point_g, self.point_h, self.point_c],
                       [self.point_d, self.point_e, self.point_f]])
        visible = visible_vertices(Point(1,4), graph, None, None)
        assert visible == [self.point_g, self.point_e, self.point_c, self.point_d]

    def test_collin3(self):
        point_g = Point(2.0, 2.0)
        point_h = Point(3.5, 5.0)
        point_i = Point(2.5, 2.0)
        graph = Graph([[self.point_a, self.point_b, self.point_c],
                       [point_g, point_h, point_i],
                       [self.point_d, self.point_e, self.point_f]])
        visible = visible_vertices(Point(1,4), graph, None, None)
        assert visible == [point_h, self.point_a, self.point_c]

    def test_collin4(self):
        graph = Graph([[Point(1,1), Point(2,3), Point(3,1),Point(2,2)],
                      [Point(2,4)]])
        visible = visible_vertices(Point(2,1), graph, None, None)
        assert visible == [Point(3,1), Point(2,2), Point(1,1)]

    def test_collin5(self):
        r = 0.2  # Radius of polygon
        n = 4  # Sides of polygon
        c = Point(1.0, 1.0)  # Center of polygon
        verts = []
        for i in range(n):
            verts.append(Point(r * cos(2*pi * i/n - pi/4) + c.x,
                               r * sin(2*pi * i/n - pi/4) + c.y))
        g = vg.VisGraph()
        g.build([verts])
        s = Point(0, 0)
        t = Point(1.7, 1.7)
        shortest = g.shortest_path(s, t)
        visible = visible_vertices(t, g.graph, s, None)
        assert verts[3] not in visible
        assert verts[1] not in shortest
        assert verts[3] not in shortest

    """ See https://github.com/TaipanRex/pyvisgraph/issues/20.
    This tests colinearity case #1 using point_in_polygon."""
    def test_collin6(self):
        graph = Graph([[Point(0,0), Point(2,1), Point(0,2)]])
        pip = point_in_polygon(Point(1,1), graph)
        assert pip > -1

    """ See https://github.com/TaipanRex/pyvisgraph/issues/20.
    This tests colinearity case #2 using point_in_polygon."""
    def test_collin7(self):
        graph = Graph([[Point(0,0), Point(1,1), Point(2,0), Point(2,2), Point(0,2)]])
        pip = point_in_polygon(Point(0.5,1), graph)
        assert pip > -1

    """ See https://github.com/TaipanRex/pyvisgraph/issues/20.
    This tests colinearity case #3 using point_in_polygon."""
    def test_collin8(self):
        graph = Graph([[Point(0,0), Point(2,0), Point(2,2), Point(1,1), Point(0,2)]])
        pip = point_in_polygon(Point(0.5,1), graph)
        assert pip > -1

    """ See https://github.com/TaipanRex/pyvisgraph/issues/20.
    This tests colinearity case #4 using point_in_polygon."""
    def test_collin9(self):
        graph = Graph([[Point(0,0), Point(1,0), Point(1,1), Point(2,1), Point(2,2),
                        Point(0,2)]])
        pip = point_in_polygon(Point(0.5,1), graph)
        assert pip > -1

    """ See https://github.com/TaipanRex/pyvisgraph/issues/20.
    This tests colinearity case #5 using point_in_polygon."""
    def test_collin10(self):
        graph = Graph([[Point(0,0), Point(1,0), Point(1,1), Point(2,1), Point(2,0),
                        Point(3,0), Point(3,2), Point(0,2)]])
        pip = point_in_polygon(Point(0.5,1), graph)
        assert pip > -1

    """ See https://github.com/TaipanRex/pyvisgraph/issues/20.
    This tests colinearity case #6 using point_in_polygon."""
    def test_collin11(self):
        graph = Graph([[Point(0,0), Point(3,0), Point(3,2), Point(2,3), Point(2,1),
                        Point(1,1), Point(1,2), Point(0,2)]])
        pip = point_in_polygon(Point(0.5,1), graph)
        assert pip > -1