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
    # encode into bytes
    elements = list(map(lambda x: str(x).encode(), elements))
    bf = bloom_filter.build_from(elements)
    assert len(bf) == len(elements)
    for e in elements:
        assert e in bf
