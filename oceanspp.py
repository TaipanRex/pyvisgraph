from math import pi, sqrt, atan
from matplotlib import pyplot as plt

class Point:

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, point):
        if point == None:
            return False
        return self.x == point.x and self.y == point.y

    def __ne__(self, point):
        return not self.__eq__(point)

    def __str__(self):
        return "(" + str(self.x) + ", " + str(self.y) + ")"

    def __hash__(self):
        # TODO: Will this mess something up with Edge comparison? if one point is x, y and other y, x?
        return self.x.__hash__() + self.y.__hash__()

class Edge:

    def __init__(self, point1, point2):
        self.points = (point1, point2)

    def contains(self, point):
        return point in self.points

    def get_adjacent(self, point):
        point_a, point_b = self.points
        if point == point_a:
            return point_b
        return point_a

    def __eq__(self, edge):
        return set(self.points) == set(edge.points)

    def __ne__(self, edge):
        return not self.__eq__(edge)

    def __str__(self):
        return "(" + ", ".join(str(p) for p in self.points) + ")"

    def __hash__(self):
        hash_val = 0
        for point in self.points:
            hash_val += point.__hash__()
        return hash_val

class Polygon:

    def __init__(self, points, edges):
        self.points = []
        self.edges = []
        for point in points:
            if point not in self.points:
                self.points.append(point)
        for edge in edges:
            if edge not in self.edges:
                self.edges.append(edge)

    def add_point(self, point):
        if point not in self.points:
            self.points.append(point)

    def add_edge(self, edge):
        if edge not in self.edges:
            self.edges.append(edge)

    def __str__(self):
        res = "Points: " + ', '.join(str(p) for p in self.points)
        res += "\nEdges: " + ', '.join(str(e) for e in self.edges)
        return res

class Graph:

    # TODO: polygons is a list of polygons, what if only one polygon is added i.e not a list?
    def __init__(self, polygons):
        self.polygons = polygons

    def get_points(self):
        points = []
        for polygon in self.polygons:
            points += polygon.points
        return points

    def get_edges(self):
        edges = []
        for polygon in self.polygons:
            edges += polygon.edges
        return edges

    def get_point_edges(self, point):
        edges = []
        for polygon in self.polygons:
            for edge in polygon.edges:
                if edge.contains(point):
                    edges.append(edge)
        return edges

    def __str__(self):
        s = ""
        for i, polygon in enumerate(self.polygons):
            s += "Polygon %d\n" % i
            s += str(polygon)
        return s

def edge_distance(point1, point2):
    """
    Return the Euclidean distance between two Points.
    """
    return sqrt((point2.x - point1.x)**2
                + (point2.y - point1.y)**2)

def point_edge_distance(point1, point2, edge):
    """
    The line going from point1 to point2, interects edge before reaching
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

#TODO: If two nodes have the same distance, will the algorithm break?
def shortest_path(graph, ship, port):
    visited = []
    not_visited = graph.get_points()
    not_visited.append(ship)
    distance = {point: float('inf') for point in not_visited}
    distance[port] = 0

    #Calculate distances
    point = None
    while point != ship:
        point = min(not_visited, key=lambda p: distance[p])
        visited.append(point)
        not_visited.remove(point)

        # Cut off edges to the ship when there is one that is better
        if distance[point] + edge_distance(point, ship) < distance[ship]:
            # TODO: Check visibility between vertex and ship
            if point == Point(8.0, 6.0) or point == Point(10.0, 1.5):
                graph.polygons[0].add_edge(Edge(point, ship)) # TODO: Ugly, add separate Edges?
            # Distance update
            for edge in graph.get_point_edges(point):
                point2 = edge.get_adjacent(point)
                if distance[point2] > distance[point] + edge_distance(point, point2):
                    distance[point2] = distance[point] + edge_distance(point, point2)

    #Return the shortest path
    path = []
    point = ship

    while point != port:
        min_edge = min(graph.get_point_edges(point), key=lambda e: distance[edge.get_adjacent(point)])
        path.append(min_edge)
        point = min_edge.get_adjacent(point)
    return path
