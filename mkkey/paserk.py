from secrets import token_bytes
from typing import Any, Union

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import ec, rsa
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
from pyseto import Key


def generate_public_paserk(
    version: int,
    kid: bool,
    password: str,
    wrapping_key: str,
    rsa_key_size: int = 2048,
) -> dict:

    if password and wrapping_key:
        raise ValueError("Only one of password or wrapping_key must be specified.")

    k: Any
    if version == 1:
        k = rsa.generate_private_key(65537, key_size=rsa_key_size)
    elif version in [2, 4]:
        k = Ed25519PrivateKey.generate()
    elif version == 3:
        k = ec.generate_private_key(ec.SECP384R1())
    else:
        raise ValueError(f"Invalid version: {version}.")

    priv_pem = k.private_bytes(
        serialization.Encoding.PEM,
        serialization.PrivateFormat.PKCS8,
        serialization.NoEncryption(),
    )
    pub_key = k.public_key()
    pub_pem = pub_key.public_bytes(
        serialization.Encoding.PEM,
        serialization.PublicFormat.SubjectPublicKeyInfo,
    )
    res: dict = {"public": {}, "secret": {}}
    pk = Key.new(version, "public", pub_pem)
    sk = Key.new(version, "public", priv_pem)
    if kid:
        res["public"]["kid"] = pk.to_paserk_id()
        res["secret"]["kid"] = sk.to_paserk_id()
    res["public"]["paserk"] = pk.to_paserk()
    res["secret"]["paserk"] = sk.to_paserk(password=password, wrapping_key=wrapping_key)
    return res


def generate_local_paserk(
    version: int,
    key_material: Union[str, bytes],
    kid: bool,
    password: str = "",
    wrapping_key: str = "",
) -> dict:

    if password and wrapping_key:
        raise ValueError("Only one of password or wrapping_key must be specified.")
    if not key_material:
        key_material = token_bytes(32)

    res: dict = {"secret": {}}
    sk = Key.new(version, "local", key_material)
    if kid:
        res["secret"]["kid"] = sk.to_paserk_id()
    res["secret"]["paserk"] = sk.to_paserk(password=password, wrapping_key=wrapping_key)
    return res
