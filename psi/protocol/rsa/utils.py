import gmpy2


def inverse(key, x):
    n = key.n
    return gmpy2.invert(x, n)


def encrypt(key, pt):
    e, n = key.e, key.n
    return gmpy2.powmod(pt, e, n)


def decrypt(key, ct):
    d, n = key.d, key.n
    return gmpy2.powmod(ct, d, n)


def sign(key, pt):
    return decrypt(key, pt)


def mulmod(x, rf_encrypted, n):
    return (x * rf_encrypted) % n
