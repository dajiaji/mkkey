# mkkey - An Application-Layer Key Generator supporting JWK and PASERK.

[![PyPI version](https://badge.fury.io/py/mkkey.svg)](https://badge.fury.io/py/mkkey)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/mkkey)
![Github CI](https://github.com/dajiaji/mkkey/actions/workflows/python-package.yml/badge.svg)
[![codecov](https://codecov.io/gh/dajiaji/mkkey/branch/main/graph/badge.svg?token=QN8GXEYEP3)](https://codecov.io/gh/dajiaji/mkkey)

mkkey is a CLI tool for generating following application-layer keys:
- [RFC7517 - JWK (JSON Web Key)](https://datatracker.ietf.org/doc/html/rfc7517)
- [PASERK (Platform-Agnositc Serialized Keys)](https://github.com/paseto-standard/paserk)

In the past, it was necessary to use `openssl` command to create a PEM-formatted key pair,
and then read the PEM-formatted key and convert it into a JWK. However, by using `mkkey`,
you can directly and easily create JWKs and PASERKs that can be used in applications
without generating intermediate data (PEM-formatted keys) as follows:

![mkkey](https://github.com/dajiaji/mkkey/wiki/images/mkkey_header.png)


## Index

- [Installation](#installation)
- [Basic Usage](#basic-usage)
  - [JWK (JSON Web Key)](#jwk-json-web-key)
  - [PASERK (Platform-Agnostic Serialized Keys)](#paserk-platform-agnostic-serialized-keys)
- [Contributing](#contributing)

## Installation

You can install mkkey with pip:

```sh
$ pip install mkkey
```

## Basic Usage


### JWK (JSON Web Key)

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

See help for details:

```sh
$ mkkey jwk --help
```

### PASERK (Platform-Agnostic Serialized Keys)


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

See help for details:

```sh
$ mkkey paserk --help
```

## Contributing

We welcome all kind of contributions, filing issues, suggesting new features or sending PRs.
