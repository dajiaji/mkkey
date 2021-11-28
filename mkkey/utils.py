import base64


def _bytes_from_int(val: int) -> bytes:
    remaining = val
    byte_length = 0
    while remaining != 0:
        remaining >>= 8
        byte_length += 1
    return val.to_bytes(byte_length, "big", signed=False)


def base64url_encode(val: bytes) -> str:
    return base64.urlsafe_b64encode(val).replace(b"=", b"").decode()


def to_base64url_uint(val: int) -> str:
    if val < 0:
        raise ValueError("Must be a positive integer.")
    int_bytes = _bytes_from_int(val)
    if len(int_bytes) == 0:
        int_bytes = b"\x00"
    return base64url_encode(int_bytes)
