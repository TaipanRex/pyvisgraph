# Python Visibility Graph

[![MIT License](https://img.shields.io/badge/license-MIT-007EC7.svg?style=flat)](/LICENSE.txt)
![PyPI](https://img.shields.io/badge/pypi-not%20released-lightgrey.svg?style=flat)

![Figure 1](docs/images/graph.png)

Given a set of simple obstacle polygons, this solution will return the
visibility graph. It can also find the shortest path between two points using
Djikstra's shortest path algorithm.

Please see [https://en.wikipedia.org/wiki/Visibility_graph](https://en.wikipedia.org/wiki/Visibility_graph)
for an explanation of visibility graphs and their applications.

I am implementing this first using Lee's Algorithm, which runs in O(n^2 log n)
time. Please see my [explanation](docs/lees_algorithm.md) of the algorithm and
implementation.
