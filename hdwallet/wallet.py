#!/usr/bin/python
"""
Hierarchical Deterministic Wallet

Resources:
    - https://github.com/bitcoin/bips/blob/master/bip-0039.mediawiki
    - https://github.com/ethereumbook/ethereumbook/blob/develop/05wallets.asciidoc
"""
import os
from dataclasses import dataclass
from math import ceil
from typing import Optional
import hashlib

from hdwallet.hash import sha256
from hdwallet.utils import byte2int, int2byte, wordlist
from hdwallet.pbkdf2 import pbkdf2, hmac_sha512

@dataclass
class Wallet:
    """ Hierarchical Deterministic Wallet"""
    mnemonic: str
    passphrase: str
    seed: Optional[int]

    @classmethod
    def generate(cls, passphrase: str=None, entropy: int=None):
        """Randomly generate a wallet"""
        if entropy == None:
            l = 256 # entropy length
            ent = os.urandom(l//8)
        else:
            l = ceil((len(entropy) * 4) / 32) * 32
            ent = int2byte(int(entropy, 16), l//8)
        cl = l//32 # checksum length
        hash = sha256(ent).hex()
        checksum = bin(int(hash, 16))[2:].zfill(256)[:cl]
        b = bin(byte2int(ent))[2:].zfill(l) + checksum
        indices = [int('0b' + b[i:i+11], 2) for i in range(0,len(b), 11)]
        wl = wordlist()
        cls.mnemonic =  ' '.join(wl[ind] for ind in indices)
        cls.passphrase = passphrase
        return cls

    @staticmethod
    def menmomic2seed(mnemonic: str, passphrase: str) -> int:
        """Conversion from mnemonic words to seed"""
        salt = b'mnemonic' + passphrase.encode()
        seed = pbkdf2(hmac_sha512, mnemonic.encode(), salt, 2048)
        return seed

    # def get_seed(self) -> int:
    #     if self.seed == None:
    #         self.seed = Wallet.menmomic2seed(self.mnemonic, self.passphrase)
    #     return self.seed

    # def master_key(self) -> int:
    #     salt = b'' + self.passphrase.encode()
    #     hash = pbkdf2(hmac_sha512, self.seed.encode(), salt, 2048)
    #     mid = int(len(hash)/2)
    #     return hash[:mid], hash[mid:]
