from pathlib import Path
from typing import List

import click

from ..create.packagecreator import ToolPackageCreator, NetworkPackageCreator, MacroNodePackageCreator
from ..exceptions import FastrPICreateError


@click.command('tool')
@click.argument('tool_files', nargs=-1, required=True,
                type=click.Path(exists=True, file_okay=True))
def create_tool(tool_files: List[click.Path]):
    """ Create a FastrPI Tool package based on a (collection of) Fastr Tool definition(s)."""
    tool_files_path = [Path(click.format_filename(str(tool_file))) for tool_file in tool_files]
    package_creator = ToolPackageCreator(tool_files_path)
    try:
        package_creator.create()
    except FastrPICreateError:
        click.echo("Package creation cancelled by user.")
    else:
        click.echo("Tool package creation complete.")


@click.command('network')
@click.argument('network_file', type=click.Path(exists=True, file_okay=True))
def create_network(network_file: click.Path):
    """ Create a FastrPI Network package based on a Fastr Network."""
    network_file_path = Path(click.format_filename(str(network_file)))
    package_creator = NetworkPackageCreator(network_file_path)
    try:
        package_creator.create()
    except FastrPICreateError:
        click.echo("Package creation cancelled by user.")
    else:
        click.echo("Network package creation complete.")


@click.command('macronode')
@click.option('-n', '--name', required=True, type=str, nargs=1, help='Name of the Network to use in a MacroNode.')
@click.option('-v', '--version', required=True, type=str, nargs=1, help='Version of the Network to use in a MacroNode.')
def create_macronode(name: str, version: str):
    """ Create a FastrPI MacroNode package for a Fastr Network package in the FastrPI repository."""
    package_creator = MacroNodePackageCreator(name, version)
    package_creator.create()
    click.echo("MacroNode package creation complete.")
