#!/usr/bin/python3
"""
SHA256 algorithm

Resource: https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.180-4.pdf
"""

K = [
    0x428a2f98, 0x71374491, 0xb5c0fbcf, 0xe9b5dba5, 0x3956c25b,
    0x59f111f1, 0x923f82a4, 0xab1c5ed5, 0xd807aa98, 0x12835b01,
    0x243185be, 0x550c7dc3, 0x72be5d74, 0x80deb1fe, 0x9bdc06a7,
    0xc19bf174, 0xe49b69c1, 0xefbe4786, 0x0fc19dc6, 0x240ca1cc,
    0x2de92c6f, 0x4a7484aa, 0x5cb0a9dc, 0x76f988da, 0x983e5152,
    0xa831c66d, 0xb00327c8, 0xbf597fc7, 0xc6e00bf3, 0xd5a79147,
    0x06ca6351, 0x14292967, 0x27b70a85, 0x2e1b2138, 0x4d2c6dfc,
    0x53380d13, 0x650a7354, 0x766a0abb, 0x81c2c92e, 0x92722c85,
    0xa2bfe8a1, 0xa81a664b, 0xc24b8b70, 0xc76c51a3, 0xd192e819,
    0xd6990624, 0xf40e3585, 0x106aa070, 0x19a4c116, 0x1e376c08,
    0x2748774c, 0x34b0bcb5, 0x391c0cb3, 0x4ed8aa4a, 0x5b9cca4f,
    0x682e6ff3, 0x748f82ee, 0x78a5636f, 0x84c87814, 0x8cc70208,
    0x90befffa, 0xa4506ceb, 0xbef9a3f7, 0xc67178f2
]

from typing import List

from hdwallet.utils import byte2int, int2byte

def rotr(x: int, n: int, size: int=32) -> int:
    """Rotate right"""
    return (x >> n) | (x << (size - n))

def shr(x: int, n: int) -> int:
    """Shift right"""
    return x >> n

def ch(x: int, y: int, z: int) -> int:
    """Choice: chooses y or z depending on the x"""
    return (x & y) ^ (~x & z)

def maj(x: int, y: int, z: int) -> int:
    """Majority: chooses the majority of the three words"""
    return (x & y) ^ (x & z) ^ (y & z)

def bigsig0(x: int, sha: int=256) -> int:
    if sha==256:
        print('no')
        return rotr(x, 2) ^ rotr(x, 13) ^ rotr(x, 22)
    else:
        return rotr(x, 28, 64) ^ rotr(x, 34, 64) ^ rotr(x, 39, 64)

def bigsig1(x: int, sha: int=256) -> int:
    if sha==256:
        return rotr(x, 6) ^ rotr(x, 11) ^ rotr(x, 25)
    else:
        return rotr(x, 14, 64) ^ rotr(x, 18, 64) ^ rotr(x, 41, 64)

def sig0(x: int, sha: int=256) -> int:
    if sha==256:
        return rotr(x, 7) ^ rotr(x, 18) ^ shr(x, 3)
    else:
        return rotr(x, 1, 64) ^ rotr(x, 8, 64) ^ shr(x, 7)

def sig1(x: int, sha: int=256) -> int:
    if sha==256:
        return rotr(x, 17) ^ rotr(x, 19) ^ shr(x, 10)
    else:
        return rotr(x, 19, 64) ^ rotr(x, 61, 64) ^ shr(x, 6)

def pad(m: bytes, sha: int=256) -> bytes:
    """ Padding
    ref: Karpathy """
    if sha == 256:
        mod = 512
        eq = 448
        bl = 64//8 # end block length
    elif sha == 512:
        mod = 1024
        eq = 896
        bl = 128//8 # end block length
    else:
        raise NotImplementedError

    l = len(m) * 8 # bytes -> bits
    b = bytearray(m)
    b.append(0x80) # = 1 and 7 zeros

    while (len(b)*8) % mod != eq:
        b.append(0x0)

    b.extend(l.to_bytes(bl, 'big'))
    return b

def parse(b: bytes, sha=256) -> List[bytes]:
    """Splits message into 512 bit blocks"""
    N = sha //4
    return [b[i:i+N] for i in range(0, len(b), N)]

def sha256(m: bytes) -> bytes:
    H = [0x6a09e667, 0xbb67ae85, 0x3c6ef372, 0xa54ff53a, 0x510e527f, 0x9b05688c, 0x1f83d9ab, 0x5be0cd19]
    b = pad(m)
    blx = parse(b)

    for M in blx:
        W = []
        print(len(M))

        for t in range(64):
            if t < 16:
                W.append(M[t*4:t*4+4])
            else:
                temp = sig1(byte2int(W[t-2])) + byte2int(W[t-7])\
                    + sig0(byte2int(W[t-15])) + byte2int(W[t-16])
                W.append(int2byte(temp % 2**32))

        a, b, c, d, e, f, g, h = H

        for t in range(64):
            T1 = (h + bigsig1(e) + ch(e,f,g) + K[t] + byte2int(W[t])) % 2**32
            T2 = (bigsig0(a) + maj(a,b,c)) % 2**32
            h = g
            g = f
            f = e
            e = (d + T1) % 2**32
            d = c
            c = b
            b = a
            a = (T1 + T2) % 2**32

        diff = [a,b,c,d,e,f,g,h]
        H = [(Hi + alpha) % 2**32 for Hi, alpha in zip(H, diff)]

    return b''.join([int2byte(hi) for hi in H])


K512 = [
    0x428a2f98d728ae22, 0x7137449123ef65cd, 0xb5c0fbcfec4d3b2f, 0xe9b5dba58189dbbc,
    0x3956c25bf348b538, 0x59f111f1b605d019, 0x923f82a4af194f9b, 0xab1c5ed5da6d8118,
    0xd807aa98a3030242, 0x12835b0145706fbe, 0x243185be4ee4b28c, 0x550c7dc3d5ffb4e2,
    0x72be5d74f27b896f, 0x80deb1fe3b1696b1, 0x9bdc06a725c71235, 0xc19bf174cf692694,
    0xe49b69c19ef14ad2, 0xefbe4786384f25e3, 0x0fc19dc68b8cd5b5, 0x240ca1cc77ac9c65,
    0x2de92c6f592b0275, 0x4a7484aa6ea6e483, 0x5cb0a9dcbd41fbd4, 0x76f988da831153b5,
    0x983e5152ee66dfab, 0xa831c66d2db43210, 0xb00327c898fb213f, 0xbf597fc7beef0ee4,
    0xc6e00bf33da88fc2, 0xd5a79147930aa725, 0x06ca6351e003826f, 0x142929670a0e6e70,
    0x27b70a8546d22ffc, 0x2e1b21385c26c926, 0x4d2c6dfc5ac42aed, 0x53380d139d95b3df,
    0x650a73548baf63de, 0x766a0abb3c77b2a8, 0x81c2c92e47edaee6, 0x92722c851482353b,
    0xa2bfe8a14cf10364, 0xa81a664bbc423001, 0xc24b8b70d0f89791, 0xc76c51a30654be30,
    0xd192e819d6ef5218, 0xd69906245565a910, 0xf40e35855771202a, 0x106aa07032bbd1b8,
    0x19a4c116b8d2d0c8, 0x1e376c085141ab53, 0x2748774cdf8eeb99, 0x34b0bcb5e19b48a8,
    0x391c0cb3c5c95a63, 0x4ed8aa4ae3418acb, 0x5b9cca4f7763e373, 0x682e6ff3d6b2b8a3,
    0x748f82ee5defb2fc, 0x78a5636f43172f60, 0x84c87814a1f0ab72, 0x8cc702081a6439ec,
    0x90befffa23631e28, 0xa4506cebde82bde9, 0xbef9a3f7b2c67915, 0xc67178f2e372532b,
    0xca273eceea26619c, 0xd186b8c721c0c207, 0xeada7dd6cde0eb1e, 0xf57d4f7fee6ed178,
    0x06f067aa72176fba, 0x0a637dc5a2c898a6, 0x113f9804bef90dae, 0x1b710b35131c471b,
    0x28db77f523047d84, 0x32caab7b40c72493, 0x3c9ebe0a15c9bebc, 0x431d67c49c100d4c,
    0x4cc5d4becb3e42b6, 0x597f299cfc657e2a, 0x5fcb6fab3ad6faec, 0x6c44198c4a475817
]

def sha512(m: bytes) -> bytes:
    H = [0x6a09e667f3bcc908, 0xbb67ae8584caa73b, 0x3c6ef372fe94f82b, 0xa54ff53a5f1d36f1,
        0x510e527fade682d1, 0x9b05688c2b3e6c1f, 0x1f83d9abfb41bd6b, 0x5be0cd19137e2179]

    b = pad(m, sha=512)
    blx = parse(b, sha=512)
    for M in blx:
        print(len(M))
        W = []
        for t in range(80):
            if t < 16:
                W.append(M[t*8:t*8+8])
            else:
                temp = sig1(byte2int(W[t-2]), sha=512) + byte2int(W[t-7])\
                    + sig0(byte2int(W[t-15]), sha=512) + byte2int(W[t-16])
                W.append(int2byte(temp % 2**64, 8))

        a, b, c, d, e, f, g, h = H
        for t in range(80):
            T1 = (h + bigsig1(e, sha=512) + ch(e,f,g) + K512[t] + byte2int(W[t])) % 2**64
            T2 = (bigsig0(a, sha=512) + maj(a,b,c)) % 2**64
            h = g
            g = f
            f = e
            e = (d + T1) % 2**64
            d = c
            c = b
            b = a
            a = (T1 + T2) % 2**64
        H = [(hi + alpha) % 2**64 for hi, alpha in zip(H, [a,b,c,d,e,f,g,h])]
    return b''.join(int2byte(hi, 8) for hi in H)

if __name__ == '__main__':
    print()
    s = b'abc'
    a = sha512(s).hex()
    print(a)
    print(type(a))
    print()
    import hashlib
    print(hashlib.sha512(s).hexdigest())
