import click
import questionary
from tabulate import tabulate

from .. import fastrpi_config
from ..packageinfo import PackageInfo
from ..server import ToolMetadataCollector, NetworkMetadataCollector


@click.command('tool')
@click.argument('name', type=str)
@click.option('-v', '--version', required=True, type=str,
              help="Version of the Tool package.")
@click.option('-p', '--package_version', required=True, type=str,
              help="Package version of the Tool package.")
def describe_tool(name: str, version: str, package_version: str) -> None:
    metadatacollector = ToolMetadataCollector(fastrpi_config.tools_folder / fastrpi_config.metadata_path)
    packageinfo = PackageInfo(name=name, version=version, package_version=package_version)
    describe_dict = metadatacollector.metadata[packageinfo.tag]['describe']
    describe_dict_keys = [key for key in describe_dict.keys()]
    while True:
        response = questionary.select("Which Tool do you want to select?:",
                                      choices=describe_dict_keys).ask()
        click.echo(describe_dict[response]['repr'])
        if not questionary.confirm("Go back?", default=False).ask():
            break


@click.command('network')
@click.argument('name', type=str)
@click.option('-v', '--version', required=True, type=str,
              help="Version of the Network package.")
def describe_network(name: str, version: str) -> None:
    metadatacollector = NetworkMetadataCollector(fastrpi_config.networks_folder / fastrpi_config.metadata_path)
    packageinfo = PackageInfo(name=name, package_version=version)
    sources = metadatacollector.metadata[packageinfo.tag]['sources']
    sinks = metadatacollector.metadata[packageinfo.tag]['sinks']
    click.echo("Sources:")
    click.echo(tabulate(sources, headers="keys", disable_numparse=True))
    click.echo("\n")
    click.echo("Sinks:")
    click.echo(tabulate(sinks, headers="keys", disable_numparse=True))
