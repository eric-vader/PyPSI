from Crypto.PublicKey import RSA
from psi.protocol import rsa
from psi.protocol.rsa import utils


class Server:
    """Server for doing RSA-PSI protocol"""

    def __init__(self, private_key=None, key_size=2048, e=0x10001):
        """
        Args:
            private_key: RSA private-key, a key will be generate using
                e and key_size if it's not provided.
            key_size: size in bits of the key.
            e: RSA public exponent.
        """

        if private_key is None:
            self.public_key, self.private_key = rsa.keygen(key_size, e)
        else:
            self.public_key, self.private_key = rsa.from_private(
                self.private_key)

    @property
    def keys(self):
        return self.public_key, self.private_key

    def sign(self, x):
        """Sign a single element using the RSA private-key.

        Args:
            x: integer in the range [0, n), where n is the RSA modulus.

        Returns:
            The signature of x.
        """
        assert 0 <= x < self.private_key.n, "x should be in range [0, {})".format(
            self.private_key.n)

        return utils.sign(self.private_key, x)

    def sign_set(self, X):
        """Sign a set of elements using the RSA private-key.

        Args:
            X: list of integers in the range [0, n), where n is the RSA modulus.

        Returns:
            A list of integers representing the signatures of the set X.
        """
        signatures = []
        for x in X:
            s = self.sign(x)
            signatures.append(s)

        return signatures
