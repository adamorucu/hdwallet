#!/usr/bin/python3
import hashlib
import hmac
from hdwallet.pbkdf2 import hmac_sha512, pbkdf2

def test_hmac_sha512():
    key = b'asdf'
    msgs = [b'', b'abc', b'do you hear the people sing singing the song of angry man']
    for msg in msgs:
        tr = hmac.digest(key, msg, hashlib.sha512).hex()
        my = hmac_sha512(key, msg).hex()
        assert my == tr

def test_pbkdf2_hmac():
    salt = b'mnemonic'+"".encode()
    pwd = b"army van defense carry jealous true garbage claim echo media make crunch"
    iters = 2048
    hl = hashlib.pbkdf2_hmac(
	hash_name='sha512',
	password=pwd,
	salt= salt,
	iterations=iters).hex()

    my = pbkdf2(hmac_sha512, pwd, salt, iters).hex()
    assert my == hl
