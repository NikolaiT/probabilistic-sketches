import random

class Stream:
    """
    Produces random elements and simulates a stream.
    """
    def __init__(self, n, rand_range):
        """
        n : Number of random elements to produce.
        range : Random elements are in this range.
        """
        self.n = n
        self.range = rand_range

    def produce(self):
        for i in range(self.n):
            yield random.randrange(*self.range)

    def __iter__(self):
        return self.produce()
