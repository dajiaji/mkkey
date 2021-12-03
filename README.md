# mkkey - An Application-Layer Key Generator supporting JWK and PASERK.

[![PyPI version](https://badge.fury.io/py/mkkey.svg)](https://badge.fury.io/py/mkkey)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/mkkey)
![Github CI](https://github.com/dajiaji/mkkey/actions/workflows/python-package.yml/badge.svg)
[![codecov](https://codecov.io/gh/dajiaji/mkkey/branch/main/graph/badge.svg?token=QN8GXEYEP3)](https://codecov.io/gh/dajiaji/mkkey)

mkkey is a CLI tool for generating following application-layer keys:
- [JWK (JSON Web Key) - RFC7517](https://datatracker.ietf.org/doc/html/rfc7517)
- [PASERK (Platform-Agnositc Serialized Keys)](https://github.com/paseto-standard/paserk)


You can install mkkey with pip:

```sh
$ pip install mkkey
```

And then, you can use it as follows.


For JWK:

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

For PASERK:

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
$ mkkey --help
$ mkkey jwk --help
$ mkkey paserk --help
```
