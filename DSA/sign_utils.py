"""Module to generate DSA keys and parameters."""
import random
import hashlib
from DSA.utils import get_prime, get_strong_prime

def generate_params():
    """
    Function to generate DSA parameters.
    Returns a tuple of (p, q, g) where:
    p is a large prime number,
    q is a prime divisor of p-1,
    g is a generator of the subgroup of order q.
    """
    q =  get_prime(160) # gettin a 160 bits prime number
    p =  get_strong_prime(1024, q) # now gettin a 1024 bits prime number that is divisible by q
    while True:
        h = random.randrange(1, p-1) # random number between 1 and p-1
        g = pow(h, (p-1)//q, p) # g is a generator of the subgroup of order q
                                # and so g^q mod p = 1 :)
        if g > 1:
            break
    return p, q, g


def generate_keys(p, q, g):
    """
    Function to generate DSA keys.
    Returns a tuple of (x, y) where:
    x is the private key,
    y is the public key.
    """
    x = random.randrange(1, q) # randomly chosen private key
    y = pow(g, x, p) # public key is g^x mod p
    return x, y

def sign_message(message, p, q, g, x):
    """
    Function to sign a message using DSA.
    Returns a tuple of (r, s) where:
    r is the first part of the signature,
    s is the second part of the signature.
    """
    hash_obj = hashlib.sha1(message.encode())
    hash_value = int(hash_obj.hexdigest(), 16)

    while True:
        k = random.randrange(1, q) # randomly chosen k
        r = pow(g, k, p) % q # r is g^k mod p, first part of the signature
        if r == 0:
            continue

        k_inv = pow(k, -1, q) # inverted k, obviously
        s = (k_inv * (hash_value + x * r)) % q  # s is k_inv * (hash_value + x * r) mod q,
                                                # second part of the signature
        if s != 0:
            break

    return (r, s)
