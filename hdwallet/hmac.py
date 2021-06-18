#!/usr/bin/python3
"""
Resources:
    - https://github.com/python/cpython/blob/3.9/Lib/hmac.py
"""
from hdwallet.hash import sha512
from hdwallet.utils import byte2int, int2byte
import hashlib

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
