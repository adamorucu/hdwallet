"""Some utility functions"""
import os
from typing import List

def byte2int(byt: bytes) -> int:
    """bytes to int conversion (big-endian)"""
    return int.from_bytes(byt, 'big')

def int2byte(i: int, length: int=4) -> bytes:
    """int to bytes conversion (big-endian)"""
    return i.to_bytes(length, 'big')

def wordlist() -> List[str]:
    """Returns mnemonic word list"""
    filename = f"{os.getcwd()}/hdwallet/wordlist.txt"
    wl = []
    with open(filename) as f:
        for line in f:
            wl.append(line.strip())
    return wl
