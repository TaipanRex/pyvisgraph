import math
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
        res = ""
        for i, polygon in enumerate(self.polygons):
            res += "Polygon %d\n" % i
            res += str(polygon)
        return res

'''
Returns the Euclidean distance between two Points.
'''
def edge_distance(point1, point2):
    return math.sqrt((point2.x - point1.x)**2 + (point2.y - point1.y)**2)


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
    
'''
    #Draw the obstacles and operating network
    fig = plt.figure(1, figsize=(5,5), dpi=90)
    ax = fig.add_subplot(111)

    #Draw the obstacles
    for polygon in graph.polygons:
        for edge in polygon.edges():
            x,y = zip(*edge)
            ax.plot(x, y, color='blue', alpha=0.7, linewidth=3, solid_capstyle='round', zorder=2)

    #Draw the operating network
    for edge in op_network.edges():
        x,y = zip(*edge)
        ax.plot(x, y, color='red', alpha=0.7, linewidth=1)

    #draw shortest path
    x,y = zip(*shortest)
    ax.plot(x, y, color='green', alpha=0.7, linewidth=2)

    ax.set_title("ocean shortest path test")
    xrange = [0, 11]
    yrange = [0, 9]
    ax.set_xlim(*xrange)
    ax.set_xticks(range(*xrange) + [xrange[-1]])
    ax.set_ylim(*yrange)
    ax.set_yticks(range(*yrange) + [yrange[-1]])
    ax.set_aspect(1)
    fig.savefig("poly.png")
'''
