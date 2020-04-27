import math
import hashlib
import gmpy2
import base64
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
        self._size = math.ceil(-capacity * math.log2(fp_prob) / math.log(2))
        self._size = math.ceil(self._size / 8) * 8
        self._num_hash_functions = math.ceil(-math.log2(fp_prob))
        # set bitarray
        self._bitarray = bitarray(self._size, endian='little')
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

    def export(self):
        """Export the bloom filter to a dictionarry, which can be then serialized
        with json.
        """
        bitarray_b64 = base64.encodebytes(self._bitarray.tobytes())
        bitarray_b64 = bitarray_b64.replace(b'\n', b'').decode()
        num_hash_functions = self._num_hash_functions
        bf_dict = {
            "num_hash_functions": num_hash_functions,
            "bits": bitarray_b64,
        }
        return bf_dict

    @staticmethod
    def from_dict(bf_dict):
        num_hash_functions = bf_dict["num_hash_functions"]
        bits_as_bytes = base64.decodebytes(bf_dict["bits"])

        bf = BloomFilter(capacity=1)  # capacity doesn't matter since we overwrite
        bf._num_hash_functions = num_hash_functions
        bf._bitarray = bitarray()
        bf._bitarray.frombytes(bits_as_bytes)
        bf._size = len(bits_as_bytes) * 8
        # set to random values for the moment
        bf.max_capacity = bf._size
        bf.count = 0

        return bf

    def __contains__(self, x):
        return self.check(x)

    def __len__(self):
        return self.count


def build_from(X, capacity=None, fp_prob=None):
    """Create a bloom_filter and add the set X.

    Args:
        X: a list of elements.
        capacity: maximum capacity of the bloom filter, set to len(X) if not
            specified.
        fp_prob: probability of false positives.

    Returns:
        BloomFilter filled with elements of the set X.
    """
    if capacity is None:
        capacity = len(X)

    if fp_prob is None:
        bf = BloomFilter(capacity)
    else:
        bf = BloomFilter(capacity, fp_prob)

    for x in X:
        bf.add(x)

    return bf
