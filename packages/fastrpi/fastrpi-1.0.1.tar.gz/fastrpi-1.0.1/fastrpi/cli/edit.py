import os
from pathlib import Path

import click

import fastrpi
from ..exceptions import FastrPINotInstalled
from ..packageinfo import PackageInfo


@click.command('network', short_help="Edit an installed Network.")
@click.argument('name', type=str)
@click.option('-v', '--version', required=True, type=str,
              help="Version of the Network package.")
@click.option('-s', '--sourcesink', is_flag=True,
              help="Flag to only copy the Source-Sink file.")
def edit_network(name: str, version: str, sourcesink: bool) -> None:
    """ Edit an installed Network.

    By running `fastrpi edit network network_name -v 1.0.0`, the package files for Network package `network_name`,
    version `1.0.0` will be copied to the folder `network_name-v1.0.0` in the current directory.
    """
    directory = Path(os.getcwd())
    try:
        package = fastrpi.network_install_record.load_package(
            PackageInfo(name=name, package_version=version)
        )
        network_dir = directory / package.tag
        if not network_dir.is_dir():
            if sourcesink:
                package.copy_source_sink(network_dir)
            else:
                package.copy_files(network_dir)
        else:
            click.echo('Network directory already exist in current folder.')
    except FastrPINotInstalled as exc:
        click.echo(exc.message)
    else:
        if sourcesink:
            click.echo(f"Source-Sink file for Network package {package.info} copied and ready for editing.")
        else:
            click.echo(f"Network package {package.info} copied and ready for editing.")


@click.command('tool', short_help="Edit an installed Tool.")
@click.argument('name', type=str)
@click.option('-v', '--version', required=True, type=str,
              help="Version of the Tool package.")
@click.option('-p', '--package_version', required=True, type=str,
              help="Package version of the Tool package.")
def edit_tool(name: str, version: str, package_version: str) -> None:
    """ Edit an installed Tool.

    By running `fastrpi edit tool tool_name -v 1.0 -p 1.0`, the package files for Tool package `tool_name`,
    version `1.0`, package version `1.0`, will be copied to the nested folders `tools/tool_name/1.0/1.0` in the current
    directory.
    """
    directory = Path(os.getcwd())
    try:
        package = fastrpi.tool_install_record.load_package(
            PackageInfo(name=name, package_version=package_version, version=version)
        )
        tool_dir = directory / 'tools' / package.name / package.version / package.package_version
        if not tool_dir.is_dir():
            package.copy_files(tool_dir)
        else:
            click.echo('Tool directory already exist in current folder.')
    except FastrPINotInstalled as exc:
        click.echo(exc.message)
    else:
        click.echo(f"Tool package {package.info} copied and ready for editing.")
