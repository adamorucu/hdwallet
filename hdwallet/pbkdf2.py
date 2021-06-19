#!/usr/bin/python3
"""
Password-based key derivation function 2 and a HMAC function for its use

Resources:
    - https://github.com/python/cpython/blob/3.9/Lib/hmac.py
    - https://en.wikipedia.org/wiki/PBKDF2
"""
from typing import Callable

from hdwallet.hash import sha512
from hdwallet.utils import byte2int, int2byte

def hmac_sha512(key: bytes, m: bytes) -> bytes:
    """ Hash-based message authentication code using SHA512 as hash function """
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

def pbkdf2(prf: Callable, pwd: bytes, salt: bytes, iters: int, repeat: int=1) -> bytes:
    """
    Password-based key derivation function 2
        Parameters:
            prf (Callable): Pseudo-random function
            pwd (bytes): master password from which derived key is generated
            salt (bytes): cryptographic salt
            iters (int): the number of iterations
            repeat (int): the number of times the process should be repeated,
                used to get a key of different length
        Returns:
            derived key (bytes): byte string
    """
    dk = b''
    for i in range(1, repeat+1):
        t = prf(pwd, salt + int2byte(i, 4))
        u = t
        t = byte2int(t)
        for _ in range(iters-1):
            u = prf(pwd, u)
            t ^=  byte2int(u)
        dk += int2byte(t, 64)
    return dk
