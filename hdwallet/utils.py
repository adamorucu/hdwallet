"""Some utility functions"""
import os

def byte2int(byt: bytes) -> int:
    return int.from_bytes(byt, 'big')

def int2byte(i: int, length: int=4) -> bytes:
    return i.to_bytes(length, 'big')

def wordlist():
    filename = f"{os.getcwd()}/hdwallet/wordlist.txt"
    wordlist = []
    with open(filename) as f:
        for line in f:
            wordlist.append(line.strip())
    return wordlist
