import math
from heapq import heappush, heappop
from matplotlib import pyplot as plt

class Point:
    
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, point):
        return self.x == point.x and self.y == point.y

    def __str__(self):
        return "(" + str(self.x) + ", " + str(self.y) + ")"

    def __hash__(self):
        return self.x.__hash__() + self.y.__hash__()

class Edge:

    def __init__(self, point1, point2):
        self.points = [point1, point2]

    def contains(self, point):
        return self.points[0] == point or self.points[1] == point

    def __eq__(self, edge):
        return set(self.points) == set(edge.points)

    def __str__(self):
        return "(" + str(self.points[0]) + ", " + str(self.points[1]) + ")"

    def __hash__(self):
        hash_val = 0
        for point in self.points:
            hash_val += point.__hash__()
        return hash_val

class Polygon:

    def __init__(self, points, edges):
        self.points = []
        self.edges = []
        for point in points: # add __points
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
        res = "Points: "
        for point in self.points:
            res += str(point) + ";"
        res += "\nEdges: "
        for edge in self.edges:
            res += str(edge) + "\n"
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
            for edge in polygon:
                if edge.contains(point):
                    edges.append(edge)
        return edges

    def __str__(self):
        res = ""
        for i in range(len(self.polygons)):
            res += "Polygon %d\n" % (i)
            res += str(self.polygons[i])
        return res

    '''
    Returns the Euclidean distance between two vertices.
    Can take two vertices or an edge as parameters.
    '''
'''
    @staticmethod
    def edge_distance(*args):
        if len(args) == 1:
            args = args[0]
        return math.sqrt((args[1][0] - args[0][0])**2 + (args[1][1] - args[0][1])**2)

#TODO: If two nodes have the same distance, will the algorithm break?
def shortest_path(graph, ship, port):
    visited = []
    not_visited = graph.vertices()
    not_visited.append(ship)
    distance = {v:float('inf') for v in not_visited}
    distance[port] = 0

    #Calculate distances
    v = None
    ship_edges = []
    while v != ship:
        # 1) Select the vertex with lowest distance
        heap = []
        for vertex in not_visited:
            heappush(heap, (distance[vertex], vertex))
        v = heappop(heap)[1]
        visited.append(v)
        not_visited.remove(v)

        if distance[v] + Graph.edge_distance(v, ship) < distance[ship]:  # 2) cut off edges to the ship node where there is one that is better
            # 3) TODO: Check visibility between vertex and ship
            if v == (8.0, 6.0) or v == (10.0, 1.5):  # Temporary solution, manually add those that are visible to ship
                graph.add_edge((v, ship))
                ship_edges.append((ship, v))
            # 4) Distance update
            for edge in graph.vertex_edges(v):
                v2 = edge[1]
                if distance[v2] > distance[v] + Graph.edge_distance(v, v2):
                    distance[v2] = distance[v] + Graph.edge_distance(v, v2)

    #Find the shortest path
    path = [ship]
    v = None
    heap = []
    for edge in ship_edges:
        heappush(heap, (distance[edge[1]] + Graph.edge_distance(edge), edge))
    v = heappop(heap)[1][1]
    path.append(v)

    while v != port:
        heap = []
        for edge in graph.vertex_edges(v):
            heappush(heap, (distance[edge[1]], edge))
        min_edge = heappop(heap)[1]
        graph.remove_edge(min_edge[1], (min_edge[1], min_edge[0]))
        path.append(min_edge[1])
        v = min_edge[1]
    return path
'''
if __name__ == "__main__":

    #obstacle A
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
    
    #obstacle B
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

    graph = Graph([polygon_a, polygon_b])

    #TODO: This is the operating network
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

    op_network = Graph([Polygon(points, edges)])
    print op_network

'''
    op_graph = { (1.0, 2.0) : [(4.0, 2.5), (1.0, 8.0), (6.0, 1.0)], #A
                 (4.0, 2.5) : [(1.0, 2.0), (5.0, 3.0)], #B
                 (5.0, 3.0) : [(4.0, 2.5), (6.0, 1.0), (8.0, 6.0), (4.5, 5.0)], #C
                 (4.5, 5.0) : [(5.0, 3.0), (4.0, 8.0), (6.0, 1.0)], #D
                 (4.0, 8.0) : [(4.5, 5.0), (1.0, 8.0), (4.0, 7.0), (8.0, 6.0)], #E
                 (1.0, 8.0) : [(1.0, 2.0), (4.0, 8.0)], #F
                 (6.0, 1.0) : [(1.0, 2.0), (5.0, 3.0), (4.5, 5.0), (8.0, 6.0), (10.0, 1.5)], #G
                 (8.0, 6.0) : [(5.0, 3.0), (4.0, 8.0), (6.0, 1.0), (10.0, 1.5)], #H
                 (10.0, 1.5) : [(8.0, 6.0), (6.0, 1.0)], #I
                 (4.0, 7.0) : [(4.0, 8.0)] #J
                }

    graph = Graph(
    op_network = Graph(op_graph)

    #Run shortest path algorithm
    port = (1.0, 2.0)
    ship = (10.0, 5.5)
    shortest = shortest_path(op_network, ship, port)

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
