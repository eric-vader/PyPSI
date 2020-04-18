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
        # compute filter size and num filter for a given fp_prob and capacity
        self._num_filters = math.ceil(math.log2(1 / fp_prob))
        self._filter_size = math.ceil(
            (capacity * abs(math.log(fp_prob))) /
            (self._num_filters * math.log(2) ** 2)
        )
        # set bitarray
        size = self._num_filters * self._filter_size
        self._bitarray = bitarray(size)
        self._bitarray.setall(0)

    def hashes(self, x):
        """Compute the hash of x for the different filters.

        Args:
            x: element to hash.

        Returns:
            list of hashes, one hash for each filter.
        """
        x = BloomFilter.encode(x)
        hashes = []
        for i in range(self._num_filters):
            hash_func = hashlib.new('md5')
            salt = str(i).zfill(hash_func.block_size).encode()
            hash_func.update(salt)
            hash_func.update(x)
            h = int(hash_func.hexdigest(), 16) % self._filter_size
            hashes.append(h)

        return hashes

    def add(self, x):
        """Add an element to the bloom filter.

        Args:
            x: element to add.
        """
        if self.count >= self.max_capacity:
            raise RuntimeWarning("Bloom filter is at maximum capacity")

        filter_offset = 0
        hashes = self.hashes(x)
        for h in hashes:
            self._bitarray[filter_offset + h] = 1
            # next filter
            filter_offset += self._filter_size

        self.count += 1

    def check(self, x):
        """Check either an element is in the bloom filter.

        Args:
            x: element to check

        Returns:
            boolean either x is in the bloom filter (True) or not (False).
        """
        filter_offset = 0
        hashes = self.hashes(x)
        for h in hashes:
            if not self._bitarray[filter_offset + h]:
                return False
            # next filter
            filter_offset += self._filter_size

        return True

    @classmethod
    def encode(cls, x):
        """Encode an element x to be hashed.

        Args:
            x: element to be encoded.

        Returns:
            bytes object.
        """
        if isinstance(x, int):
            neg = False
            if x < 0:
                neg = True
                x = abs(x)

            h = hex(x)[2:]
            if len(h) % 2:
                h = h.zfill(len(h) + 1)
            if neg:
                h = str(ord('-')) + h

            return unhexlify(h)

        elif isinstance(x, type(gmpy2.mpz())):
            return BloomFilter.encode(x.__int__())

        else:
            raise NotImplementedError(
                "encode doesn't support {} objects".format(type(x)))

    def __contains__(self, x):
        return self.check(x)

    def __len__(self):
        return self.count


def build_from(X):
    """Create a bloom_filter and add the set X.

    Args:
        X: a list of elements.

    Returns:
        BloomFilter filled with elements of the set X.
    """
    bf = BloomFilter(len(X))
    for x in X:
        bf.add(x)

    return bf
