import pytest

from salic_api.utils import encrypt, decrypt


@pytest.fixture(params=['foo', 'foobar', '1234', 'ação'])
def msg(request):
    return request.param


@pytest.fixture
def encrypted(msg):
    return encrypt(msg)


def test_encrypt_decrypt(msg, encrypted):
    assert decrypt(encrypted) == msg
