import pytest
from jwt import PyJWK

from mkkey.jwk import generate_jwk


@pytest.mark.parametrize(
    "kty, crv, alg, use, key_ops, kid, kid_type, kid_size, output_format, rsa_key_size",
    [
        ("RSA", "", "RS256", "", False, "", "none", 0, "json", 2048),
        ("RSA", "", "RS384", "", False, "", "none", 0, "json", 2048),
        ("RSA", "", "RS512", "", False, "", "none", 0, "json", 2048),
        ("RSA", "", "PS256", "", False, "", "none", 0, "json", 2048),
        ("RSA", "", "PS384", "", False, "", "none", 0, "json", 2048),
        ("RSA", "", "PS512", "", False, "", "none", 0, "json", 2048),
        ("RSA", "", "RS256", "sig", False, "", "none", 0, "json", 2048),
        ("RSA", "", "RS256", "", True, "", "none", 0, "json", 2048),
        ("RSA", "", "RS256", "", False, "01", "none", 0, "json", 2048),
        ("RSA", "", "RS256", "", False, "01", "sha256", 0, "json", 2048),
        ("RSA", "", "RS256", "", False, "", "sha256", 0, "json", 2048),
        ("RSA", "", "RS256", "", False, "", "sha256", 32, "json", 2048),
        ("RSA", "", "RS256", "", False, "", "sha256", 16, "json", 2048),
        ("RSA", "", "RS256", "", False, "", "sha256", 8, "json", 2048),
        ("RSA", "", "RS256", "", False, "", "sha256", 8, "jwks", 2048),
        ("EC", "P-256", "", "", False, "", "none", 0, "json", 0),
        ("EC", "P-256", "ES256", "", False, "", "none", 0, "json", 0),
        ("EC", "P-384", "", "", False, "", "none", 0, "json", 0),
        ("EC", "P-384", "ES384", "", False, "", "none", 0, "json", 0),
        ("EC", "P-521", "", "", False, "", "none", 0, "json", 0),
        ("EC", "P-521", "ES512", "", False, "", "none", 0, "json", 0),
        ("EC", "secp256k1", "", "", False, "", "none", 0, "json", 0),
        ("EC", "secp256k1", "ES256K", "", False, "", "none", 0, "json", 0),
        ("EC", "P-256", "", "", False, "", "sha256", 0, "json", 0),
        ("EC", "P-256", "", "sig", False, "", "none", 0, "json", 0),
        ("EC", "P-256", "", "", True, "", "none", 0, "json", 0),
        ("OKP", "Ed25519", "", "", False, "", "none", 0, "json", 0),
        ("OKP", "Ed25519", "EdDSA", "", False, "", "none", 0, "json", 0),
        ("OKP", "Ed448", "", "", False, "", "none", 0, "json", 0),
        ("OKP", "Ed448", "EdDSA", "", False, "", "none", 0, "json", 0),
        ("OKP", "Ed25519", "", "", False, "", "sha256", 0, "json", 0),
        ("OKP", "Ed25519", "", "sig", False, "", "none", 0, "json", 0),
        ("OKP", "Ed25519", "", "", True, "", "none", 0, "json", 0),
    ],
)
def test_generate_jwk(kty, crv, alg, use, key_ops, kid, kid_type, kid_size, output_format, rsa_key_size):

    res = generate_jwk(kty, crv, alg, use, key_ops, kid, kid_type, kid_size, output_format, rsa_key_size)
    assert "secret" in res
    assert "public" in res
    jwk_dict: dict
    if output_format == "json":
        assert "jwk" in res["secret"]
        assert "kty" in res["secret"]["jwk"]
        assert "jwk" in res["public"]
        assert "kty" in res["public"]["jwk"]
        pub_dict = res["public"]["jwk"]
        priv_dict = res["secret"]["jwk"]

    elif output_format == "jwks":
        assert "jwks" in res["secret"]
        assert "keys" in res["secret"]["jwks"]
        assert isinstance(res["secret"]["jwks"]["keys"], list)
        assert len(res["secret"]["jwks"]["keys"]) == 1
        assert "jwks" in res["public"]
        assert "keys" in res["public"]["jwks"]
        assert isinstance(res["public"]["jwks"]["keys"], list)
        assert len(res["public"]["jwks"]["keys"]) == 1
        pub_dict = res["public"]["jwks"]["keys"][0]
        priv_dict = res["secret"]["jwks"]["keys"][0]

    else:
        pytest.fail("Invalid test argument.")

    # For mitigating the bug on PyJWT(<=2.3.0)
    if "crv" in pub_dict and pub_dict["crv"] == "Ed448":
        pub_dict["alg"] = priv_dict["alg"] = "EdDSA"

    try:
        pub = PyJWK.from_dict(pub_dict)
        priv = PyJWK.from_dict(priv_dict)
    except Exception as err:
        pytest.fail(f"PyJWK.from_dict() must not fail: {err}.")

    assert pub.key_type == pub_dict["kty"]
    if kid or kid_type != "none":
        assert pub.key_id == pub_dict["kid"]
    if use:
        assert pub.public_key_use == pub_dict["use"]
    assert priv.key_type == priv_dict["kty"]
    if kid or kid_type != "none":
        assert priv.key_id == priv_dict["kid"]
    if use:
        assert priv.public_key_use == priv_dict["use"]

    try:
        signature = priv.Algorithm.sign(b"Hello world!", priv.key)
        assert pub.Algorithm.verify(b"Hello world!", pub.key, signature)
    except Exception as err:
        pytest.fail(f"jwt.encode()/decode() must not fail: {err}.")


@pytest.mark.parametrize(
    "kty, crv, alg, use, kid, kid_type, kid_size, output_format, rsa_key_size, msg",
    [
        ("RSA", "", "RS256", "", "", "xxx", 0, "json", 2048, "Invalid kid_type: xxx."),
        ("EC", "P-256", "", "", "", "xxx", 0, "json", 0, "Invalid kid_type: xxx."),
        ("OKP", "Ed25519", "", "", "", "xxx", 0, "json", 0, "Invalid kid_type: xxx."),
        ("EC", "P-xxx", "", "", "", "none", 0, "json", 0, "Invalid crv for EC: P-xxx."),
        ("EC", "P-256", "ES384", "", "", "none", 0, "json", 0, "alg must be ES256."),
        ("EC", "P-384", "ES256", "", "", "none", 0, "json", 0, "alg must be ES384."),
        ("EC", "P-521", "ES256", "", "", "none", 0, "json", 0, "alg must be ES512."),
        ("EC", "secp256k1", "ES256", "", "", "none", 0, "json", 0, "alg must be ES256K."),
        ("OKP", "xxx", "", "", "", "none", 0, "json", 0, "Invalid crv for OKP: xxx."),
        ("OKP", "Ed25519", "ECDSA", "", "", "none", 0, "json", 0, "alg must be EdDSA."),
        ("RSA", "", "RS256", "", "", "sha256", 64, "json", 2048, "size is longer than the source kid"),
        ("xxx", "", "RS256", "", "", "none", 0, "json", 2048, "Invalid kty: xxx."),
        ("RSA", "", "RS256", "", "", "none", 0, "xxx", 2048, "Invalid output_format: xxx."),
    ],
)
def test_generate_jwk_with_invalid_arg(kty, crv, alg, use, kid, kid_type, kid_size, output_format, rsa_key_size, msg):

    with pytest.raises(ValueError) as err:
        generate_jwk(kty, crv, alg, use, False, kid, kid_type, kid_size, output_format, rsa_key_size)
        pytest.fail("generate_jwk() must fail.")
    assert msg in str(err.value)
