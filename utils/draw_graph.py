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
import matplotlib.pyplot as plt
from vis_graph.graph import Point


def draw_graph(polygons):
    fig = plt.figure(1, figsize=(5, 5), dpi=90)
    ax = fig.add_subplot(111)
    for polygon in polygons:
        if len(polygon) == 1:
            ax.plot(polygon[0].x, polygon[0].y, 'ro')
        else:
            x = [p.x for p in polygon]
            y = [p.y for p in polygon]
            ax.plot(x, y, linewidth=2.0)

    ax.set_title("Plot polygons")
    fig.savefig("plot.png", bbox_inches='tight')
draw_graph([[Point(0.0, 1.0), Point(1.0, 1.0), Point(1.0, 2.0), Point(0.0, 1.0)], [Point(5.0, 6.0), Point(6.0, 6.0), Point(6.0, 7.0), Point(5.0, 6.0)], [Point(4.0, 5.0)]])
