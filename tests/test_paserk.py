from secrets import token_bytes

import pytest

from mkkey.paserk import generate_local_paserk, generate_public_paserk


@pytest.mark.parametrize(
    "version, kid, password, rsa_key_size",
    [
        (1, False, "", 2048),
        (2, False, "", 0),
        (3, False, "", 0),
        (4, False, "", 0),
        (1, True, "", 2048),
        (2, True, "", 0),
        (3, True, "", 0),
        (4, True, "", 0),
        (1, False, "mysecret", 2048),
        (2, False, "mysecret", 0),
        (3, False, "mysecret", 0),
        (4, False, "mysecret", 0),
        (1, True, "mysecret", 2048),
        (2, True, "mysecret", 0),
        (3, True, "mysecret", 0),
        (4, True, "mysecret", 0),
    ],
)
def test_generate_public_paserk(version, kid, password, rsa_key_size):

    res = generate_public_paserk(version, kid, password, rsa_key_size)
    assert "secret" in res
    assert "public" in res
    assert "paserk" in res["secret"]
    assert "paserk" in res["public"]


@pytest.mark.parametrize(
    "version, kid, password, rsa_key_size, msg",
    [
        (0, False, "", 0, "Invalid version: 0."),
        (-1, False, "", 0, "Invalid version: -1."),
        (100, False, "", 0, "Invalid version: 100."),
    ],
)
def test_generate_public_paserk_with_invalid_arg(version, kid, password, rsa_key_size, msg):

    with pytest.raises(ValueError) as err:
        generate_public_paserk(version, kid, password, rsa_key_size)
        pytest.fail("generate_public_paserk() must fail.")
    assert msg in str(err.value)


@pytest.mark.parametrize(
    "version, key_material, kid, password",
    [
        (1, "", False, ""),
        (2, "", False, ""),
        (3, "", False, ""),
        (4, "", False, ""),
        (1, "mysupersecret", False, ""),
        (2, token_bytes(32), False, ""),
        (3, "mysupersecret", False, ""),
        (4, "mysupersecret", False, ""),
        (1, "", False, "mysecret"),
        (2, "", False, "mysecret"),
        (3, "", False, "mysecret"),
        (4, "", False, "mysecret"),
        (1, "", True, ""),
        (2, "", True, ""),
        (3, "", True, ""),
        (4, "", True, ""),
    ],
)
def test_generate_local_paserk(version, key_material, kid, password):

    res = generate_local_paserk(version, key_material, kid, password)
    assert "secret" in res
    if kid:
        assert "kid" in res["secret"]
    assert "paserk" in res["secret"]
