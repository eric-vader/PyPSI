import pytest
from psi.datastructure import bloom_filter


@pytest.mark.parametrize(
    "elements",
    [
        [60, 66, 73, 81, 90, 100],
        [-6, 0, 1, 2, -1],
        list(range(1024)),
    ]
)
def test_bf(elements):
    bf = bloom_filter.build_from(elements)
    assert len(bf) == len(elements)
    for e in elements:
        assert e in bf


def test_encode_int():
    x = 8978
    neg_x = -x
    x_encoded = bloom_filter.BloomFilter.encode(x)
    assert x_encoded == b'#\x12'

    neg_x_encoded = bloom_filter.BloomFilter.encode(neg_x)
    # E is the hex decoding of ord('-')
    assert b'E' + x_encoded == neg_x_encoded
