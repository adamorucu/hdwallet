#!/usr/bin/python3
"""
Resources:
    - https://github.com/python/cpython/blob/3.9/Lib/hmac.py
    - https://en.wikipedia.org/wiki/PBKDF2
"""
from functools import reduce

from hdwallet.hash import sha512
from hdwallet.utils import byte2int, int2byte

def hmac_sha512(key: bytes, m: bytes) -> bytes:
    bsize = 1024//8
    if len(key) > bsize:
        key = sha512(key)

    o = bytes((x ^ 0x5c) for x in range(256))
    i = bytes((x ^ 0x36) for x in range(256))

    key = key + b'\x00' * (bsize - len(key))
    opad_key = key.translate(o)
    ipad_key = key.translate(i)
    ipad = sha512(ipad_key + m)
    opad = sha512(opad_key + ipad)
    return opad

def pbkdf2(prf, pwd, salt, iters, len_offset=1):
    dk = b''
    for i in range(1, len_offset+1):
        t = prf(pwd, salt + int2byte(i, 4))
        u = t
        t = byte2int(t)
        for _ in range(iters-1):
            u = prf(pwd, u)
            t ^=  byte2int(u)
        dk += int2byte(t, 64)
    return dk
