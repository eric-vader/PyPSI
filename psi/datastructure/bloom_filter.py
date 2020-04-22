import math
import hashlib
import gmpy2
from binascii import unhexlify
from bitarray import bitarray


class BloomFilter:
    """
    Bloom filter implementation.
    Section 3: http://gsd.di.uminho.pt/members/cbm/ps/dbloom.pdf
    """

    def __init__(self, capacity, fp_prob=0.001):
        """
        Args:
            capacity: maximum number of elements the bloom filter should hold to
                satisfy the probability of false positives.
            fp_prob: probability of false positives. Inserting more than the
                specified size will increase this probability.
        """
        if capacity <= 0:
            raise ValueError("capacity must be an integer > 0")
        if not 0 < fp_prob < 1:
            raise ValueError("fp_prob must be in the range (0,1)")

        self.max_capacity = capacity
        self.count = 0
        self._size = math.ceil(-1.44 * capacity * math.log2(fp_prob))
        self._num_hash_functions = math.ceil(-math.log2(fp_prob))
        # set bitarray
        self._bitarray = bitarray(self._size)
        self._bitarray.setall(0)

    def hashes(self, x):
        """Compute the hash of x for the different filters.

        Args:
            x: element to hash (bytes).

        Returns:
            list of hashes, one hash for each filter.
        """
        assert isinstance(x, bytes), "BloomFilter accepts bytes objects"

        hash_func = hashlib.new('sha256')
        hash_func.update(b'1' + x)
        h1 = int(hash_func.hexdigest(), 16) % self._size
        hash_func = hashlib.new('sha256')
        hash_func.update(b'2' + x)
        h2 = int(hash_func.hexdigest(), 16) % self._size

        hashes = []
        for i in range(self._num_hash_functions):
            hashes.append((h1 + i * h2) % self._size)

        return hashes

    def add(self, x):
        """Add an element to the bloom filter.

        Args:
            x: element to add (bytes).
        """
        if self.count >= self.max_capacity:
            raise RuntimeWarning("Bloom filter is at maximum capacity")

        hashes = self.hashes(x)
        for h in hashes:
            self._bitarray[h] = 1

        self.count += 1

    def check(self, x):
        """Check whether an element is in the bloom filter.

        Args:
            x: element to check (bytes).

        Returns:
            boolean whether x is possibly in the bloom filter (True) or not (False).
        """
        hashes = self.hashes(x)
        for h in hashes:
            if not self._bitarray[h]:
                return False

        return True

    def __contains__(self, x):
        return self.check(x)

    def __len__(self):
        return self.count


def build_from(X, eps=0.01):
    """Create a bloom_filter and add the set X.

    Args:
        X: a list of elements.
        eps: probability of false positive.

    Returns:
        BloomFilter filled with elements of the set X.
    """
    bf = BloomFilter(len(X))
    for x in X:
        bf.add(x)

    return bf
