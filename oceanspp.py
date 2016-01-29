import math

class Graph:
    
    def __init__(self, graph_dict={}):
        self.__graph_dict = graph_dict

    def add_vertex(self, vertex):
        if vertex not in self.__graph_dict:
            self.__graph_dict[vertex] = []

    def add_edge(self, edge):
        (vertex1, vertex2) = tuple(edge)
        if vertex1 in self.__graph_dict:
            self.__graph_dict[vertex1].append(vertex2)
        else:
            self.__graph_dict[vertex1] = [vertex2]

    def vertices(self):
        return self.__graph_dict.keys()

    def edges(self):
        edges = []
        for vertex in self.__graph_dict:
            for neighbour in self.__graph_dict[vertex]:
                if {vertex, neighbour} not in edges:
                    edges.append({vertex, neighbour})
        return edges

    def __str__(self):
        res = "vertices: "
        for vertex in self.__graph_dict:
            res += str(vertex) + " "
        res += "\nedges: "
        for edge in self.edges():
            res += str(edge) + " "
        return res

def edge_distance(vertex1, vertex2):
    return math.sqrt((vertex2[0] - vertex1[0])**2 + (vertex2[1] - vertex1[1])**2)

if __name__ == "__main__":
    g = { (6.0, 1.0) : [(7.0, 2.0), (10.0,1.5)],
          (7.0, 2.0) : [(6.0, 1.0), (8.0, 6.0)],
          (8.0, 6.0) : [(7.0, 2.0), (10.0,1.5)],
          (10.0,1.5) : [(8.0, 6.0), (6.0, 1.0)]
        }

    graph = Graph(g)
    print graph

    for edge in graph.edges():
        res = str(edge) + ": "
        res += str(edge_distance(edge.pop(), edge.pop()))
        print res
