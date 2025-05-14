"""Crypto utility functions for RSA encryption."""
import random


def miller_rabin(n, k=100):
    """
    Function to check if a number is prime using Miller-Rabin primality test.

    n: int - The number to check for primality.
    k: int - The number of iterations for accuracy.
    Returns True if n is probably prime, False if n is composite.
    """
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0:
        return False

    r, d = 0, n - 1
    while d % 2 == 0:
        d //= 2
        r += 1

    for _ in range(k):
        a = random.randint(2, n - 2)
        x = pow(a, d, n)

        if x == 1 or x == n - 1:
            continue

        for _ in range(r - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False

    return True


def get_prime():
    """
    Function to generate a large prime number for RSA encryption.

    Returns a prime number that is ~100 digits long.
    """
    num = random.randint(10 ** 50, 10 ** 51)
    while True:
        if miller_rabin(num):
            return num

        num += 1


def transform_msg(msg: bytes):
    """
    Transforming messages for encoding

    :param msg: bytes
    :return: bytes
    """
    pad_len = 16 - (len(msg) % 16)
    return msg + bytes([pad_len] * pad_len)
