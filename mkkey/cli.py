import json

import click
from click_help_colors import HelpColorsGroup

from .completion import InstallCompletionError, install
from .jwk import generate_jwk
from .paserk import generate_local_paserk, generate_public_paserk


def show_result(res: dict):
    click.secho(json.dumps(res, indent=4), fg="cyan")
    return


def show_error(err: Exception):
    click.secho(f"Failed to make key: {err}", err=True, fg="red")
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

    click.echo(f"{shell} completion installed in ", nl=False)
    click.secho(f"{path}", fg="green", bold=True, nl=False)
    click.echo(".", nl=True)
    click.echo("", nl=True)

    if shell == "bash" or shell == "zsh":
        click.echo("Run ", nl=False)
        click.secho(f". {path}", fg="green", bold=True, nl=False)
        click.echo(" to activate the completion.", nl=True)

        click.echo("Run ", nl=False)
        click.secho(
            f'echo -e ". {path}" >> ~/.{shell}rc', fg="green", bold=True, nl=False
        )
        click.echo(" to activate the completion permanently.", nl=True)
        click.echo("", nl=True)
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
    pass


@cli.group("jwk")
def jwk():
    """Generate JWK (JSON Web Key) for JWT/JOSE."""


@jwk.command("rsa")
@click.option(
    "--alg",
    type=click.Choice(["RS256", "RS384", "RS512", "PS256", "PS384", "PS512"]),
    default="RS256",
    required=True,
    help="Algorithm.",
)
@click.option(
    "--use",
    type=click.Choice(["sig"]),
    required=False,
    help="Key usage.",
)
@click.option(
    "--kid_policy",
    type=click.Choice(["none", "sha256"]),
    default="none",
    required=False,
    help="Key id generation policy.",
)
@click.option(
    "--kid_size",
    type=int,
    default=32,
    required=False,
    help="Key id size.",
)
@click.option(
    "--kid",
    type=str,
    default="",
    required=False,
    help="Key id for manural setting.",
)
@click.option(
    "--key_size",
    type=int,
    default=2048,
    required=False,
    help="Key size (MUST be >=512).",
)
def jwk_rsa(
    alg: str,
    use: str = "",
    kid_policy: str = "none",
    kid_size: int = 32,
    kid: str = "",
    key_size: int = 2048,
):

    """Generate RSA JWK."""
    try:
        show_result(
            generate_jwk(
                "rsa",
                alg=alg,
                use=use,
                kid_policy=kid_policy,
                kid_size=kid_size,
                kid=kid,
                rsa_key_size=key_size,
            )
        )
    except Exception as err:
        show_error(err)
    return


@jwk.command("ec")
@click.option(
    "--crv",
    type=click.Choice(["P-256", "P-384", "P-521", "secp256k1"]),
    default="P-384",
    required=True,
    help="Curve.",
)
@click.option(
    "--alg",
    type=click.Choice(["EdDSA"]),
    required=False,
    help="Algorithm.",
)
@click.option(
    "--use",
    type=click.Choice(["sig"]),
    required=False,
    help="Key usage.",
)
@click.option(
    "--kid_policy",
    type=click.Choice(["none", "sha256"]),
    default="none",
    required=False,
    help="Key id generation policy.",
)
@click.option(
    "--kid_size",
    type=int,
    default=32,
    required=False,
    help="Key id size.",
)
@click.option(
    "--kid",
    type=str,
    default="",
    required=False,
    help="Key id for manural setting.",
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
    kid_policy: str = "none",
    kid_size: int = 32,
    kid: str = "",
    output_format: str = "json",
):

    """Generate EC JWK."""
    try:
        show_result(
            generate_jwk(
                "ec",
                crv=crv,
                alg=alg,
                use=use,
                kid_policy=kid_policy,
                kid_size=kid_size,
                kid=kid,
                output_format=output_format,
            )
        )
    except Exception as err:
        show_error(err)
    return


@jwk.command("okp")
@click.option(
    "--crv",
    type=click.Choice(["Ed25519", "Ed448"]),
    default="Ed25519",
    required=True,
    help="Curve.",
)
@click.option(
    "--alg",
    type=click.Choice(["EdDSA"]),
    required=False,
    help="Algorithm.",
)
@click.option(
    "--use",
    type=click.Choice(["sig"]),
    required=False,
    help="Key usage.",
)
@click.option(
    "--kid_policy",
    type=click.Choice(["none", "sha256"]),
    default="none",
    required=False,
    help="Key id generation policy.",
)
@click.option(
    "--kid_size",
    type=int,
    default=32,
    required=False,
    help="Key id size.",
)
@click.option(
    "--kid",
    type=str,
    default="",
    required=False,
    help="Key id for manural setting.",
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
    kid_policy: str = "none",
    kid_size: int = 32,
    kid: str = "",
    output_format: str = "json",
):

    """Generate OKP JWK."""
    try:
        show_result(
            generate_jwk(
                "okp",
                crv=crv,
                alg=alg,
                use=use,
                kid_policy=kid_policy,
                kid_size=kid_size,
                kid=kid,
                output_format=output_format,
            )
        )
    except Exception as err:
        show_error(err)
    return


@cli.group("paserk")
def paserk():
    """Generate PASERK (Platform-Agnositc SERialized Keys) for PASETO."""


@paserk.group("v4")
def v4():
    """Generate PASERK for PASETO v4."""
    pass


@v4.command("public")
@click.option(
    "--kid/--no-kid",
    default=False,
    required=False,
    help="Generate key id or not.",
)
def paserk_v4_public(kid: bool):
    try:
        show_result(generate_public_paserk(4, kid))
    except Exception as err:
        show_error(err)
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
    help="Generate key id or not.",
)
def paserk_v4_local(key_material: str, kid: bool = True):
    try:
        show_result(generate_local_paserk(4, key_material, kid))
    except Exception as err:
        show_error(err)
    return


@paserk.group("v3")
def v3():
    """Generate PASERK for PASETO v3."""
    pass


@v3.command("public")
@click.option(
    "--kid/--no-kid",
    default=False,
    required=False,
    help="Generate key id or not.",
)
def paserk_v3_public(kid: bool):
    try:
        show_result(generate_public_paserk(3, kid))
    except Exception as err:
        show_error(err)
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
    help="Generate key id or not.",
)
def paserk_v3_local(key_material: str, kid: bool = True):
    try:
        show_result(generate_local_paserk(3, key_material, kid))
    except Exception as err:
        show_error(err)
    return


@paserk.group("v2")
def v2():
    """Generate PASERK for PASETO v2."""
    pass


@v2.command("public")
@click.option(
    "--kid/--no-kid",
    default=False,
    required=False,
    help="Generate key id or not.",
)
def paserk_v2_public(kid: bool):
    try:
        show_result(generate_public_paserk(2, kid))
    except Exception as err:
        show_error(err)
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
    help="Generate key id or not.",
)
def paserk_v2_local(key_material: str, kid: bool = True):
    try:
        show_result(generate_local_paserk(2, key_material, kid))
    except Exception as err:
        show_error(err)
    return


@paserk.group("v1")
def v1():
    """Generate PASERK for PASETO v1."""
    pass


@v1.command("public")
@click.option(
    "--kid/--no-kid",
    default=False,
    required=False,
    help="Generate key id or not.",
)
@click.option(
    "--key_size",
    type=int,
    default=2048,
    required=False,
    help="Key size (MUST be >=512).",
)
def paserk_v1(kid: bool, key_size: int):
    try:
        show_result(generate_public_paserk(1, kid, rsa_key_size=key_size))
    except Exception as err:
        show_error(err)
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
def paserk_v1_local(key_material: str, kid: bool = True):
    try:
        show_result(generate_local_paserk(1, key_material, kid))
    except Exception as err:
        show_error(err)
    return
