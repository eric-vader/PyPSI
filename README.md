# PyPSI
![Tests](https://github.com/OpenMined/PyPSI/workflows/Tests/badge.svg)

A Python library for private set intersection. PyPSI is interoperable with other OpenMined PSI libraries such as [psi.js](https://github.com/OpenMined/psi.js) [SwiftPSI](https://github.com/OpenMined/SwiftPSI) [KotlinPSI](https://github.com/OpenMined/KotlinPSI) and you should be able to implement your PSI client and server in different languages depending on your need.

## PSI Protocols

Our PSI libraries aim at providing different PSI protocols. Below is a list of supported protocols:

- RSA Blind Signature-based PSI (RSA-PSI) as described in this [paper](https://encrypto.de/papers/KLSAP17.pdf), implemented under `psi.protocol.rsa`

## Example

Below is a code snippet showing how to do PSI using the RSA-PSI protocol, this is done locally, however, this should involve communication between a client and a server in a real application scenario.

```python
from psi.protocol import rsa
from psi.datastructure import bloom_filter

def run_protocol(client_set, server_set):
    ## BASE
    server = rsa.Server()
    public_key = server.public_key
    client = rsa.Client(public_key)
    random_factors = client.random_factors(len(client_set))
    ## SETUP
    signed_server_set = server.sign_set(server_set)
    # must encode to bytes
    signed_server_set = [str(sss).encode() for sss in signed_server_set]
    bf = bloom_filter.build_from(signed_server_set)
    ## ONLINE
    A = client.blind_set(client_set, random_factors)
    B = server.sign_set(A)
    unblinded_client_set = client.unblind_set(B, random_factors)
    # must encode to bytes
    unblinded_client_set = [str(ucs).encode() for ucs in unblinded_client_set]
    
    intr = client.intersect(client_set, unblinded_client_set, bf)
    return intr


run_protocol([0, 1, 2, 3, 4, 5], [0, 3, 4, 7, 9, 73])

```

## License

[Apache License 2.0](https://github.com/OpenMined/PyPSI/blob/master/LICENSE)
