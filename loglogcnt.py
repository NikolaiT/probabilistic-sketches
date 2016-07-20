#!/usr/bin/env python3

import random
import math
import hashlib
import numpy as np
from stream import Stream

np.set_printoptions(threshold=np.inf)

class LogLogCounter:
    def __init__(self, H, k, etype=8, n=100000):
        """
        H: length of hash function in bits
        k: number of bits that determine bucket
        etype: number of bits for each estimator (Not used yet)
        """
        self.H = H
        self.k = k
        self.etype = etype # currently ignored

        self.m = 2**self.k
        self.estimators = np.zeros(self.m, dtype=np.int8)
        self.hash_func_len = int(math.log(self.m, 2) + math.floor(math.log(n/self.m) + 3))

    def hash(self, value):
        """
        hashes the value and returns a 128 bit long bitstring.
        md5 is used, other hash functions might also work.
        """
        m = hashlib.md5()
        m.update(bytes(value))
        h = m.hexdigest()
        return '{0:0128b}'.format(int(h, 16))

    def get_bits(self, value, start, end, number=False):
        """
        Get a number from the bitstring specified by the range
        from start to end.
        """
        s = value[start:end]
        if number:
            return int(s, 2)
        else:
            return s

    def rank(self, value):
        """
        Find the position of the first '1' bit in the hash value.
        100...b has rank 1
        001...b has rank 3
        0000001...b has rank 7
        """
        try:
            return value.index('1') + 1
        except ValueError as e:
            return len(value)

    def add(self, value):
        hashed = self.hash(value)
        bucket = self.get_bits(hashed, 0, self.k, number=True)
        self.estimators[bucket] = max(
            self.estimators[bucket],
            self.rank(self.get_bits(hashed, self.k, self.H))
        )

    def estimate_cardinality(self):
        est_factor = 0.39701
        power = (1.0/self.m) * self.estimators.sum()
        est = est_factor * self.m * 2**power
        return int(est)

def main():
    n = 100000
    randrange = (1, 1000000)
    s = Stream(n, randrange)
    real_card = set()
    loglogc = LogLogCounter(128, 10, 8, n)
    for a in s.produce():
        loglogc.add(a)
        real_card.add(a)

    real, est = len(real_card), loglogc.estimate_cardinality()
    error = abs(1 - (float(real)/est)) * 100
    print('Real cardinality={} and estimated cardinality={}'.format(real, est))
    print('Error is: {0:.2f}%'.format(error))

if __name__ == '__main__':
    main()
