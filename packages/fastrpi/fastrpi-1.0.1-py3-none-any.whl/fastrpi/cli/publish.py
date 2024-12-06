from pathlib import Path

import click

import fastrpi
from ..exceptions import (FastrPIManifestError, FastrPIPublishError,
                          FastrPIPublishTestError, FastrPIInstallError)
from ..manifest import Manifest
from ..package import Package


@click.command('network', short_help="Publish a Network package.")
@click.argument('manifest_file', type=click.Path(exists=True, file_okay=True))
def publish_network(manifest_file: click.Path) -> None:
    """
    Publish a Network package to the FastrPI repository.
    """

    if not fastrpi.fastrpi_config.gitlab_token:
        click.echo(f"Gitlab token is not set. Publishing is not possible.")
        raise SystemExit(1)

    manifest_path = Path(click.format_filename(str(manifest_file)))
    if manifest_path.name != fastrpi.fastrpi_config.manifest_name:
        click.echo(f"Manifest must be named '{fastrpi.fastrpi_config.manifest_name}'.")
        raise SystemExit(1)
    try:
        manifest = Manifest.create(manifest_path)
    except FastrPIManifestError as exc:
        click.echo(exc.message)
        raise SystemExit(1) from exc

    if manifest['package_type'] not in ['network']:
        click.echo("Package type does not correspond to a Network type.")
        raise SystemExit(1)

    package = Package.create(manifest)
    try:
        fastrpi.network_package_repo.publish(package)
    except FastrPIPublishTestError as exc:
        click.echo(exc.message)
        click.echo("Publish tests have failed.")
    except FastrPIPublishError as exc:
        click.echo(exc.message)
        click.echo("Publishing has failed.")
    except FastrPIInstallError as exc:
        click.echo(exc.message)
        click.echo("Installation of the packages for publish tests has failed.")
    else:
        click.echo("Publishing successfull.")


@click.command('tool', short_help="Publish a Tool package.")
@click.argument('manifest_file', type=click.Path(exists=True, file_okay=True))
def publish_tool(manifest_file: click.Path) -> None:
    """
    Publish a Tool package to the FastrPI repository.
    """

    if not fastrpi.fastrpi_config.gitlab_token:
        click.echo(f"Gitlab token is not set. Publishing is not possible.")
        raise SystemExit(1)

    manifest_path = Path(click.format_filename(str(manifest_file)))
    if manifest_path.name != fastrpi.fastrpi_config.manifest_name:
        click.echo(f"Manifest must be named '{fastrpi.fastrpi_config.manifest_name}'.")
        raise SystemExit(1)
    try:
        manifest = Manifest.create(manifest_path)
    except FastrPIManifestError as exc:
        click.echo(exc.message)
        raise SystemExit from exc

    if manifest['package_type'] not in ['tool', 'macronode']:
        click.echo("Package type does not correspond to a Tool type.")
        raise SystemExit(1)

    package = Package.create(manifest)
    try:
        fastrpi.tool_package_repo.publish(package)
    except FastrPIPublishTestError as exc:
        click.echo(exc.message)
        click.echo("Publish tests have failed.")
    except FastrPIPublishError as exc:
        click.echo(exc.message)
        click.echo("Publishing has failed.")
    else:
        click.echo("Publishing successfull.")
