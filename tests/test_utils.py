import pytest

from mkkey.utils import to_base64url_uint


@pytest.mark.parametrize(
    "val, msg",
    [
        (-1, "Must be a positive integer."),
    ],
)
def test_to_base64url_uint(val, msg):
    with pytest.raises(ValueError) as err:
        to_base64url_uint(val)
        pytest.fail("to_base64url_uint() must fail.")
    assert msg in str(err.value)
