from __future__ import print_function
from math import pi, sqrt, atan, acos
from graph import Point, Edge, Polygon, Graph, edge_distance


def visible_vertices(point, graph, ship, port):
    points = graph.get_points()
    edges = graph.get_edges()
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
        for edge in graph.get_point_edges(p):
                try:
                    open_edges.remove(edge)
                except ValueError:
                    pass

        if len(open_edges) == 0 or edge_distance(point, p) <= point_edge_distance(point, p, open_edges[0]):
            if previous_point is not None and angle(point, p) == angle(point, previous_point):
                if edge_distance(point, p) < edge_distance(point, previous_point):
                    visible.append(p)
            else:
                visible.append(p)

        edge_order = []
        for edge in graph.get_point_edges(p):
            if (not edge.contains(point)) and counterclockwise(point, edge, p):
                edge_order.append((angle2(point, p, edge.get_adjacent(p)), edge))
        edge_order.sort(key=lambda x: x[0])
        for e in edge_order:
            open_edges.append(e[1])
        previous_point = p

    # remove edges that cross through polygons. Must be a better way...
    for polygon in graph.polygons:
        if point in polygon.points:
            for p in polygon.points:
                if not Edge(point, p) in polygon.edges:
                    try:
                        visible.remove(p)
                    except ValueError:
                        pass

    return visible


def angle2(point_a, point_b, point_c):
    a = edge_distance(point_b, point_c)
    b = edge_distance(point_a, point_c)
    c = edge_distance(point_a, point_b)
    return acos((a**2 + c**2 - b**2) / (2*a*c))


def counterclockwise(point, edge, endpoint):
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
        else:
            return pi / 2
    if dy == 0:
        if dx < 0:
            return pi
        else:
            return 0

    if dx < 0:
        return pi + atan(dy/dx)
    if dy < 0:
        return 2*pi + atan(dy/dx)

    return atan(dy/dx)


def edge_intersect(point1, point2, edge):
    """
    Return True if 'edge' is interesected by the line going
    through 'point1' and 'point2', False otherwise.
    If edge contains either 'point1' or 'point2', return False.
    """
    edge_point1, edge_point2 = edge.points
    if edge.contains(point1) or edge.contains(point2):
        return False

    if point1.x == point2.x:
        x1_left = edge_point1.x < point1.x
        x2_left = edge_point2.x < point1.x
        return not (x1_left == x2_left)

    slope = (point1.y - point2.y) / (point1.x - point2.x)

    y1_ex = slope * (edge_point1.x - point1.x) + point1.y
    y2_ex = slope * (edge_point2.x - point1.x) + point1.y

    if y1_ex == edge_point1.y or y2_ex == edge_point2.y:
        return False

    y1_below = (y1_ex > edge_point1.y)
    y2_below = (y2_ex > edge_point2.y)
    return not (y1_below == y2_below)
