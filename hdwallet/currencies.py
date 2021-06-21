"""
Currency specific parameters and utilities
"""
from dataclasses import dataclass

from hdwallet.ecdsa import Curve, Point, ECDSA

@dataclass
class Coin:
    curv: Curve
    G: Point
    ecdsa: ECDSA

def get_coin(p: int, a: int, b: int, x: int, y: int, n: int) -> Coin:
    curv = Curve(p=p, a=a, b=b)
    G = Point(curve=curv, x=x, y=y)
    ecdsa = ECDSA(G=G, n=n)
    return Coin(curv=curv, G=G, ecdsa=ecdsa)

BTC = get_coin(
        p = 2**256-2**32-2**9-2**8-2**7-2**6-2**4-1,
        a = 0,
        b = 7,
        x = 0x79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798,
        y = 0x483ada7726a3c4655da4fbfc0e1108a8fd17b448a68554199c47d08ffb10d4b8,
        n = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141
)
