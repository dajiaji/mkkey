import pytest

from mkkey.jwk import generate_jwk


@pytest.mark.parametrize(
    "kty, crv, alg, use, kid, kid_type, kid_size, output_format, rsa_key_size",
    [
        ("RSA", "", "RS256", "", "", "none", 0, "json", 2048),
        ("RSA", "", "RS384", "", "", "none", 0, "json", 2048),
        ("RSA", "", "RS512", "", "", "none", 0, "json", 2048),
        ("RSA", "", "PS256", "", "", "none", 0, "json", 2048),
        ("RSA", "", "PS384", "", "", "none", 0, "json", 2048),
        ("RSA", "", "PS512", "", "", "none", 0, "json", 2048),
        ("RSA", "", "RS256", "sig", "", "none", 0, "json", 2048),
        ("RSA", "", "RS256", "", "01", "none", 0, "json", 2048),
        ("RSA", "", "RS256", "", "01", "sha256", 0, "json", 2048),
        ("RSA", "", "RS256", "", "", "sha256", 0, "json", 2048),
        ("RSA", "", "RS256", "", "", "sha256", 32, "json", 2048),
        ("RSA", "", "RS256", "", "", "sha256", 16, "json", 2048),
        ("RSA", "", "RS256", "", "", "sha256", 8, "json", 2048),
        ("RSA", "", "RS256", "", "", "sha256", 8, "jwks", 2048),
        ("EC", "P-256", "", "", "", "none", 0, "json", 0),
        ("EC", "P-256", "ES256", "", "", "none", 0, "json", 0),
        ("EC", "P-384", "", "", "", "none", 0, "json", 0),
        ("EC", "P-384", "ES384", "", "", "none", 0, "json", 0),
        ("EC", "P-521", "", "", "", "none", 0, "json", 0),
        ("EC", "P-521", "ES512", "", "", "none", 0, "json", 0),
        ("EC", "secp256k1", "", "", "", "none", 0, "json", 0),
        ("EC", "secp256k1", "ES256K", "", "", "none", 0, "json", 0),
        ("EC", "P-256", "", "", "", "sha256", 0, "json", 0),
        ("EC", "P-256", "", "sig", "", "none", 0, "json", 0),
        ("OKP", "Ed25519", "", "", "", "none", 0, "json", 0),
        ("OKP", "Ed25519", "EdDSA", "", "", "none", 0, "json", 0),
        ("OKP", "Ed448", "", "", "", "none", 0, "json", 0),
        ("OKP", "Ed448", "EdDSA", "", "", "none", 0, "json", 0),
        ("OKP", "Ed25519", "", "", "", "sha256", 0, "json", 0),
        ("OKP", "Ed25519", "", "sig", "", "none", 0, "json", 0),
    ],
)
def test_generate_jwk(kty, crv, alg, use, kid, kid_type, kid_size, output_format, rsa_key_size):

    res = generate_jwk(kty, crv, alg, use, kid, kid_type, kid_size, output_format, rsa_key_size)
    assert "secret" in res
    assert "public" in res
    if output_format == "json":
        assert "jwk" in res["secret"]
        assert "kty" in res["secret"]["jwk"]
        assert "jwk" in res["public"]
        assert "kty" in res["public"]["jwk"]

    elif output_format == "jwks":
        assert "jwks" in res["secret"]
        assert "keys" in res["secret"]["jwks"]
        assert isinstance(res["secret"]["jwks"]["keys"], list)
        assert len(res["secret"]["jwks"]["keys"]) == 1
        assert "jwks" in res["public"]
        assert "keys" in res["public"]["jwks"]
        assert isinstance(res["public"]["jwks"]["keys"], list)
        assert len(res["public"]["jwks"]["keys"]) == 1

    else:
        pytest.fail("Invalid test argument.")


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
        generate_jwk(kty, crv, alg, use, kid, kid_type, kid_size, output_format, rsa_key_size)
        pytest.fail("generate_jwk() must fail.")
    assert msg in str(err.value)
