.. _manual:

#######################
Pyvisgraph User Manual
#######################
:Author: Christian Reksten-Monsen, <christian@reksten-monsen.com>
:Version: 0.0.1
:Date: |today|
:Copyright:
  This document is licensed under the `MIT License`__.

.. __: https://opensource.org/licenses/MIT

:Abstract:
  This document explains how to use the Pyvisgraph to build the visibility graph
  for a given list of simple obstacle polygons, then find the shortest path
  between two points.

.. _intro:

Introduction
=============

Pyvisgraph is a MIT-licensed Python package for building visibility graphs from
a list of simple obstacle polygons. The visibility graph algorithm (D.T. Lee)
runs in O(n^2 log n) time. The shortest path is found using Djikstra's
algorithm.
