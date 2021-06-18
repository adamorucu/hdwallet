import hashlib
import hmac
from hdwallet.hmac import hmac_sha512


def test_hmac_sha512():
    key = b'asdf'
    msgs = [b'', b'abc', b'do you hear the people sing singing the song of angry man']
    for msg in msgs:
        tr = hmac.digest(key, msg, hashlib.sha512).hex()
        my = hmac_sha512(key, msg).hex()
        assert my == tr



# def test_pbkdf2_hmac():
    # hl = hashlib.pbkdf2_hmac(
	# hash_name='sha512',
	# password=sentence,
	# salt=b'mnemonic'+passphrase.encode(),
	# iterations=2048).hex()
