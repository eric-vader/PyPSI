"""Implementation of the RSA-PSI protocol defined in
https://encrypto.de/papers/KLSAP17.pdf
"""

from Crypto.PublicKey import RSA
from psi.protocol.rsa.client import Client
from psi.protocol.rsa.server import Server


def keygen(key_size, e):
    """Construct an RSA public and private key pair.

    Args:
        key_size: size in bits of the key.
        e: RSA public exponent.

    Returns:
        tuple of public and private RSA keys.
    """
    private_key = RSA.generate(key_size, e=e)
    return from_private(private_key)


def from_private(private_key):
    """Construct a public key from the private key.

    Args:
        private_key: RSA private-key.

    Returns:
        tuple of public and private RSA keys.
    """
    public_key = RSA.construct((private_key.n, private_key.e))
    return public_key, private_key


__all__ = ["Client", "Server"]
