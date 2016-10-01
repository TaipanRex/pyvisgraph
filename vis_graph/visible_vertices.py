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
from math import pi, sqrt, atan, acos
from graph import Point, Edge, Graph
from utils.avl import AVLTree


def visible_vertices(point, graph, origin=None, destination=None):
    """Returns list of Points in 'graph' visible by 'point'.

    Args:
        point: Point to check visibility from.
        graph: Graph to check visibility against.
        origin: A optional origin/starting Point included in visibility test
        destination: A optional destination Point included in visibility test
    """
    edges = graph.get_edges()
    points = graph.get_points()
    if origin: points.append(origin)
    if destination: points.append(destination)
    points.sort(key=lambda p: (angle(point, p), edge_distance(point, p)))

    # Initialize open_edges list with any intersecting edges from point to
    # the first point in angle sorted point list.
    open_edges = AVLTree()
    point_inf = Point(10000.0, point.y)
    for e in edges:
        if point in e:
            continue
        if edge_intersect(point, point_inf, e):
            i = intersect_point(point, point_inf, e)
            if e.points[0].y > i.y or e.points[1].y > i.y:
                k = EdgeKey(point, point_inf, e)
                open_edges.insert(k)

    visible = []
    prev_point = None
    for p in points:
        if p == point: continue

        for edge in graph[p]:
            if ccw(point, p, edge.get_adjacent(p)) == -1:
                k = EdgeKey(point, p, edge)
                open_edges.delete(k)
        is_visible = False

        smallest_edge = open_edges.smallest()
        if not smallest_edge or edge_distance(point, p) <= point_edge_distance(point, p, smallest_edge.edge):
            if prev_point and angle(point, p) == angle(point, prev_point):
                if edge_distance(point, p) < edge_distance(point, prev_point):
                    is_visible = True
            else:
                is_visible = True

        # Check that visibility is not through a polygon.
        # TODO: In Graph, add a attribute that states if a polygon is convex
        # or not (http://bit.ly/1RsvqpO). If polygon is convex, it is simple
        # to check if point in polygon.
        if is_visible and p.polygon_id == point.polygon_id:
            if p not in graph.get_adjacent_points(point):
                is_visible = point_in_polygon(point, p, graph.get_edges())

        if is_visible: visible.append(p)
        for edge in graph[p]:
            if (point not in edge) and ccw(point, p, edge.get_adjacent(p)) == 1:
                k = EdgeKey(point, p, edge)
                open_edges.insert(k)

        prev_point = p

    return visible


def point_in_polygon(p1, p2, graph_edges):
    mid_p1 = Point((p1.x + p2.x) / 2, (p1.y + p2.y) / 2)
    mid_p2 = Point(float('inf'), mid_p1.y)
    intersect_count = 0
    co_flag = False
    co_dir = 0
    for edge in graph_edges:
        # TODO: Implement a Polygon class. Pull edges from that and not
        # from the whole graph as below.
        if edge.points[0].polygon_id == p1.polygon_id:
            # collinear points on right side
            co0 = ccw(mid_p1, edge.points[0], mid_p2) == 0 and edge.points[0].x > mid_p1.x
            co1 = ccw(mid_p1, edge.points[1], mid_p2) == 0 and edge.points[1].x > mid_p1.x
            co_point = edge.points[0] if co0 else edge.points[1]
            if co0 or co1:
                if edge.get_adjacent(co_point).y > mid_p1.y:
                    co_dir += 1
                else:
                    co_dir -= 1
                if co_flag:
                    if co_dir == 0: intersect_count += 1
                    co_flag = False
                    co_dir = 0
                else:
                    co_flag = True
            elif edge_intersect(mid_p1, mid_p2, edge):
                intersect_count += 1
    if intersect_count % 2 == 0:
        return True
    return False


def edge_distance(p1, p2):
    """Return the Euclidean distance between two Points."""
    return sqrt((p2.x - p1.x)**2 + (p2.y - p1.y)**2)


def point_edge_distance(p1, p2, edge):
    """The line going from point1 to point2, intersects edge before reaching
    point2. Return the distance from point1 to this interect point.
    """
    intersect_p = intersect_point(p1, p2, edge)
    if intersect_p is not None:
        return edge_distance(p1, intersect_p)
    return 0


def intersect_point(p1, p2, edge):
    edge_p1, edge_p2 = edge.points

    if edge_p1.x == edge_p2.x:
        if p1.x == p2.x:
            return None
        pslope = (p1.y - p2.y) / (p1.x - p2.x)
        intersect_x = edge_p1.x
        intersect_y = pslope * (intersect_x - p1.x) + p1.y
        return Point(intersect_x, intersect_y)

    if p1.x == p2.x:
        eslope = (edge_p1.y - edge_p2.y) / (edge_p1.x - edge_p2.x)
        intersect_x = p1.x
        intersect_y = eslope * (intersect_x - edge_p1.x) + edge_p1.y
        return Point(intersect_x, intersect_y)

    pslope = (p1.y - p2.y) / (p1.x - p2.x)
    eslope = (edge_p1.y - edge_p2.y) / (edge_p1.x - edge_p2.x)
    if eslope == pslope:
        return None
    intersect_x = (eslope * edge_p1.x - pslope * p1.x + p1.y - edge_p1.y) / (eslope - pslope)
    intersect_y = eslope * (intersect_x - edge_p1.x) + edge_p1.y
    return Point(intersect_x, intersect_y)


def angle(center, point):
    """Return the angle of 'point' from the 'center' of the radian circle."""
    dx = point.x - center.x
    dy = point.y - center.y
    if dx == 0:
        if dy < 0:
            return pi * 3 / 2
        return pi / 2
    if dy == 0:
        if dx < 0:
            return pi
        return 0
    if dx < 0:
        return pi + atan(dy / dx)
    if dy < 0:
        return 2 * pi + atan(dy / dx)
    return atan(dy / dx)


def angle2(point_a, point_b, point_c):
    a = edge_distance(point_b, point_c)
    b = edge_distance(point_a, point_c)
    c = edge_distance(point_a, point_b)
    x = (a**2 + c**2 - b**2) / (2 * a * c)
    return acos(round(x, 5))


def ccw(A, B, C):
    area = (B.x - A.x) * (C.y - A.y) - (B.y - A.y) * (C.x - A.x)
    if area > 0: return 1  # ccw
    if area < 0: return -1  # cw
    return 0  # collinear


def edge_intersect(A, B, edge):
    """Return True if 'edge' is interesected by the line going through 'A' and
    'B', False otherwise. If edge contains either 'A' or 'B', return False.
    """
    # TODO: May be an issue with colinerity or intersections at vertex points.
    # http://www.geeksforgeeks.org/check-if-two-given-line-segments-intersect/
    C, D = edge.points
    return ccw(A, C, D) != ccw(B, C, D) and ccw(A, B, C) != ccw(A, B, D)


class EdgeKey:
    def __init__(self, p1, p2, edge):
        self.p1 = p1
        self.p2 = p2
        self.edge = edge

    def __cmp__(self, other):
        if self.edge == other.edge:
            return 0
        # if other p2 is in both edges, distance is equal and we need the angle
        if other.p2 in self.edge:
            aslf = angle2(other.p1, other.p2, self.edge.get_adjacent(other.p2))
            aot = angle2(other.p1, other.p2, other.edge.get_adjacent(other.p2))
            if aot < aslf:
                return 1
            return -1
        # if no intersect with self, self > other
        if not edge_intersect(other.p1, other.p2, self.edge):
            return 1
        # last case is where we need to recalculate distance for me, other is edge_distance p1,p2
        self_dist = point_edge_distance(other.p1, other.p2, self.edge)
        other_dist = point_edge_distance(other.p1, other.p2, other.edge)
        if self_dist > other_dist:
            return 1
        return -1

    def __repr__(self):
        reprstring = (self.__class__.__name__, self.edge, self.p1, self.p2)
        return "{}(Edge={!r}, p1={!r}, p2={!r})".format(*reprstring)
