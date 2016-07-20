#!/usr/bin/env python3
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt

from stream import Stream
from cardinality_cnt import CardinalityCounter

c = CardinalityCounter(100)
s = Stream(1000, (1, 100000))
X = [c.hash(a) for a in s.produce()]

# the histogram of the data
n, bins, patches = plt.hist(X, c.m, facecolor='green', alpha=0.75)

plt.xlabel('Hash Function Output Domain')
plt.ylabel('Frequency')
plt.grid(True)

plt.show()
