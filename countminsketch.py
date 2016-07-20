#!/usr/bin/env python3

import numpy as np
from stream import Stream

class CountMinSketch:
    """
    Implements the Count-Min-Sketch probabilistic data
    structure that allows to count frequencies of elements
    in a large data stream.
    """

    def __init__(self, d, w):
        """
        d: Number of different hash functions. Height of matrix.
        w: cardinality of result domain of hash functions.
        """
        self.d = d
        self.w = w
        self.estimators = np.ndarray((self.d, self.w), dtype=np.int)
        self.estimators.fill(0)

        # coefficients for linear hash functions
        self.a = np.zeros(d, dtype=np.int)
        self.b = np.zeros(d, dtype=np.int)
        self.p = 2**31 - 1 # large prime number

        self.init_hash_functions()

    def init_hash_functions(self):
        for i in range(self.d):
            self.a[i] = np.random.randint(1, self.p)
            self.b[i] = np.random.randint(1, self.p)

    def hash(self, value, i):
        return ((self.a[i] * value + self.b[i]) % self.p) % self.w

    def add_value(self, value):
        for i in range(self.d):
            self.estimators[i][self.hash(value, i)] += 1

    def estimate_frequency(self, value):
        return min([self.estimators[i][self.hash(value, i)] for i in range(self.d)])

def main():
    exact_counter = dict()
    cms = CountMinSketch(15, 2**10)
    s = Stream(1000000, (0, 1000))
    for a in s:
        if a not in exact_counter:
            exact_counter[a] = 1
        else:
            exact_counter[a] += 1
        cms.add_value(a)

    for key in exact_counter:
        print('Value {}, estimated freq = {}, real freq = {}'.format(key, cms.estimate_frequency(key), exact_counter[key]))

main()
