# mkkey - An Application-Layer Key Generator supporting JWK and PASERK.

[![PyPI version](https://badge.fury.io/py/mkkey.svg)](https://badge.fury.io/py/mkkey)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/mkkey)
![Github CI](https://github.com/dajiaji/mkkey/actions/workflows/python-package.yml/badge.svg)
[![codecov](https://codecov.io/gh/dajiaji/mkkey/branch/main/graph/badge.svg?token=QN8GXEYEP3)](https://codecov.io/gh/dajiaji/mkkey)

mkkey is a CLI tool for generating following application-layer keys:
- [RFC7517 - JWK (JSON Web Key)](https://datatracker.ietf.org/doc/html/rfc7517)
- [PASERK (Platform-Agnositc Serialized Keys)](https://github.com/paseto-standard/paserk)

Until now, in order to create a JWK, you had to create a PEM-formatted key pair using a command
such as `openssl`, and then load it and convert it into a JWK. With `mkkey`, you can
directly and easily create JWKs and PASERKs that can be used in applications as shown below,
without generating intermediate keys (PEM-formatted keys):

![mkkey](https://github.com/dajiaji/mkkey/wiki/images/mkkey_header.png)

# Index

- [Installation](#installation)
- [Basic Usage](#basic-usage)
  - [JWK (JSON Web Key)](#jwk-json-web-key)
      - [Generate a simple (default) JWK](#generate-a-simple-default-jwk)
      - [Generate a JWK with specifying curve](#generate-a-jwk-with-specifying-curve)
      - [Generate a JWK with optional attributes](#generate-a-jwk-with-optional-attributes)
      - [Generate a JWK with kid generation method](#generate-a-jwk-with-kid-generation-method)
  - [PASERK (Platform-Agnostic Serialized Keys)](#paserk-platform-agnostic-serialized-keys)
      - [Generate a PASERK](#generate-a-paserk)
      - [Generate a PASERK along with a PASERK ID](#generate-a-paserk-along-with-a-paserk-id)
- [kid generation methods for JWK](#kid-generation-methods-for-jwk)
- [Contributing](#contributing)

# Installation

You can install mkkey with pip:

```sh
$ pip install mkkey
```

If the shell you are using is `bash`, `zsh` or `fish`, you can activate tab completion
by following the steps below:

1. Run `mkkey --install`.
2. Follow the steps described in the output of `mkkey --install`.

# Basic Usage

## JWK (JSON Web Key)

JWKs can be generated using the `mkkey jwk` command.

Typical use cases are shown in this section but for details, see help:

```sh
$ mkkey jwk --help
```

### Generate a simple (default) JWK

The simplest way to use `mkkey jwt` is as follows. Simply specify a key type (in this case, `ec`).
Now you will get the minimum JWK you need.

```sh
$ mkkey jwk ec
{
    "public": {
        "jwk": {
            "kty": "EC",
            "crv": "P-256",
            "x": "Ti-mNoi-uQFYBVNkH6BSmuTAd8WL8kyEVJufZYv3mG8",
            "y": "ANwoZQFI_teNrltM0s9LPjWli0_zyYvvv8cEZWKx1CQ"
        }
    },
    "secret": {
        "jwk": {
            "kty": "EC",
            "crv": "P-256",
            "x": "Ti-mNoi-uQFYBVNkH6BSmuTAd8WL8kyEVJufZYv3mG8",
            "y": "ANwoZQFI_teNrltM0s9LPjWli0_zyYvvv8cEZWKx1CQ",
            "d": "l9Pbq0BmCsOzdapBtSxVpRiHhDTK5-ATteA0nMKzvFU"
        }
    }
}
```

In addtion to `ec`, `rsa` and `okp` (Octet Key Pair) can be used as key types:

```sh
$ mkkey jwk rsa
$ mkkey jwk okp
```

### Generate a JWK with specifying curve

If you want to use a curve other than `P-256`, use the `--crv` option:

```sh
$ mkkey jwk ec --crv P-384
```

### Generate a JWK with optional attributes

If you want to include `kid`, `alg` and `use` in the JWK, use the `--kid`, `--alg` and `--use` respectively:

```sh
$ mkkey jwk ec --kid 01 --alg ES256 --use sig
{
    "public": {
        "jwk": {
            "kid": "01",
            "kty": "EC",
            "crv": "P-256",
            "alg": "ES256",
            "use": "sig",
            "x": "qg-3SA7jNvG7DPF8ajuRR69d5LoBz-I8Xg4ze1kjdHs",
            "y": "JctPLnWOeyJM3apWxyEX3bHDo97kel4gdI8x0FlTwHc"
        }
    },
    "secret": {
        "jwk": {
            "kid": "01",
            "kty": "EC",
            "crv": "P-256",
            "alg": "ES256",
            "use": "sig",
            "x": "qg-3SA7jNvG7DPF8ajuRR69d5LoBz-I8Xg4ze1kjdHs",
            "y": "JctPLnWOeyJM3apWxyEX3bHDo97kel4gdI8x0FlTwHc",
            "d": "GZ9ihMNwYYbglWHV8vau-W5gaZal5ajBb_NiY7Ci7Uk"
        }
    }
}
```

### Generate a JWK with kid generation method

`kid` can also be generated automatically. In this case, use `--kid-type` to specify the generation method.
For now, only `sha256` (see [kid generation methods for JWK](#kid-generation-methods-for-jwk)) is available.
You can adjust the size of the auto-generated kid by using `--kid-size` as well:

```sh
$ mkkey jwk ec --kid-type sha256 --kid-size 16
{
    "public": {
        "jwk": {
            "kid": "ozh_CYlRd3A1f2RLlA3Y5w",
            "kty": "EC",
            "crv": "P-256",
            "x": "hDuMnnmlnFAKMsn-qP37XsKchg6K0bXPhsFgmWOpnVw",
            "y": "_oQgP8b8V0hC_H73gIVBaMylAoTOA4mwM57Y2hC2xIk"
        }
    },
    "secret": {
        "jwk": {
            "kid": "ozh_CYlRd3A1f2RLlA3Y5w",
            "kty": "EC",
            "crv": "P-256",
            "x": "hDuMnnmlnFAKMsn-qP37XsKchg6K0bXPhsFgmWOpnVw",
            "y": "_oQgP8b8V0hC_H73gIVBaMylAoTOA4mwM57Y2hC2xIk",
            "d": "1b0lNEiyV_C8U0fGXDczfwTrKnHpWwjt_OU0H-MLJvs"
        }
    }
}
```

## PASERK (Platform-Agnostic Serialized Keys)

PASERKs can be generated using the `mkkey paserk` command.

Typical use cases are shown in this section but for details, see help:

```sh
$ mkkey paserk --help
```

### Generate a PASERK

PASERKs can be generated using the `mkkey paserk` command with a target PASETO version
and a purpose (in this case, `v4` and `public` respectively).

```sh
$ mkkey paserk v4 public
{
    "public": {
        "paserk": "k4.public.2BWUTPg5pmXZ3EVrOBv9I4I_F8Afj0TJ21HkaPT926M"
    },
    "secret": {
        "paserk": "k4.secret.fKIawV2PPVpEONDcEH3_p1dc4OEYlTncmMa8gvwMVy_YFZRM-DmmZdncRWs4G_0jgj8XwB-PRMnbUeRo9P3bow"
    }
}

```

### Generate a PASERK along with a PASERK ID

If you want to generate a PASERK ID (`kid`) along with a PASERK, use the `--kid` option:

```sh
$ mkkey paserk v4 public --kid
{
    "public": {
        "kid": "k4.pid.B7i9vMzTQv32mDV9JKjyRy5Iu4eyuufb_RjXwQeZiGrh",
        "paserk": "k4.public.Qo7ipKpEa2RxCqmVXSpHdRbWMGtg9QsesMUbLQfU_Pw"
    },
    "secret": {
        "kid": "k4.sid.v1091k4VuZOEKfIO5hLByGwK-RP6dFhfaltURc4CFkUd",
        "paserk": "k4.secret.0h5Q2HDR8PbFMZhN8z7iXbbCyn5-bRQdNPRYIglvnWdCjuKkqkRrZHEKqZVdKkd1FtYwa2D1Cx6wxRstB9T8_A"
    }
}
```

## kid generation methods for JWK

Following kid generation methods are available that can be specified as `--kid-type` option:

- `sha256`: Use a SHA256 hash value of PEM-formatted public key bytes as a kid value. The PEM format must be subject public key info which starts with `-----BEGIN PUBLIC KEY-----`.
- `none`: Do not generate kid [default].

## Contributing

We welcome all kind of contributions, filing issues, suggesting new features or sending PRs.
