from math import sqrt


class Point:

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, point):
        if point is None:
            return False
        return self.x == point.x and self.y == point.y

    def __ne__(self, point):
        return not self.__eq__(point)

    def __str__(self):
        return "(" + str(self.x) + ", " + str(self.y) + ")"

    def __hash__(self):
        '''TODO: Will this mess something up with Edge comparison? if one
        point is x, y and other y, x?'''
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

    '''TODO: polygons is a list of polygons, what if only one polygon is added
    i.e not a list?'''
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
    return sqrt((point2.x - point1.x)**2 + (point2.y - point1.y)**2)
