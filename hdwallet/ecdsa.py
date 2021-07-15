"""
Elliptic Curve Digital Signature Algorithm

Resources:
    - https://en.bitcoin.it/wiki/Elliptic_Curve_Digital_Signature_Algorithm
    - https://github.com/ethereumbook/ethereumbook/blob/develop/04keys-addresses.asciidoc
    - https://en.wikipedia.org/wiki/Elliptic_curve_point_multiplication#Point_addition
    - https://github.com/karpathy/cryptos/blob/main/cryptos/curves.py
"""
from __future__ import annotations
from dataclasses import dataclass
import math

def extended_euclidean_algorithm(a, b):
    """By Karpathy"""
    old_r, r = a, b
    old_s, s = 1, 0
    old_t, t = 0, 1
    while r != 0:
        quotient = old_r // r
        old_r, r = r, old_r - quotient * r
        old_s, s = s, old_s - quotient * s
        old_t, t = t, old_t - quotient * t
    return old_r, old_s, old_t

def inv(n, p):
    """by karpathy"""
    gcd, x, y = extended_euclidean_algorithm(n, p)
    return x % p

@dataclass
class Curve:
    p: int
    a: int
    b: int

@dataclass
class Point:
    curve: Curve
    x: int
    y: int

    def __add__(self, other: Point) -> Point:
        # handle special case of P + 0 = 0 + P = 0
        if self == None:
            return other
        if other == None:
            return self
        # handle special case of P + (-P) = 0
        if self.x == other.x and self.y != other.y:
            return None
        # compute the "slope"
        if self.x == other.x: # (self.y = other.y is guaranteed too per above check)
            m = (3 * self.x**2 + self.curve.a) * inv(2 * self.y, self.curve.p)
        else:
            m = (self.y - other.y) * inv(self.x - other.x, self.curve.p)
        # compute the new point
        rx = (m**2 - self.x - other.x) % self.curve.p
        ry = (-(m*(rx - self.x) + self.y)) % self.curve.p
        return Point(self.curve, rx, ry)

    # def __radd__(self, p):
    #     if self == None:
    #         return p
    #     if p == None:
    #         return self
    #     if self.x == p.x and self.y != p.y:
    #         return None

    #     lmb = (p.y - self.y) / (p.x - self.x)
    #     # lmb = (self.y - p.y) / (self.x - p.x)
    #     xnew = (lmb**2 - self.x - p.x) % self.curve.p
    #     ynew = (lmb * (self.x - xnew) - self.y) % self.curve.p
    #     # ynew = (lmb * (p.x - xnew) - p.y) % self.curve.p
    #     return Point(curve=self.curve, x=xnew, y=ynew)

    # def __add__(self, p):
    #     if self == None:
    #         return p
    #     if p == None:
    #         return self
    #     if self.x == p.x and self.y != p.y:
    #         return None

    #     # lmb = (p.y - self.y) / (p.x - self.x)
    #     lmb = (self.y - p.y) / (self.x - p.x)
    #     xnew = (lmb**2 - self.x - p.x) % self.curve.p
    #     # ynew = (lmb * (self.x - xnew) - self.y) % self.curve.p
    #     ynew = (lmb * (p.x - xnew) - p.y) % self.curve.p
    #     return Point(curve=self.curve, x=xnew, y=ynew)

    def __rmul__(self, k: int):
        """by karpathy"""
        assert isinstance(k, int) and k >= 0
        result = None
        append = self
        while k:
            if k & 1:
                result = append + result
            append = append + append
            k >>= 1
        return result

    # def double(self):
    #     if self == None or self.y == 0:
    #         return None

    #     lmb = (3 * self.x**2 + self.curve.a) / (2 * self.y)
    #     xnew = (lmb**2 - self.x - self.x) % self.curve.p
    #     ynew = (lmb * (self.x - xnew) - self.y) % self.curve.p
    #     return Point(curve=self.curve, x=xnew, y=ynew)

    # def montgomery_ladder(self, k: int):
    #     r0 = None
    #     r1 = self
    #     m = math.floor(math.log2(k))
    #     d = str(bin(k)[2:])[::-1]
    #     for i in range(m, 0, -1):
    #         if d[i] == '0':
    #             r1 = r0 + r1
    #             if r0 != None:
    #                 r0 = r0.double()
    #         else:
    #             r0 = r0 + r1
    #             if r1 != None:
    #                 r1 = r1.double()
    #     return r1

@dataclass
class ECDSA:
    G: Point
    n: int

