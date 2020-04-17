from secrets import randbelow
from psi.protocol.rsa import utils


class Client:
    """Client for doing RSA-PSI protocol"""

    def __init__(self, public_key):
        """
        Args:
            rsa_public_key: RSA public-key.
        """
        self.public_key = public_key

    def random_factors(self, n_elements):
        """Generate n_elements random factors, then inverse and encrypt them.

        Args:
            n_elements: number of random factors to generate.

        Returns:
            A list of tuples, each tuple is composed of the inverse and 
            encryption of a random factor.
        """
        random_factors = []
        for _ in range(n_elements):
            r = randbelow(self.public_key.n)
            r_inv = utils.inverse(self.public_key, r)
            r_encrypted = utils.encrypt(self.public_key, r)
            random_factors.append((r_inv, r_encrypted))

        return random_factors

    def blind(self, x, rf):
        """Blind an element using the encryption of a random factor.

        Args:
            x: integer in the range [0, n), where n is the RSA modulus.
            rf: tuple composed of the inverse and encryption of a random
                factor.

        Returns:
            The blinded version of the element integer x.
        """
        assert 0 <= x < self.public_key.n, "x should be in range [0, {})".format(
            self.public_key.n)
        rf_encrypted = rf[1]
        return utils.mulmod(x, rf_encrypted, self.public_key.n)

    def blind_set(self, X, random_factors):
        """Blind a set of elements using the encryption of random factors.

        Args:
            X: list of integers in the range [0, n), where n is the RSA modulus.
            random_factor: list of tuples, each tuple is composed of the inverse and 
                encryption of a random factor.

        Returns:
            A list of integers representing the blinded set X.
        """
        assert len(X) <= len(
            random_factors), "There is more element than random factors"

        blinded_set = []
        for x, rf in zip(X, random_factors):
            b = self.blind(x, rf)
            blinded_set.append(b)

        return blinded_set

    def intersect(self, Y, B, random_factors, bf):
        """Compute the intersection of the client and server set.

        Args:
            Y: client set.
            B: signatures of the blinded client set.
            random_factors: list of tuples, each tuple is composed of the inverse and 
                encryption of a random factor.
            bf: bloom filter filled with the signed server set.

        Returns:
            A list of integer representing the intersection of the client and 
            server set.
        """
        result = []
        for y, b, rf in zip(Y, B, random_factors):
            rf_inv = rf[0]
            to_check = utils.mulmod(b, rf_inv, self.public_key.n)
            if to_check in bf:
                result.append(y)
        return result
