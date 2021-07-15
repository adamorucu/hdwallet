"""
Public key cryptography
Resources:
    - https://github.com/karpathy/cryptos/blob/main/cryptos/keys.py
    - https://www.oreilly.com/library/view/programming-bitcoin/9781492031482/ch04.html
"""

from dataclasses import dataclass

from hdwallet.ecdsa import Point
from hdwallet.currencies import BTC
from hdwallet.utils import int2byte

# @dataclass
# class PublicKey:
#     key: int

# @dataclass
# class PrivateKey:
#     key: int

#     def get_public_key(self) -> PublicKey:
#         return PublicKey(self.key * BTC['EC']['G'])


class PublicKey(Point):
    @classmethod
    def from_point(cls, pnt: Point):
        "pk from point"
        return cls(pnt.curve, pnt.x, pnt.y)

    @classmethod
    def from_sk(cls, sk: int):
        """from secret key generate public key"""
        pk = sk * BTC.G
        return cls.from_point(pk)

    def encode(self, compressed: bool=True) -> bytes:
        """returns SEC format"""
        if compressed:
            if self.y % 2 == 0:
                return b'\x02' + int2byte(self.x, 32)
            else:
                return b'\x03' + int2byte(self.x, 32)
        else:
            return b'\x04' + int2byte(self.x, 32) + int2byte(self.y, 32)

    @classmethod
    def decode(cls, sec: bytes):
        """returns publickey (point) from SEC format"""
        pass
