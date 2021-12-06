import json

import pytest
from click.testing import CliRunner

from mkkey.cli import cli, jwk, paserk

runner = CliRunner()


def test_cli_install():

    res = runner.invoke(cli, ["--install"])
    assert res.exit_code in [0, 1]
    if res.exit_code == 0:
        assert "bash completion installed in" in res.output


def test_cli_help():

    res = runner.invoke(cli, ["--help"])
    assert res.exit_code == 0
    assert "Usage: cli [OPTIONS] COMMAND [ARGS]..." in res.output


def test_cli_version():

    res = runner.invoke(cli, ["--version"])
    assert res.exit_code == 0
    assert "cli, version" in res.output


@pytest.mark.parametrize(
    "args",
    [
        ["rsa"],
        ["ec"],
        ["okp"],
        ["rsa", "--alg", "RS256"],
        ["rsa", "--alg", "RS384"],
        ["rsa", "--alg", "RS512"],
        ["rsa", "--alg", "PS256"],
        ["rsa", "--alg", "PS384"],
        ["rsa", "--alg", "PS512"],
        ["ec"],
        ["okp"],
        ["rsa", "--kid", "01"],
        ["ec", "--kid", "01"],
        ["okp", "--kid", "01"],
    ],
)
def test_jwk(args):

    res = runner.invoke(jwk, args)
    assert res.exit_code == 0
    k = json.loads(res.output)
    assert "secret" in k
    assert "public" in k


@pytest.mark.parametrize(
    "args",
    [
        ["v1", "public"],
        ["v2", "public"],
        ["v3", "public"],
        ["v4", "public"],
        ["v1", "public", "--kid"],
        ["v2", "public", "--kid"],
        ["v3", "public", "--kid"],
        ["v4", "public", "--kid"],
        ["v1", "public", "--password", "mysecret"],
        ["v2", "public", "--password", "mysecret"],
        ["v3", "public", "--password", "mysecret"],
        ["v4", "public", "--password", "mysecret"],
        ["v1", "local"],
        ["v2", "local"],
        ["v3", "local"],
        ["v4", "local"],
        ["v1", "local", "--kid"],
        ["v2", "local", "--kid"],
        ["v3", "local", "--kid"],
        ["v4", "local", "--kid"],
        ["v1", "local", "--password", "mysecret"],
        ["v2", "local", "--password", "mysecret"],
        ["v3", "local", "--password", "mysecret"],
        ["v4", "local", "--password", "mysecret"],
    ],
)
def test_paserk(args):

    res = runner.invoke(paserk, args)
    assert res.exit_code == 0
    k = json.loads(res.output)
    assert "secret" in k
    if args[1] == "public":
        assert "public" in k


@pytest.mark.parametrize(
    "args, msg",
    [
        (["ec", "--crv", "P-256", "--alg", "ES384"], "Failed to make key: alg must be ES256."),
    ],
)
def test_jwk_with_invalid_args(args, msg):

    res = runner.invoke(jwk, args)
    assert res.exit_code == 0
    assert msg in res.output


@pytest.mark.parametrize(
    "args, msg",
    [
        (["rsa", "--alg", "RSxxx"], "Usage: jwk rsa [OPTIONS]"),
    ],
)
def test_jwk_with_invalid_args_handled_by_click(args, msg):

    res = runner.invoke(jwk, args)
    assert res.exit_code == 2
    assert msg in res.output


@pytest.mark.parametrize(
    "args, msg",
    [
        (["v2", "local", "mysecret"], "Failed to make key: key must be 32 bytes long."),
        (["v1", "public", "--key-size", "256"], "Failed to make key: key_size must be at least 512-bits."),
    ],
)
def test_paserk_with_invalid_args(args, msg):

    res = runner.invoke(paserk, args)
    assert res.exit_code == 0
    assert msg in res.output
