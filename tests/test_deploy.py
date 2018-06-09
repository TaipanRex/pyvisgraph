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
import shapefile
import pyvisgraph as vg

class TestVisGraphBuild:

    def setup_method(self, method):
        self.sf = shapefile.Reader("examples/shapefiles/GSHHS_c_L1.dbf")
        self.shapes = self.sf.shapes()
        self.polys = []
        self.polys.append([vg.Point(a[0], a[1]) for a in self.shapes[4].points])


    def test_build_1_core(self):
        world = vg.VisGraph()
        world.build(self.polys)
        assert len(world.graph.get_points()) == 310
        assert len(world.graph.get_edges()) == 310
        assert len(world.visgraph.get_edges()) == 1156
        s = "Graph points: {} edges: {}, visgraph edges: {}"
        print(s.format(len(world.graph.get_points()),
                       len(world.graph.get_edges()),
                       len(world.visgraph.get_edges())))

    def test_build_2_core(self):
        world = vg.VisGraph()
        world.build(self.polys, workers=2)
        assert len(world.graph.get_points()) == 310
        assert len(world.graph.get_edges()) == 310
        assert len(world.visgraph.get_edges()) == 1156
        s = "Graph points: {} edges: {}, visgraph edges: {}"
        print(s.format(len(world.graph.get_points()),
                       len(world.graph.get_edges()),
                       len(world.visgraph.get_edges())))


class TestVisGraphMethods:

    def setup_method(self, method):
        self.world = vg.VisGraph()
        self.world.load('world.pk1')
        self.origin = vg.Point(100, -20)
        self.destination = vg.Point(25, 75)

    def test_shortest_path(self):
        shortest = self.world.shortest_path(self.origin, self.destination)
        assert len(shortest) == 19

    def test_shortest_path_not_update_visgraph(self):
        shortest = self.world.shortest_path(self.origin, self.destination)
        assert self.origin not in self.world.visgraph
        assert self.destination not in self.world.visgraph

    def test_shortest_path_not_update_graph(self):
        shortest = self.world.shortest_path(self.origin, self.destination)
        assert self.origin not in self.world.graph
        assert self.destination not in self.world.graph

    def test_update(self):
        self.world.update([self.origin, self.destination])
        assert self.origin in self.world.visgraph
        assert self.destination in self.world.visgraph

    def test_update_not_update_graph(self):
        self.world.update([self.origin, self.destination])
        assert self.origin not in self.world.graph
        assert self.destination not in self.world.graph
