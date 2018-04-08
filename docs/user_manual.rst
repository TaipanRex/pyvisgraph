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
runs in O(n^2 log n) time. The shortest path is found using Djikstra's
algorithm.

Installing Pyvisgraph
=====================

Text

Usage Example
=============

Text

Data Model
==========

Text

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
