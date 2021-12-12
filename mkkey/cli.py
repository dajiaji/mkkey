import json

import click
from click_help_colors import HelpColorsGroup

from .completion import InstallCompletionError, install
from .jwk import generate_jwk
from .paserk import generate_local_paserk, generate_public_paserk


def _show_result(res: dict):
    click.secho(json.dumps(res, indent=4), fg="cyan")
    return


def _show_error(err: Exception):
    click.secho(f"Failed to make key: {err}", err=True, fg="red")
    return


def _jwk(
    kty: str,
    crv: str = "",
    alg: str = "",
    use: str = "",
    key_ops: bool = False,
    kid: str = "",
    kid_type: str = "none",
    kid_size: int = 0,
    output_format: str = "json",
    rsa_key_size: int = 2048,
):
    try:
        _show_result(
            generate_jwk(
                kty,
                crv=crv,
                alg=alg,
                use=use,
                key_ops=key_ops,
                kid=kid,
                kid_type=kid_type,
                kid_size=kid_size,
                output_format=output_format,
            )
        )
    except Exception as err:
        _show_error(err)
    return


def _paserk_public(version: int, kid: bool, password: str, wrapping_key: str, rsa_key_size: int = 2048):
    try:
        _show_result(generate_public_paserk(version, kid, password, wrapping_key, rsa_key_size=rsa_key_size))
    except Exception as err:
        _show_error(err)


def _paserk_local(version: int, key_material: str, kid: bool, password: str, wrapping_key: str = ""):
    try:
        _show_result(generate_local_paserk(version, key_material, kid, password, wrapping_key))
    except Exception as err:
        _show_error(err)


def _display_instruction(shell: str, path: str):
    click.echo(f"{shell} completion installed in ", nl=False)
    click.secho(f"{path}", fg="cyan", bold=True, nl=False)
    click.echo(".", nl=True)
    click.echo("", nl=True)

    if shell == "bash" or shell == "zsh":
        click.echo("Run ", nl=False)
        click.secho(f". {path}", fg="cyan", bold=True, nl=False)
        click.echo(" to activate the completion.", nl=True)

        click.echo("Run ", nl=False)
        click.secho(f'echo -e ". {path}" >> ~/.{shell}rc', fg="cyan", bold=True, nl=False)
        click.echo(" to activate the completion permanently.", nl=True)
        click.echo("", nl=True)
    if shell == "fish":
        click.echo("If you see an error log, run ", nl=False)
        click.secho("mkdir -p ~/.config/fish/completions", fg="cyan", bold=True, nl=True)
        click.echo("and then run ", nl=False)
        click.secho("mkkey --install ", fg="cyan", bold=True, nl=False)
        click.echo("again.", nl=True)
    return


def install_callback(ctx, attr, value):
    if not value or ctx.resilient_parsing:
        return value

    try:
        shell, path = install()
    except InstallCompletionError as err:
        click.secho(
            f"ERROR: {err.shell} is not supported. bash, zsh, and fish are only supported.",
            fg="red",
            nl=True,
        )
        exit(1)

    _display_instruction(shell, path)
    exit(0)


@click.group(
    cls=HelpColorsGroup,
    help_headers_color="green",
    help_options_color="cyan",
)
@click.version_option()
@click.option(
    "--install",
    is_flag=True,
    callback=install_callback,
    expose_value=False,
    help="Install completion for the current shell.",
)
def cli():
    """
    A Generic Application-Layer Key Generator supporting JWK and PASERK.
    """


@cli.group("jwk")
def jwk():
    """Generate JWK (JSON Web Key) for JWT/JOSE."""


@jwk.command("rsa")
@click.option(
    "--alg",
    type=click.Choice(["RS256", "RS384", "RS512", "PS256", "PS384", "PS512"]),
    default="RS256",
    show_default=True,
    required=True,
    help="Set algorithm ('alg').",
)
@click.option(
    "--use",
    type=click.Choice(["sig"]),
    required=False,
    help="Set public key usage ('use').",
)
@click.option(
    "--key-ops/--no-key-ops",
    default=False,
    required=False,
    help="Set key operations ('key_ops') or not.",
)
@click.option(
    "--kid",
    type=str,
    default="",
    required=False,
    help="Set key id ('kid').",
)
@click.option(
    "--kid-type",
    type=click.Choice(["none", "sha256"]),
    default="none",
    required=False,
    help="Set auto key id generation method when '--kid' is not used.",
)
@click.option(
    "--kid-size",
    type=int,
    default=0,
    required=False,
    help="Set auto-generated key id size for truncation.",
)
@click.option(
    "-o",
    "--output_format",
    type=click.Choice(["json", "jwks"]),
    default="json",
    required=False,
    help="Set output format.",
)
@click.option(
    "--key-size",
    type=int,
    default=2048,
    show_default=True,
    required=False,
    help="Set the length of modulus in bits for RSA key (MUST be >=512).",
)
def jwk_rsa(
    alg: str,
    use: str = "",
    key_ops: bool = False,
    kid: str = "",
    kid_type: str = "none",
    kid_size: int = 0,
    output_format: str = "json",
    key_size: int = 2048,
):

    """Generate RSA JWK."""
    _jwk("RSA", "", alg, use, key_ops, kid, kid_type, kid_size, output_format, key_size)
    return


@jwk.command("ec")
@click.option(
    "--crv",
    type=click.Choice(["P-256", "P-384", "P-521", "secp256k1"]),
    default="P-256",
    show_default=True,
    required=True,
    help="Set curve ('crv').",
)
@click.option(
    "--alg",
    type=click.Choice(["ES256", "ES384", "ES512", "ES256K"]),
    required=False,
    help="Set algorithm ('alg').",
)
@click.option(
    "--use",
    type=click.Choice(["sig"]),
    required=False,
    help="Set public key usage ('use').",
)
@click.option(
    "--key-ops/--no-key-ops",
    default=False,
    required=False,
    help="Set key operations ('key_ops') or not.",
)
@click.option(
    "--kid",
    type=str,
    default="",
    required=False,
    help="Set key id ('kid').",
)
@click.option(
    "--kid-type",
    type=click.Choice(["none", "sha256"]),
    default="none",
    required=False,
    help="Set auto key id generation method when '--kid' is not used.",
)
@click.option(
    "--kid-size",
    type=int,
    default=0,
    required=False,
    help="Set auto-generated key id size for truncation.",
)
@click.option(
    "-o",
    "--output_format",
    type=click.Choice(["json", "jwks"]),
    default="json",
    required=False,
    help="Set output format.",
)
def jwk_ec(
    crv: str,
    alg: str = "",
    use: str = "",
    key_ops: bool = False,
    kid: str = "",
    kid_type: str = "none",
    kid_size: int = 0,
    output_format: str = "json",
):

    """Generate EC JWK."""
    _jwk("EC", crv, alg, use, key_ops, kid, kid_type, kid_size, output_format, 0)
    return


@jwk.command("okp")
@click.option(
    "--crv",
    type=click.Choice(["Ed25519", "Ed448"]),
    default="Ed25519",
    show_default=True,
    required=True,
    help="Set curve ('crv').",
)
@click.option(
    "--alg",
    type=click.Choice(["EdDSA"]),
    required=False,
    help="Set algorithm ('alg').",
)
@click.option(
    "--use",
    type=click.Choice(["sig"]),
    required=False,
    help="Set public key usage ('use').",
)
@click.option(
    "--key-ops/--no-key-ops",
    default=False,
    required=False,
    help="Set key operations ('key_ops') or not.",
)
@click.option(
    "--kid",
    type=str,
    default="",
    required=False,
    help="Set key id ('kid').",
)
@click.option(
    "--kid-type",
    type=click.Choice(["none", "sha256"]),
    default="none",
    required=False,
    help="Set auto key id generation method when '--kid' is not used.",
)
@click.option(
    "--kid-size",
    type=int,
    default=0,
    required=False,
    help="Set auto-generated key id size for truncation.",
)
@click.option(
    "-o",
    "--output_format",
    type=click.Choice(["json", "jwks"]),
    default="json",
    required=False,
    help="Set output format.",
)
def jwk_okp(
    crv: str,
    alg: str = "",
    use: str = "",
    key_ops: bool = False,
    kid: str = "",
    kid_type: str = "none",
    kid_size: int = 0,
    output_format: str = "json",
):

    """Generate OKP JWK."""
    _jwk("OKP", crv, alg, use, key_ops, kid, kid_type, kid_size, output_format, 0)
    return


@cli.group("paserk")
def paserk():
    """Generate PASERK (Platform-Agnositc SERialized Keys) for PASETO."""


@paserk.group("v4")
def v4():
    """Generate PASERK for PASETO v4."""


@v4.command("public")
@click.option(
    "--kid/--no-kid",
    default=False,
    required=False,
    help="Set PASERK ID ('kid') or not.",
)
@click.option(
    "--password",
    type=str,
    default="",
    required=False,
    help="Set password for key wrapping.",
)
@click.option(
    "--wrapping-key",
    type=str,
    default="",
    required=False,
    help="Set another symmetric key for key wrapping.",
)
def paserk_v4_public(kid: bool, password: str, wrapping_key: str):
    """Generate v4.public PASERK for Asymmetric-key digital signatures."""
    _paserk_public(4, kid, password, wrapping_key)
    return


@v4.command("local")
@click.argument(
    "key_material",
    type=str,
    default="",
    required=False,
)
@click.option(
    "--kid/--no-kid",
    default=False,
    required=False,
    help="Set PASERK ID ('kid') or not.",
)
@click.option(
    "--password",
    type=str,
    default="",
    required=False,
    help="Set password for key wrapping.",
)
@click.option(
    "--wrapping-key",
    type=str,
    default="",
    required=False,
    help="Set another symmetric key for key wrapping.",
)
def paserk_v4_local(key_material: str, kid: bool, password: str, wrapping_key: str):
    """Generate v4.local PASERK for Symmetric-key encryption (AEAD)."""
    _paserk_local(4, key_material, kid, password)
    return


@paserk.group("v3")
def v3():
    """Generate PASERK for PASETO v3."""


@v3.command("public")
@click.option(
    "--kid/--no-kid",
    default=False,
    required=False,
    help="Set PASERK ID ('kid') or not.",
)
@click.option(
    "--password",
    type=str,
    default="",
    required=False,
    help="Set password for key wrapping.",
)
@click.option(
    "--wrapping-key",
    type=str,
    default="",
    required=False,
    help="Set another symmetric key for key wrapping.",
)
def paserk_v3_public(kid: bool, password: str, wrapping_key: str):
    """Generate v3.public PASERK for Asymmetric-key digital signatures."""
    _paserk_public(3, kid, password, wrapping_key)
    return


@v3.command("local")
@click.argument(
    "key_material",
    type=str,
    default="",
    required=False,
)
@click.option(
    "--kid/--no-kid",
    default=False,
    required=False,
    help="Set PASERK ID ('kid') or not.",
)
@click.option(
    "--password",
    type=str,
    default="",
    required=False,
    help="Set password for key wrapping.",
)
@click.option(
    "--wrapping-key",
    type=str,
    default="",
    required=False,
    help="Set another symmetric key for key wrapping.",
)
def paserk_v3_local(key_material: str, kid: bool, password: str, wrapping_key: str):
    """Generate v3.local PASERK for Symmetric-key encryption (AEAD)."""
    _paserk_local(3, key_material, kid, password, wrapping_key)
    return


@paserk.group("v2")
def v2():
    """Generate PASERK for PASETO v2."""


@v2.command("public")
@click.option(
    "--kid/--no-kid",
    default=False,
    required=False,
    help="Set PASERK ID ('kid') or not.",
)
@click.option(
    "--password",
    type=str,
    default="",
    required=False,
    help="Set password for key wrapping.",
)
@click.option(
    "--wrapping-key",
    type=str,
    default="",
    required=False,
    help="Set another symmetric key for key wrapping.",
)
def paserk_v2_public(kid: bool, password: str, wrapping_key: str):
    """Generate v2.public PASERK for Asymmetric-key digital signatures."""
    _paserk_public(2, kid, password, wrapping_key)
    return


@v2.command("local")
@click.argument(
    "key_material",
    type=str,
    default="",
    required=False,
)
@click.option(
    "--kid/--no-kid",
    default=False,
    required=False,
    help="Set PASERK ID ('kid') or not.",
)
@click.option(
    "--password",
    type=str,
    default="",
    required=False,
    help="Set password for key wrapping.",
)
@click.option(
    "--wrapping-key",
    type=str,
    default="",
    required=False,
    help="Set another symmetric key for key wrapping.",
)
def paserk_v2_local(key_material: str, kid: bool, password: str, wrapping_key: str):
    """Generate v2.local PASERK for Symmetric-key encryption (AEAD)."""
    _paserk_local(2, key_material, kid, password, wrapping_key)
    return


@paserk.group("v1")
def v1():
    """Generate PASERK for PASETO v1."""


@v1.command("public")
@click.option(
    "--kid/--no-kid",
    default=False,
    required=False,
    help="Set PASERK ID ('kid') or not.",
)
@click.option(
    "--password",
    type=str,
    default="",
    required=False,
    help="Set password for key wrapping.",
)
@click.option(
    "--wrapping-key",
    type=str,
    default="",
    required=False,
    help="Set another symmetric key for key wrapping.",
)
@click.option(
    "--key-size",
    type=int,
    default=2048,
    show_default=True,
    required=False,
    help="Set the length of modulus in bits for RSA key (MUST be >=512).",
)
def paserk_v1_public(kid: bool, password: str, wrapping_key: str, key_size: int):
    """Generate v1.public PASERK for Asymmetric-key digital signatures."""
    _paserk_public(1, kid, password, wrapping_key, rsa_key_size=key_size)
    return


@v1.command("local")
@click.argument(
    "key_material",
    type=str,
    default="",
    required=False,
)
@click.option(
    "--kid/--no-kid",
    default=False,
    required=False,
    help="Generate key id or not.",
)
@click.option(
    "--password",
    type=str,
    default="",
    required=False,
    help="Set password for key wrapping.",
)
@click.option(
    "--wrapping-key",
    type=str,
    default="",
    required=False,
    help="Set another symmetric key for key wrapping.",
)
def paserk_v1_local(key_material: str, kid: bool, password: str, wrapping_key: str):
    """Generate v1.local PASERK for Symmetric-key encryption (AEAD)."""
    _paserk_local(1, key_material, kid, password, wrapping_key)
    return
