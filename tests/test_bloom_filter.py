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


def test_serialization():
    # same test as cpp
    capacity = 100
    fp_prob = 0.01
    bf = bloom_filter.BloomFilter(capacity, fp_prob)
    expected_num_hash_functions = 7
    expected_bits = ("VN3/BXfUjEDvJLcxCTepUCTXGQwlTax0xHiMohCNb45uShFsznK099RH"
                     "0CFVIMn91Bdc7jLkXHXrXp1NimmZSDrYSj5sd/500nroNOdXbtd53u8c"
                     "ejPMGxbx7kR1E1zyO19mSkYLXq4xf7au5dFN0qhxqfLnjaCE")

    for i in range(capacity):
        x = "Element {}".format(i).encode()
        bf.add(x)

    serialized = bf.export()
    assert serialized["num_hash_functions"] == expected_num_hash_functions
    assert serialized["bits"] == expected_bits
