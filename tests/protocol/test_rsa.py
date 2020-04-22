from psi.protocol import rsa
from psi.datastructure import bloom_filter
import pytest


@pytest.mark.parametrize(
    "client_set, server_set",
    [
        (list(range(0, 2**10, 5)), list(range(0, 2**10))),
        (list(range(0, 2**10, 5)), list(range(0, 2**11))),
    ]
)
def test_rsa_psi(client_set, server_set):
    intr = run_protocol(client_set, server_set)
    client_set = set(client_set)
    expected_intr = client_set.intersection(server_set)

    # We don't check how many false positive there is
    for e in expected_intr:
        assert e in intr


def run_protocol(client_set, server_set):
    # BASE
    server = rsa.Server()
    public_key = server.public_key
    client = rsa.Client(public_key)
    random_factors = client.random_factors(len(client_set))
    # SETUP
    signed_server_set = server.sign_set(server_set)
    # Can also do this
    # signed_server_set = [server.sign(x) for x in server_set]
    # encode server set to bytes before adding them to bf
    signed_server_set = [str(sss).encode() for sss in signed_server_set]
    bf = bloom_filter.build_from(signed_server_set)
    # ONLINE
    A = client.blind_set(client_set, random_factors)
    # Can also do this
    # A = [client.blind(x, rf) for x, rf in zip(client_set, random_factors)]
    B = server.sign_set(A)
    # Can also do this
    # B = [server.sign(x) for x in A]
    intr = client.intersect(client_set, B, random_factors, bf)

    return intr
