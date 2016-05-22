from __future__ import print_function
from math import pi, sqrt, atan, acos
from graph import Point, Edge, Graph, edge_distance


def visible_vertices(point, graph, ship, port):
    edges = set(graph.get_edges())
    points = graph.get_points()
    points.append(ship)
    points.remove(point)

    ''' Sort points by angle from x-axis with point as center. If angle is same,
    sort by point closest to center. '''
    points.sort(key=lambda p: (angle(point, p), edge_distance(point, p)))

    ''' Initialize open_edges list with any intersecting edges from point to
    the first point in angle sorted point list.'''
    open_edges = []
    for edge in edges:
        if edge_intersect(point, points[0], edge):
            open_edges.append(edge)
    open_edges.sort(key=lambda e: point_edge_distance(point, points[0], edge))

    visible = []
    previous_point = None
    ''' Visit all points in graph to check visibility from point. '''
    for p in points:
        for edge in graph[p]:
                try:
                    open_edges.remove(edge)
                except ValueError:
                    pass
        is_visible = False
        ''' Not ideal, checking each open_edge, but should be able to add new
        open edges in sorted order, so you only check the closest edge.
        Is likely due to concave polygons.'''
        smallest_edge = float('inf')
        for e in open_edges:
            dist = point_edge_distance(point, p, e)
            if dist < smallest_edge:
                smallest_edge = dist
        if not open_edges or edge_distance(point, p) <= smallest_edge:
            if previous_point is not None and angle(point, p) == angle(point, previous_point):
                if edge_distance(point, p) < edge_distance(point, previous_point):
                    is_visible = True
            else:
                is_visible = True
        ''' Check that visibility is not through a polygon '''
        if p.polygon_id == point.polygon_id and p not in graph.get_adjacent_points(point):
            is_visible = False
        if is_visible:
            visible.append(p)

        ''' This should only be needed if I fix open_edges order '''
        edge_order = []
        for edge in graph[p]:
            if (point not in edge) and counterclockwise(point, edge, p):
                edge_order.append((angle2(point, p, edge.get_adjacent(p)), edge))
        edge_order.sort(key=lambda x: x[0])
        for e in edge_order:
            open_edges.append(e[1])
        previous_point = p

    return visible


def angle2(point_a, point_b, point_c):
    a = edge_distance(point_b, point_c)
    b = edge_distance(point_a, point_c)
    c = edge_distance(point_a, point_b)
    return acos((a**2 + c**2 - b**2) / (2*a*c))


def counterclockwise(point, edge, endpoint):
    ''' TODO: merge with ccw() '''
    edge_point1, edge_point2 = edge.points
    if edge_point1 == endpoint:
        angle_diff = angle(point, edge_point2) - angle(point, endpoint)
    else:
        angle_diff = angle(point, edge_point1) - angle(point, endpoint)

    if angle_diff <= 0:
        angle_diff += 2 * pi
    return angle_diff < pi


def point_edge_distance(point1, point2, edge):
    """
    The line going from point1 to point2, intersects edge before reaching
    point2. Return the distance from point1 to this interect point.
    """
    edge_point1, edge_point2 = edge.points

    if edge_point1.x == edge_point2.x:
        if point1.x == point2.x:
            return 0
        points_slope = (point1.y - point2.y) / (point1.x - point2.x)
        intersect_x = edge_point1.x
        intersect_y = points_slope * (intersect_x - point1.x) + point1.y
        return edge_distance(point1, Point(intersect_x, intersect_y))

    if point1.x == point2.x:
        edge_slope = (edge_point1.y - edge_point2.y) / (edge_point1.x - edge_point2.x)
        intersect_x = point1.x
        intersect_y = edge_slope * (intersect_x - edge_point1.x) + edge_point1.y
        return edge_distance(point1, Point(intersect_x, intersect_y))

    points_slope = (point1.y - point2.y) / (point1.x - point2.x)
    edge_slope = (edge_point1.y - edge_point2.y) / (edge_point1.x - edge_point2.x)
    if edge_slope == points_slope:
        return 0
    intersect_x = (edge_slope*edge_point1.x - points_slope*point1.x + point1.y - edge_point1.y) / (edge_slope - points_slope)
    intersect_y = edge_slope * (intersect_x - edge_point1.x) + edge_point1.y
    return edge_distance(point1, Point(intersect_x, intersect_y))


def angle(center, point):
    """
    Return the angle of 'point' where 'center' is the center of
    the radian circle.
    """
    dx = point.x - center.x
    dy = point.y - center.y
    if dx == 0:
        if dy < 0:
            return pi*3 / 2
        return pi / 2
    if dy == 0:
        if dx < 0:
            return pi
        return 0
    if dx < 0:
        return pi + atan(dy/dx)
    if dy < 0:
        return 2*pi + atan(dy/dx)
    return atan(dy/dx)


def ccw(A, B, C):
    return (C.y-A.y) * (B.x-A.x) > (B.y-A.y) * (C.x-A.x)


def edge_intersect(A, B, edge):
    """
    Return True if 'edge' is interesected by the line going through 'A' and
    'B', False otherwise. If edge contains either 'A' or 'B', return False.
    TODO: May be an issue with colinerity here. See:
    http://www.geeksforgeeks.org/check-if-two-given-line-segments-intersect/
    """
    C, D = edge.points
    if A in edge or B in edge:
        return False
    return ccw(A, C, D) != ccw(B, C, D) and ccw(A, B, C) != ccw(A, B, D)
