import click

import fastrpi
from ..exceptions import FastrPIAlreadyInstalled, FastrPIInstallError
from ..package import PackageInfo


@click.command('network', short_help="Install a network.")
@click.argument('name', type=str)
@click.option('-v', '--version', type=str,
              help="Version of the Network package.", required=True)
def install_network(name: str, version: str) -> None:
    """
    Install a Network and the required Tools.
    """
    package_info = PackageInfo(name=name, package_version=version)
    try:
        fastrpi.network_package_repo.install(package_info)
    except FastrPIAlreadyInstalled as exc:
        click.echo(exc.message)
    except FastrPIInstallError:
        click.echo(f"Network {package_info} could not be installed.")
    except Exception as exc:
        click.echo(f"Unknown Exception raised when installing network {package_info}.")
        click.echo(exc)
    else:
        click.echo(f"Network {package_info} installed successfully.")


@click.command('tool', short_help="Install a Tool package.")
@click.argument('name', type=str)
@click.option('-v', '--version', required=True, type=str,
              help="Version of the Tool package.")
@click.option('-p', '--package_version', required=True, type=str,
              help="Package version of the Tool package.")
def install_tool(name: str, version: str, package_version: str) -> None:
    """
    Install a Tool and the corresponding container.
    """
    package_info = PackageInfo(name=name, version=version, package_version=package_version)
    try:
        fastrpi.tool_package_repo.install(package_info)
    except FastrPIAlreadyInstalled as exc:
        click.echo(exc.message)
    except FastrPIInstallError:
        click.echo(f"Tool {package_info} could not be installed.")
    except Exception as exc:
        click.echo(f"Unknown Exception raised when installing tool {package_info}.")
        click.echo(exc)
    else:
        click.echo(f"Tool {package_info} installed successfully.")
