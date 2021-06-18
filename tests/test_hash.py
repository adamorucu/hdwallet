import hashlib
from hdwallet.hash import sha256, sha512

test_arr = [
  b'',
  b'asdf',
  b'abc',
  b'do you hear the people sing, singing the song of angry man it is the music of the people whowill now be slaves again' * 10
]


def test_sha256():
  for x in test_arr:
    hl = hashlib.sha256(x).hexdigest()
    my = sha256(x).hex()
    assert hl == my

def test_sha512():
  for x in test_arr:
    hl = hashlib.sha512(x).hexdigest()
    my = sha512(x).hex()
    assert hl == my
