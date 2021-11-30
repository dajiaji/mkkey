from copy import deepcopy
from typing import Any

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import ec, rsa
from cryptography.hazmat.primitives.asymmetric.ed448 import Ed448PrivateKey
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey

from .utils import base64url_encode, to_base64url_uint


def generate_jwk(
    kty: str,
    crv: str = "",
    alg: str = "",
    use: str = "",
    kid_policy: str = "none",
    kid_size: int = 32,
    kid: str = "",
    output_format: str = "json",
    rsa_key_size: int = 2048,
) -> dict:

    k: Any
    res: dict = {}
    if kty == "rsa":
        k = rsa.generate_private_key(65537, key_size=rsa_key_size)

        # public
        pn = k.private_numbers().public_numbers
        pk = {"kty": "RSA"}
        if alg:
            pk["alg"] = alg
        if use:
            pk["use"] = use
        pk["n"] = to_base64url_uint(pn.n)
        pk["e"] = to_base64url_uint(pn.e)

        # secret
        sn = k.private_numbers()
        sk = deepcopy(pk)
        sk["d"] = to_base64url_uint(sn.d)
        sk["p"] = to_base64url_uint(sn.p)
        sk["q"] = to_base64url_uint(sn.q)
        sk["dp"] = to_base64url_uint(sn.dmp1)
        sk["dq"] = to_base64url_uint(sn.dmq1)
        sk["qi"] = to_base64url_uint(sn.iqmp)

    elif kty == "ec":
        key_len: int
        if crv == "P-256":
            k = ec.generate_private_key(ec.SECP256R1())
            key_len = 32
        elif crv == "P-384":
            k = ec.generate_private_key(ec.SECP384R1())
            key_len = 48
        elif crv == "P-521":
            k = ec.generate_private_key(ec.SECP521R1())
            key_len = 66
        elif crv == "secp256k1":
            k = ec.generate_private_key(ec.SECP256K1())
            key_len = 32
        else:
            raise ValueError(f"Invalid crv for EC: {crv}.")

        # public
        pk = {"kty": "EC", "crv": crv}
        if alg:
            pk["alg"] = alg
        if use:
            pk["use"] = use
        pk["x"] = base64url_encode(
            k.public_key().public_numbers().x.to_bytes(key_len, byteorder="big")
        )
        pk["y"] = base64url_encode(
            k.public_key().public_numbers().y.to_bytes(key_len, byteorder="big")
        )

        # secret
        sk = deepcopy(pk)
        sk["d"] = base64url_encode(
            k.private_numbers().private_value.to_bytes(key_len, byteorder="big")
        )

    elif kty == "okp":
        if crv == "Ed25519":
            k = Ed25519PrivateKey.generate()
        elif crv == "Ed448":
            k = Ed448PrivateKey.generate()
        else:
            raise ValueError(f"Invalid crv for OKP: {crv}.")

        x = k.public_key().public_bytes(
            serialization.Encoding.Raw, serialization.PublicFormat.Raw
        )
        d = k.private_bytes(
            serialization.Encoding.Raw,
            serialization.PrivateFormat.Raw,
            serialization.NoEncryption(),
        )

        # public
        pk = {"kty": "OKP", "crv": crv}
        if alg:
            pk["alg"] = alg
        if use:
            pk["use"] = use
        pk["x"] = base64url_encode(x)

        # secret
        sk = deepcopy(pk)
        sk["d"] = base64url_encode(d)

    else:
        raise ValueError(f"Invalid kty: {kty}.")

    if output_format == "json":
        res["public"] = {"jwk": pk}
        res["secret"] = {"jwk": sk}
    elif output_format == "jwks":
        res["public"] = {"jwks": {"keys": [pk]}}
        res["secret"] = {"jwks": {"keys": [sk]}}
    else:
        raise ValueError(f"Invalid output_format: {output_format}.")
    return res
