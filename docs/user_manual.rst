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
  This document explains how to use Pyvisgraph to build the visibility graph
  for a given list of simple obstacle polygons, then find the shortest path
  between two points.

.. _intro:

Introduction
=============

Pyvisgraph is a MIT-licensed Python package for building visibility graphs from
a list of simple obstacle polygons. The visibility graph algorithm (D.T. Lee)
runs in :math:`O(n^2 \log n)` time. The shortest path is found using Djikstra's
algorithm.

Installing Pyvisgraph
=====================

.. code-block:: console

  $ pip install pyvisgraph

Pyvisgraph supports Python 2 and 3. Pyvisgraph does not require any other packages.

Usage Example
=============

Here is an example of building a visibility graph given a list of simple polygons:

.. code-block:: pycon

  >>> from pyvisgraph.graph import Point
  >>> from pyvisgraph.vis_graph import VisGraph
  >>> polys = [[Point(0.0,1.0), Point(3.0,1.0), Point(1.5,4.0)],
  >>>          [Point(4.0,4.0), Point(7.0,4.0), Point(5.5,8.0)]]
  >>> graph = VisGraph()
  >>> graph.build(polys)
  >>> shortest = graph.shortest_path(Point(1.5,0.0), Point(4.0, 6.0))
  >>> print shortest
  [Point(1.50, 0.00), Point(3.00, 1.00), Point(4.00, 6.00)]

Once the visibility graph is built, it can be saved and subsequently loaded. This is 
useful for large graphs where build time is long. `pickle`_ is used for saving and loading.

.. code-block:: pycon

  >>> graph.save('graph.pk1')
  >>> graph2 = VisGraph()
  >>> graph2.load('graph.pk1')

Data Model
==========

Text

Graph classes
=============

The `pyvisgraph.graph` module contains the `Point`, `Edge` and `Graph` classes.

Points
------
.. class:: Point(x, y)
  
  The `Point` constructor takes positional coordinate values `x` and `y`.

.. code-block:: pycon

  >>> from pyvisgraph.graph import Point
  >>> point = Point(0.0, 0.0)

Coordinate values are accessed via `x` and `y` properties.

.. code-block:: pycon
  
  >>> point.x
  0.0
  >>> point.y
  0.0

Points can be compared for equality - equality will be based on each `Point`'s
coordinates, not the Python object.

.. code-block:: pycon

  >>> point1 = Point(0.0, 0.0)
  >>> point2 = Point(0.0, 1.0)
  >>> point3 = Point(0.0, 1.0)
  >>> point1 == point2
  False
  >>> point2 == point3
  True

Edges
-----
.. class:: Edge(point1, point2)

  The `Edge` constructor takes two `Point`, which are the end points of the `Edge`.

.. code-block:: pycon

  >>> from pyvisgraph.graph import Edge, Point
  >>> edge = Edge(Point(0.0, 0.0), Point(1.0, 1.0))

End points are accessed via `p1` and `p2` properties.

.. code-block:: pycon

  >>> edge.p1
  Point(0.00, 0.00)
  >>> edge.p2
  Point(1.00, 1.00)

Edges can be compared for equality - equality will be based on each `Edge`'s set
of end points (order does not matter).

  >>> edge1 = Edge(Point(0.0, 0.0), Point(0.0, 0.0))
  >>> edge2 = Edge(Point(0.0, 0.0), Point(1.0, 1.0))
  >>> edge3 = Edge(Point(1.0, 1.0), Point(0.0, 0.0))
  >>> edge1 == edge2
  False
  >>> edge2 == edge3
  True

Graphs
------
.. class:: Graph(polygons)

  A `Graph` is represented by a dictionary where the keys are `Points` in the graph
  and the dictionary values are sets containing `Edges` incident on each `Point`.

  The constructor takes a list of polygons, where each polygon is represented by a 
  list of `Points`.
  
  .. note:: 
    If there is only one polygon, the input to the constructor must still be a list 
    in a list, i.e. `[[Point(0.0, 0.0), Point(2.0, 0.0), Point(2.0, 1.0)]]`.

    The `Points` representing a polygons should be in-order (clockwise or counter 
    clockwise) in order for Pyvisgraph to function properly.

  The property `edges` contains all `Edges` in the graph.
  Property `polygons` dictionary: key is a integer polygon ID and values are the
  edges that make up the polygon. Note only polygons with 3 or more Points
  will be classified as a polygon. Non-polygons like just one Point will be
  given a polygon ID of -1 and not maintained in the dict.

.. _troubleshooting:

Troubleshooting
===============

This section outlines some common problems a user may run into and possible
solutions. If you can't find a solution to your problem, please send me an email
or open an issue on `GitHub`_.

.. _trouble-float-rep-error:

Floating point representation errors
------------------------------------

Because of the way floating point numbers are represented in computer hardware,
you may run into problems under certain circumstances. If you get an error like
`ValueError: math domain error` or your visibility graph looks wrong, chances
are they are due to floating point representation errors.

The `Python docs`_ explain representation errors and issues better. You can use
the `Decimal` class to see what the actual representation of a float is.
For example:

.. code-block:: pycon

  >>> from decimal import Decimal
  >>> Decimal(1.1)
  Decimal('1.100000000000000088817841970012523233890533447265625')

The representation error seems to consistently happen at the 18th significant
digit. When you start adding or multiplying numbers together, the errors
starting from the 18th significant digit start adding up:

.. code-block:: pycon

  >>> Decimal(1.1*1.1)
  Decimal('1.2100000000000001865174681370262987911701202392578125')

Now the error is occurring from the 17th significant digit.

The solution to this issue is to truncate the trailing digits. The correct
number of digits to keep after the decimal point depends on your coordinate
system. Using a normal geographical longitude latitude coordinate system,  you
have three digits before the decimal point, which gives you less precision
after the decimal point. Truncating to 8 digits after the decimal point is in
this case more than enough to avoid any floating point representation errors.

This truncating solution is used in several key Pyvisgraph functions
(`angle2()` and `ccw()`). Currently, you can only set it by changing the
global `COLIN_TOLERANCE` in `visible_vertices.py`. In the future this will be
changeable through the API.

Crossing the antimeridian
-------------------------

If your use case is finding shortest paths on a geographical map, you may
run into a problem if the shortest path crosses the `antimeridian`_. Pyvisgraph
will not find that path. Please see `issue 27`_ on GitHub for discussions on
possible solutions.


.. _Python docs: https://docs.python.org/2/tutorial/floatingpoint.html
.. _GitHub: https://github.com/TaipanRex/pyvisgraph
.. _antimeridian: https://en.wikipedia.org/wiki/180th_meridian
.. _issue 27: https://github.com/TaipanRex/pyvisgraph/issues/27
.. _pickle: https://docs.python.org/2/library/pickle.html