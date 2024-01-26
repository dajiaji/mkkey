Changes
=======

Unreleased
----------

Version 0.7.1
-------------

Released 2024-01-27

- Add Python 3.12 to CI. `#90 <https://github.com/dajiaji/pyseto/pull/90>`__
- Add Python 3.12 to tox.ini. `#80 <https://github.com/dajiaji/pyseto/pull/80>`__
- Fix .readthedocs.yml. `#78 <https://github.com/dajiaji/pyseto/pull/78>`__
- Update dependencies.
    - Bump click-help-colors to 0.9.4. `#77 <https://github.com/dajiaji/pyseto/pull/77>`__
    - Bump shellingham to 1.5.4. `#73 <https://github.com/dajiaji/pyseto/pull/73>`__
- Update dev dependencies.
    - Bump tox to 4.12.1. `#89 <https://github.com/dajiaji/pyseto/pull/89>`__
    - Bump pre-commit/flake8 to 7.0.0. `#87 <https://github.com/dajiaji/mkkey/pull/87>`__
    - Bump pytest to 7.4.4. `#85 <https://github.com/dajiaji/pyseto/pull/85>`__
    - Bump pre-commit/black to 23.12.1. `#84 <https://github.com/dajiaji/mkkey/pull/84>`__
    - Bump pre-commit/isort to 5.12.0. `#84 <https://github.com/dajiaji/mkkey/pull/84>`__
    - Bump pre-commit/mirrors-mypy to 1.8.0. `#84 <https://github.com/dajiaji/mkkey/pull/84>`__
    - Bump actions/{checkout, setup-python} to v4. `#79 <https://github.com/dajiaji/mkkey/pull/79>`__
    - Bump pytest to 7.4.3. `#74 <https://github.com/dajiaji/pyseto/pull/74>`__
    - Bump pre-commit to 3.5.0. `#71 <https://github.com/dajiaji/pyseto/pull/71>`__
    - Bump pre-commit/pre-commit-hooks to 4.5.0. `#70 <https://github.com/dajiaji/mkkey/pull/70>`__

Version 0.7.0
-------------

Released 2023-09-17

- Add SECURITY.md. `#66 <https://github.com/dajiaji/pyseto/pull/66>`__
- Drop support for Python3.7. `#63 <https://github.com/dajiaji/pyseto/pull/63>`__
- Drop support for Python3.6. `#57 <https://github.com/dajiaji/pyseto/pull/57>`__
- Update dependencies.
    - Bump pyseto to 1.7.4. `#64 <https://github.com/dajiaji/pyseto/pull/64>`__
    - Bump click to 8.1.7. `#64 <https://github.com/dajiaji/pyseto/pull/64>`__
    - Bump shellingham to 1.5.3. `#64 <https://github.com/dajiaji/pyseto/pull/64>`__
    - Bump click-help-colors to 0.9.2. `#64 <https://github.com/dajiaji/pyseto/pull/64>`__
- Update dev dependencies.
    - Bump pre-commit/isort to 5.12.0. `#67 <https://github.com/dajiaji/mkkey/pull/67>`__
    - Bump pre-commit/black to 23.7.0. `#65 <https://github.com/dajiaji/mkkey/pull/65>`__
    - Bump pre-commit/blacken-docs to 1.16.0. `#65 <https://github.com/dajiaji/mkkey/pull/65>`__
    - Bump pre-commit/flake8 to 6.1.0. `#65 <https://github.com/dajiaji/mkkey/pull/65>`__
    - Bump pre-commit/pre-commit-hooks to 4.4.0. `#65 <https://github.com/dajiaji/mkkey/pull/65>`__
    - Bump pytest to 7.4.2. `#64 <https://github.com/dajiaji/pyseto/pull/64>`__
    - Bump pytest-cov to 4.1.0. `#64 <https://github.com/dajiaji/pyseto/pull/64>`__
    - Bump tox to 4.11.3. `#64 <https://github.com/dajiaji/pyseto/pull/64>`__
    - Bump pre-commit to 3.4.0. `#64 <https://github.com/dajiaji/pyseto/pull/64>`__
    - Bump PyJWT to 2.8.0. `#64 <https://github.com/dajiaji/pyseto/pull/64>`__

Version 0.6.2
-------------

Released 2022-08-11

- Update dependencies.
    - Bump cryptography to >=36,<38. `#43 <https://github.com/dajiaji/pyseto/pull/43>`__
- Update dev dependencies.
    - Bump pre-commit/flake8 to 5.0.4. `#51 <https://github.com/dajiaji/mkkey/pull/51>`__
    - Bump mypy to 0.971. `#49 <https://github.com/dajiaji/mkkey/pull/49>`__
    - Bump pre-commit/black to 22.6.0. `#48 <https://github.com/dajiaji/mkkey/pull/48>`__
    - Bump tox to 3.25.1. `#58 <https://github.com/dajiaji/mkkey/pull/58>`__
    - Bump pre-commit/pre-commit-hooks to 4.3.0. `#47 <https://github.com/dajiaji/mkkey/pull/47>`__
    - Bump pytest to ^7.0. `#37 <https://github.com/dajiaji/mkkey/pull/37>`__
    - Bump pre-commit/blacken-docs to 1.12.0. `#36 <https://github.com/dajiaji/mkkey/pull/36>`__

Version 0.6.1
-------------

Released 2021-12-12

- Fix tab completion instruction for fish. `#29 <https://github.com/dajiaji/mkkey/pull/29>`__

Version 0.6.0
-------------

Released 2021-12-07

- Add support for PASERK key wrapping with symmetric key. `#25 <https://github.com/dajiaji/mkkey/pull/25>`__

Version 0.5.0
-------------

Released 2021-12-06

- Add support for PASERK password-based key wrapping. `#22 <https://github.com/dajiaji/mkkey/pull/22>`__

Version 0.4.0
-------------

Released 2021-12-05

- Add __main__.py. `#21 <https://github.com/dajiaji/mkkey/pull/21>`__
- Use DER format for "sha256" kid generation method. `#19 <https://github.com/dajiaji/mkkey/pull/19>`__

Version 0.3.0
-------------

Released 2021-12-05

- Add test with external jose library. `#16 <https://github.com/dajiaji/mkkey/pull/16>`__
- Add support for key_ops. `#15 <https://github.com/dajiaji/mkkey/pull/15>`__

Version 0.2.0
-------------

Released 2021-12-04

- Rename option from underscore to hyphen. `#13 <https://github.com/dajiaji/mkkey/pull/13>`__
- Reorder output of paserk. `#12 <https://github.com/dajiaji/mkkey/pull/12>`__
- Refine README and help message. `#9 <https://github.com/dajiaji/mkkey/pull/9>`__

Version 0.1.0
-------------

Released 2021-12-03

- First public release.
