#!/usr/bin/env python3

import random
import math
from stream import Stream

class CardinalityCounter:

    def __init__(self, m):
        self.m = m
        # simulate the bitmask by using
        # a string with length m
        self.bitmask = self.m * [0]

    def hash(self, value):
        evenly_distributed = value * 19441 + 73877
        return evenly_distributed % self.m

    def add(self, value):
        hvalue = self.hash(value)
        self.bitmask[hvalue] = 1

    def get_cardinality(self):
        """
        Estimates the cardinality.
        """
        weight = sum(self.bitmask)
        if self.m == weight:
            raise Exception('Cannot estimate cardinality, weight equals m')
        return -self.m * math.log((self.m - weight) / self.m)


def test_hash_function():
    c = CardinalityCounter(50)
    s = Stream(200, (1, 1000))
    for a in s.produce():
        c.add(a)
        print(c.bitmask)

def main():
    n = 100000
    randrange = (1, 1000000)
    m = 25000
    s = Stream(n, randrange)
    c = CardinalityCounter(m)
    real_cardinality = set()

    for a in s.produce():
        c.add(a)
        real_cardinality.add(a)

    real, est = len(real_cardinality), c.get_cardinality()
    error = abs(1 - (float(real)/est)) * 100
    print('Load factor is ', n/m)
    print('Estimated cardinality is ', est)
    print('Real cardinality is ', real)
    print('Error is: {0:.2f}%'.format(error))

if __name__ == '__main__':
    main()
