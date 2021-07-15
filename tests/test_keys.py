from hdwallet.keys import PublicKey
from hdwallet.currencies import BTC


def test_public_key():
    pk = PublicKey.from_sk(0x1E99423A4ED27608A15A2616A2B0E9E52CED330AC530EDCC32C8FFC6A526AEDD)
    print(hex(int(pk.x)))
    assert format(int(pk.x), '064x').upper() == 'F028892BAD7ED57D2FB57BF33081D5CFCF6F9ED3D3D7F159C2E2FFF579DC341A'
    print(pk.y)
    assert format(pk.y, '064x').upper() == '07CF33DA18BD734C600B96A72BBC4749D5141C90EC8AC328AE52DDFE2E505BDB'
