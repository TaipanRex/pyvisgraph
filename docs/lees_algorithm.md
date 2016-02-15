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

![Figure 1](lee_figure1.png)
