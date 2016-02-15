#Lee's Algorithm
There seems to be no easy to follow explanation of visibility graph algorithms
on the internet. I have searched far and low and while the sources I did find
are detailed and thorough, they were meant for smarter people than me. I will
here attempt to explain Lee's algorithm, in a way that would make me understand
it when I started researching the implementation.

First I would like to list the key sources I have used in implementing Lee's
algorithm. These have been instrumental in guiding me to a working
implementation:

* Kitzinger, J. (2003). [The visibility graph among polygonal obstacles:
A comparison of algorithms](http://www.cs.unm.edu/~moore/tr/03-05/Kitzingerthesis.pdf)
* Coleman, D. (2012). [Lee's O(n^2 log n) Visibility Graph Algorithm
Implementation and Analysis](http://dav.ee/papers/Visibility_Graph_Algorithm.pdf)
* Berg, M. D. (2008). [Computational geometry: Algorithms and applications.](http://www.amazon.com/Computational-Geometry-Applications-Mark-Berg/dp/3540779736/)
Berlin: Springer.

Lee's algorithm solves the visibility graph in O(n^2 log n) time and was the
first non-trivial solution to the visibility problem. He wrote this algorithm
as part of his 1978 Ph.D. dissertation. Faster solutions were created after
that, the fastest being the Ghosh and Mount approach running in O(e + n log n),
though I leave those for another time.

## Naive solution
Before we start looking at Lee's algorithm, lets quickly understand the naive
solution:

    for each point p in graph G                                             #O(n)
        for each point p2 in graph {G - p}                                  #O(n)
            for each edge e in Graph G                                      #O(e)
                if the arc from p to p2 does not intersect edge e then
                    point p and p2 are mutually visible to each other

For each point in the graph we need to check if every other point is visible
to it. To do that we need to check each pair of points to all the edges, if they
intersect or not. This leaves us with three nested `for` loops, giving us
O(n^3) running time. _I want to also note that you would need to check that none
of the arcs from p to p2 can cross the interior of a polygon. I deal with that
in my Lee's algorithm._

## Lee's scan line
We are still going to need the first two `for` loops as in the naive solution;
where Lee's approach saves us running time is by reducing the number of
edges we need to check for each pair of points. That part of the algorithm runs
in O(log n) time, leaving a total running time of O(n^2 log n).

The key concept to understand in Lee's algorithm is the scan line. This took me
actually implementing a working solution to fully understand. Hopefully I can
explain it in a way that will save you some headaches.

![Figure 1](images/lee_figure1.png)

Let's say we are checking which points are visible from `point s`. To do this
we need to visit each of the points `a` through `f`. The way we are going to visit
the points is in a counter clockwise circle. We are going to use Lee's scan line
for this, which is a half-line. Conceptually the scan line has its origin at
`point s`, pointing to the right (parallel to the x-axis) and moves counter clock
wise until it hits a point to check for visibility. _In reality we don't
actually need to move in this way, we can just order the points according to
their angle to `point s` and the x-axis (more on that later)._  

Together with the scan line we are going to keep a ordered list of edges that
we will need to use when we visit each point. This list will be used to check
for point visibility.

Once the scan line hits a point, the algorithm is going to work some magic on
the edges incident on the point. Take figure 1: the first point the scan line
will hit is `point a`, which has two edges (`edge ab` and `edge ac`). what
it is going to do is check if each edge is on the "counter clock wise" side of
the scan line. I.e., when the scan line continues moving, will it intersect any
of those edges? In the case of `point a`, both edges are on the CCW side and will
be added the edge list I mentioned we are tracking.

Lets continue the scan line to `point b` (figure 2). Now, `edge ab` is
on the clock wise side of the scan line and *it will never be intersected by the
scan line again*. This means we are free to completely ignore that edge for all
unvisited points and we can remove it from the tracking edge list. `edge ac` is
still partially on the CCW side, so it stays in the list.

What the scan line allows us to do is ignore edges that are no longer an issue;
edges that can no longer block visibility of the next points to visit.
When the scan line moves on to point c, d, e and f, it will never have to
consider the edges that it has already passed, like `edge ab`.

## Edge list
