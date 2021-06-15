import hashlib
from hdwallet.sha256 import sha256

test_arr = [
  b'',
  b'asdf',
  b'abc',
  b'do you hear the people sing, singing the song of angry man it is the music of the people whowill now be slaves again' * 10
]

def test_sha256():
  for x in test_arr:
    hl = hashlib.sha256(x).hexdigest()
    my = sha256(x)
    assert hl == my
