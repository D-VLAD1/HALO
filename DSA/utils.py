"""Module containing utility functions for various algorithms."""
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

def check_prime(num):
    """Function to check if a number is prime."""
    if num < 2:
        return False # 0, 1, and negative numbers are not prime


    low_primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47,\
                53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, \
                113, 127, 131, 137, 139, 149, 151, 157, 163, 167, 173, 179, \
                181, 191, 193, 197, 199, 211, 223, 227, 229, 233, 239, 241, \
                251, 257, 263, 269, 271, 277, 281, 283, 293, 307, 311, 313, \
                317, 331, 337, 347, 349, 353, 359, 367, 373, 379, 383, 389, \
                397, 401, 409, 419, 421, 431, 433, 439, 443, 449, 457, 461, \
                463, 467, 479, 487, 491, 499, 503, 509, 521, 523, 541, 547, \
                557, 563, 569, 571, 577, 587, 593, 599, 601, 607, 613, 617, \
                619, 631, 641, 643, 647, 653, 659, 661, 673, 677, 683, 691, \
                701, 709, 719, 727, 733, 739, 743, 751, 757, 761, 769, 773, \
                787, 797, 809, 811, 821, 823, 827, 829, 839, 853, 857, 859, \
                863, 877, 881, 883, 887, 907, 911, 919, 929, 937, 941, 947, \
                953, 967, 971, 977, 983, 991, 997]

    if num in low_primes:
        return True

    for p in low_primes:
        if num % p == 0:
            return False

    return miller_rabin(num)

def get_prime(bitsize):
    """
    Function to generate a large prime number.
    
    Returns a prime number according to bitsize.
    """

    while True:
        num = random.randrange(2**(bitsize-1), 2**(bitsize))
        if check_prime(num):
            return num

def get_strong_prime(bitsize, q):
    """
    Function to generate a strong prime number.

    A strong prime is a prime number that is not only large but also satisfies 
    certain mathematical properties.

    q is a prime factor of p-1, where p is the strong prime.
    """
    while True:
        k = random.getrandbits(bitsize - q.bit_length())
        p = k * q + 1
        if p.bit_length() != bitsize:
            continue
        if check_prime(p):
            return p
