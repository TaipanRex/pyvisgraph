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
from math import sqrt
from collections import defaultdict


class Point:

    def __init__(self, x, y, polygon_id=None):
        self.x = x
        self.y = y
        self.polygon_id = polygon_id

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

    def __repr__(self):
        return "Point(%d, %d)" % (self.x, self.y)


class Edge:

    def __init__(self, point1, point2):
        self.points = (point1, point2)

    def get_adjacent(self, point):
        point_a, point_b = self.points
        if point == point_a:
            return point_b
        return point_a

    def __contains__(self, point):
        return point in self.points

    # TODO: This runs slow, self.points should be a set in __init__
    def __eq__(self, edge):
        return set(self.points) == set(edge.points)

    def __ne__(self, edge):
        return not self.__eq__(edge)

    def __str__(self):
        return "(" + ", ".join(str(p) for p in self.points) + ")"

    def __repr__(self):
        return "Edge(%s, %s)" % (self.points[0].__repr__(), self.points[1].__repr__())

    def __hash__(self):
        hash_val = 0
        for point in self.points:
            hash_val += point.__hash__()
        return hash_val


class Graph:

    '''TODO: polygons is a list of polygons, what if only one polygon is added
    i.e not a list?
    Edges are also generated weirdly
    Need to store as separate polygons'''
    def __init__(self, polygons):
        self.graph = defaultdict(list)
        self.polygon_count = 0
        for polygon in polygons:
            self.polygon_count += 1

            for i, point in enumerate(polygon):
                point.polygon_id = self.polygon_count
                sibling_point = polygon[(i+1) % len(polygon)]
                edge = Edge(point, sibling_point)

                if edge not in self.graph[point]:
                    self.graph[point].append(edge)

                if edge not in self.graph[sibling_point]:
                    self.graph[sibling_point].append(edge)

    def get_adjacent_points(self, point):
        return [edge.get_adjacent(point) for edge in self.graph[point]]

    ''' should return a generator/iterator? or does it already? '''
    def get_points(self):
        return self.graph.keys()

    ''' bad code '''
    def get_edges(self):
        return set([edge for edges in self.graph.values() for edge in edges])

    def __getitem__(self, point):
        if point in self.graph:
            return self.graph[point]
        return []

    def __str__(self):
        res = ""
        for point in self.graph:
            res += "\n" + str(point) + ": "
            for edge in self.graph[point]:
                res += str(edge)
        return res

    def __repr__(self):
        return self.__str__()
