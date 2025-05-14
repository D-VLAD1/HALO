import random
import ECC.utils as utils
from sympy.ntheory import sqrt_mod
from hashlib import sha256
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import unpad


class Curve:
    """
    The curve class
    """
    def __init__(self, a, b, mod):
        self.a = a
        self.b = b
        self.mod = mod


class Point:
    """
    The Point class
    """
    def __init__(self, x, y, curve):
        self.x = x
        self.y = y
        self.curve = curve

    def __add__(self, other):
        """
        Implements points' addition

        :param other: Point
        :return: Point
        """
        if not isinstance(other, Point):
            raise ValueError('Not a Point')

        mod = self.curve.mod

        ## magic formula to determine the k coefficient
        if self.x == other.x:
            if self.y == 0:
                return None
            k = ((3 * pow(self.x, 2) + self.curve.a) * pow(2 * self.y, -1, mod)) % mod

        else:
            k = ((other.y - self.y) * pow(other.x - self.x, -1, mod)) % mod


        ## magic formular to determine a new point
        x3 = (k ** 2 - self.x - other.x) % mod
        y3 = (k * (self.x - x3) - self.y) % mod

        return Point(x3, y3, self.curve)

    def __mul__(self, k):
        """
        Implements point multiple addition

        :param k: int, how many times to add
        :return: Point
        """
        if not isinstance(k, int):
            raise ValueError('Not am integer')

        result, temp = None, self

        for bit in map(int, bin(k)[:1:-1]):
            if bit == 1: ## iterating through bits, if curr bit is 1 add temp
                if result is None:
                    result = temp
                else:
                    result = result + temp
            temp = temp + temp ## else: double the temp variable

        return result

    @classmethod
    def get_valid_point(cls, curve):
        """
        Generate point where x and y are integers

        :param curve: Curve
        :return: Point
        """
        x, y = None, None
        while y is None:
            x = random.randint(1, curve.mod - 1)
            rhs = (x ** 3 + curve.a * x + curve.b) % curve.mod ## the main curve formula
            y = sqrt_mod(rhs, curve.mod) ## soling x^2 = a (mod curve.mod)

        return cls(x, y, curve)


class ECC:
    """
    The ECC class
    """
    @staticmethod
    def create_keys():
        """
        Generates keys

        :return: tuple[str, str], private and public keys
        """
        curve = Curve(utils.get_prime(), utils.get_prime(), utils.get_prime())

        G = Point.get_valid_point(curve) ## defining an initial point
        p = utils.get_prime() ## defining a huge randon number(ECC private key)

        P = G * p ## computing ECC public key

        r = utils.get_prime()
        R = G * r ## milestone point to get private key for AES algorithm
        S = P * r ## milestone point to get public key for AES algorithm

        S_dec = R * p ## computing point for getting private key

        public_key = sha256(S.x.to_bytes(32)).digest()
        private_key = sha256(S_dec.x.to_bytes(32)).digest()

        return private_key, public_key

    @staticmethod
    def encrypt(key, message: bytes):
        """
        Encrypts the message with a key

        :param key: str, key to encrypt
        :param message: bytes, message to encrypt
        :return: tuple[str, int], encrypted message and IV
        """
        iv = get_random_bytes(16)
        cipher = AES.new(key, AES.MODE_CBC, iv)
        encrypted = cipher.encrypt(utils.transform_msg(message))
        return encrypted, iv

    @staticmethod
    def decrypt(key, encrypted, iv):
        """
        Decrypts the message with a key

        :param key: str, key to encrypt
        :param encrypted: str, message to decrypt
        :param iv: int, IV coefficient
        :return: str
        """

        cipher = AES.new(key, AES.MODE_CBC, iv)
        decrypted = cipher.decrypt(encrypted)
        unpadded = unpad(decrypted, AES.block_size) ## normalize the output bytes
        return unpadded.decode()


if __name__ == '__main__':
    ecc = ECC()
    private_key, public_key = ecc.create_keys()
    encrypted, iv = ecc.encrypt(public_key, b'Hello')
    print(ecc.decrypt(private_key, encrypted, iv))
