import pybloom_live


class BloomFilter:

    def __init__(self, size=None, eps=0.01):
        """
        Args:
            size: number of elements the bloom filter should hold.
            eps: probability of false positive.
        """
        mode = pybloom_live.ScalableBloomFilter.SMALL_SET_GROWTH
        self.bf = pybloom_live.ScalableBloomFilter(mode=mode)

    def add(self, x):
        """Add an element to the bloom filter.

        Args:
            x: element to add.
        """
        self.bf.add(x)

    def check(self, x):
        """Check either an element is in the bloom filter.

        Args:
            x: element to check

        Returns:
            boolean either x is in the bloom filter (True) or not (False).
        """
        return x in self.bf

    def __contains__(self, x):
        return self.check(x)


def build_from(X, eps=0.01):
    """Create a bloom_filter and add the set X.

    Args:
        X: a list of elements.
        eps: probability of false positive.

    Returns:
        BloomFilter filled with elements of the set X.
    """
    bf = BloomFilter()
    for x in X:
        bf.add(x)

    return bf
