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
from graph import Point


def visible_vertices(point, graph, origin=None, destination=None, scan='full'):
    """Returns list of Points in graph visible by point.

    If origin and/or destination Points are given, these will also be checked
    for visibility. scan 'full' will check for visibility against all points in
    graph, 'half' will check for visibility against half the points. This saves
    running time when building a complete visibility graph, as the points
    that are not checked will eventually be 'point'.
    """
    edges = graph.get_edges()
    points = graph.get_points()
    if origin: points.append(origin)
    if destination: points.append(destination)
    points.sort(key=lambda p: (angle(point, p), edge_distance(point, p)))

    # Initialize open_edges with any intersecting edges on the half line from
    # point along the positive x-axis
    open_edges = []
    point_inf = Point(float('inf'), point.y)
    for e in edges:
        if point in e: continue
        if edge_intersect(point, point_inf, e):
            ip = intersect_point(point, point_inf, e)
            if e.p1.y > ip.y or e.p2.y > ip.y:
                k = EdgeKey(point, point_inf, e)
                insort(open_edges, k)

    visible = []
    prev_point = None
    for p in points:
        if p == point: continue
        if scan == 'half' and angle(point, p) > pi: break

        # Remove clock wise edges incident on p
        if open_edges:
            for edge in graph[p]:
                if ccw(point, p, edge.get_adjacent(p)) == -1:
                    k = EdgeKey(point, p, edge)
                    index = bisect(open_edges, k) - 1
                    if open_edges[index] == k:
                        del open_edges[index]

        # Check if p is visible from point
        is_visible = False
        smallest_edge = None
        if len(open_edges) > 0:
            smallest_edge = open_edges[0].edge
        if not smallest_edge or edge_distance(point, p) <= point_edge_distance(point, p, smallest_edge):
            if prev_point and angle(point, p) == angle(point, prev_point):
                if edge_distance(point, p) < edge_distance(point, prev_point):
                    is_visible = True
            else:
                is_visible = True

        # Check if the visible edge is interior to its polygon
        if is_visible and p not in graph.get_adjacent_points(point):
            is_visible = not edge_in_polygon(point, p, graph)

        if is_visible: visible.append(p)

        # Add counter clock wise edges incident on p to open_edges
        for edge in graph[p]:
            if (point not in edge) and ccw(point, p, edge.get_adjacent(p)) == 1:
                k = EdgeKey(point, p, edge)
                insort(open_edges, k)

        prev_point = p
    return visible


def polygon_crossing(p1, poly_edges):
    """Returns True if Point p1 is internal to the polygon

    The polygon is defined by the Edges in poly_edges. Uses crossings
    algorithm and takes into account edges that are collinear to p1.
    """

    p2 = Point(float('inf'), p1.y)
    intersect_count = 0
    co_flag = False
    co_dir = 0
    for edge in poly_edges:
        if p1.y < edge.p1.y and p1.y < edge.p2.y:
            continue
        if p1.y > edge.p1.y and p1.y > edge.p2.y:
            continue
        # collinear points on right side
        co0 = ccw(p1, edge.p1, p2) == 0 and edge.p1.x > p1.x
        co1 = ccw(p1, edge.p2, p2) == 0 and edge.p2.x > p1.x
        co_point = edge.p1 if co0 else edge.p2
        if co0 or co1:
            if edge.get_adjacent(co_point).y > p1.y:
                co_dir += 1
            else:
                co_dir -= 1
            if co_flag:
                if co_dir == 0: intersect_count += 1
                co_flag = False
                co_dir = 0
            else:
                co_flag = True
        elif edge_intersect(p1, p2, edge):
            intersect_count += 1
    if intersect_count % 2 == 0:
        return False
    return True


def edge_in_polygon(p1, p2, graph):
    if p1.polygon_id != p2.polygon_id:
        return False
    if p1.polygon_id == -1 or p2.polygon_id == -1:
        return False
    mid_point = Point((p1.x + p2.x) / 2, (p1.y + p2.y) / 2)
    return polygon_crossing(mid_point, graph.polygons[p1.polygon_id])


# TODO: Check if point is in polygon bounding box first
def point_in_polygon(p, graph):
    for polygon in graph.polygons:
        if polygon_crossing(p, graph.polygons[polygon]):
            return polygon
    return -1


def closest_point(p, graph, polygon_id):
    polygon_edges = graph.polygons[polygon_id]
    smallest_dist = None
    smallest_point = None
    for i, e in enumerate(polygon_edges):
        u = ((p.x-e.p1.x)*(e.p2.x-e.p1.x)+(p.y-e.p1.y)*(e.p2.y-e.p1.y))/((e.p2.x - e.p1.x)**2 + (e.p2.y - e.p1.y)**2)
        pu = Point(e.p1.x + u*(e.p2.x - e.p1.x), e.p1.y + u*(e.p2.y- e.p1.y))
        pc = pu
        if u < 0:
            pc = e.p1
        elif u > 1:
            pc = e.p2
        d = edge_distance(p, pc)
        if i == 0 or d < smallest_dist:
            smallest_dist = d
            smallest_point = pc
    return smallest_point


def edge_distance(p1, p2):
    """Return the Euclidean distance between two Points."""

    return sqrt((p2.x - p1.x)**2 + (p2.y - p1.y)**2)


def intersect_point(p1, p2, edge):
    """Return intersect Point where the edge from p1, p2 intersects edge"""

    if edge.p1.x == edge.p2.x:
        if p1.x == p2.x:
            return None
        pslope = (p1.y - p2.y) / (p1.x - p2.x)
        intersect_x = edge.p1.x
        intersect_y = pslope * (intersect_x - p1.x) + p1.y
        return Point(intersect_x, intersect_y)

    if p1.x == p2.x:
        eslope = (edge.p1.y - edge.p2.y) / (edge.p1.x - edge.p2.x)
        intersect_x = p1.x
        intersect_y = eslope * (intersect_x - edge.p1.x) + edge.p1.y
        return Point(intersect_x, intersect_y)

    pslope = (p1.y - p2.y) / (p1.x - p2.x)
    eslope = (edge.p1.y - edge.p2.y) / (edge.p1.x - edge.p2.x)
    if eslope == pslope:
        return None
    intersect_x = (eslope * edge.p1.x - pslope * p1.x + p1.y - edge.p1.y) / (eslope - pslope)
    intersect_y = eslope * (intersect_x - edge.p1.x) + edge.p1.y
    return Point(intersect_x, intersect_y)


def point_edge_distance(p1, p2, edge):
    """Return the Eucledian distance from p1 to intersect point with edge.

    The line going from p1 to p2 intersects edge before reaching p2.
    """

    ip = intersect_point(p1, p2, edge)
    if ip is not None:
        return edge_distance(p1, ip)
    return 0


def angle(center, point):
    """Return the angle (radian) of point from center of the radian circle.

     ------p
     |   /
     |  /
    c|a/
    """

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
    """Return 1 if counter clockwise, -1 if clock wise, 0 if collinear """

    area = (B.x - A.x) * (C.y - A.y) - (B.y - A.y) * (C.x - A.x)
    if area > 0: return 1  # counter clock wise
    if area < 0: return -1  # clock wise
    return 0  # collinear


def edge_intersect(A, B, edge):
    """Return True if edge from A, B interects edge.

    If edge contains either 'A' or 'B', return False.
    """

    # TODO: May be an issue with colinerity or intersections at vertex points.
    # http://www.geeksforgeeks.org/check-if-two-given-line-segments-intersect/
    C = edge.p1
    D = edge.p2
    return ccw(A, C, D) != ccw(B, C, D) and ccw(A, B, C) != ccw(A, B, D)

def insort(a, x):
    lo = 0
    hi = len(a)
    while lo < hi:
        mid = (lo+hi)//2
        if a[mid] > x: hi = mid
        else: lo = mid+1
    a.insert(lo, x)

def bisect(a, x):
    lo = 0
    hi = len(a)
    while lo < hi:
        mid = (lo+hi)//2
        if a[mid] > x: hi = mid
        else: lo = mid+1
    return lo

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
        # if distance is equal, need to check angle
        self_dist = point_edge_distance(other.p1, other.p2, self.edge)
        other_dist = point_edge_distance(other.p1, other.p2, other.edge)
        if self_dist > other_dist:
            return 1
        if self_dist < other_dist:
            return -1
        elif self_dist == other_dist:
            if self.edge.p1 == other.edge.p1 or self.edge.p1 == other.edge.p2:
                same_point = self.edge.p1
            elif self.edge.p2 == other.edge.p1 or self.edge.p2 == other.edge.p2:
                same_point = self.edge.p2
            aslf = angle2(other.p1, other.p2, self.edge.get_adjacent(same_point))
            aot = angle2(other.p1, other.p2, other.edge.get_adjacent(same_point))
            if aot < aslf:
                return 1
            return -1

    def __repr__(self):
        reprstring = (self.__class__.__name__, self.edge, self.p1, self.p2)
        return "{}(Edge={!r}, p1={!r}, p2={!r})".format(*reprstring)
