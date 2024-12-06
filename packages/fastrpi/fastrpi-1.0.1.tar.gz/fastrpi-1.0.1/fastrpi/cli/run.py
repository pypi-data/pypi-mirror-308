from pathlib import Path
from typing import Union

import click

import fastrpi
from ..exceptions import FastrPINotInstalled, FastrPIRunError
from ..helpers import load_module_from_file
from ..packageinfo import PackageInfo


@click.command('run', short_help="Runs an installed Network.")
@click.argument('name', type=str)
@click.option('-v', '--version', required=True, type=str,
              help="Version of an installed network.")
@click.option('--source_sink', required=True,
              type=click.Path(exists=True, dir_okay=False),
              help="Python file containing get_source_data().")
@click.option('--tmp_dir', required=False,
              type=click.Path(exists=True, file_okay=False),
              help="Directory for temporary files.")
@click.option('-m', '--memory_multiplier', required=False,
              type=int,
              help='Memory multiplier in Fastr ResourceLimit.')
def run_network(name: str, version: str, source_sink: click.Path,
                tmp_dir: Union[click.Path, None] = None, memory_multiplier: Union[int, None] = None) -> None:
    """
    Runs an installed network given files containing functions generating
    Source and Sink data.
    """
    from fastr.api import ResourceLimit
    source_sink_path = Path(click.format_filename(str(source_sink)))
    if tmp_dir is None:
        # tmp_dir_path = 'vfs://tmp/'
        tmp_dir_path = None
    else:
        tmp_dir_path = Path(click.format_filename(str(tmp_dir)))
    package_info = PackageInfo(name=name, package_version=version)

    try:
        if memory_multiplier is not None:
            ResourceLimit.set_memory_multiplier(memory_multiplier)
        package = fastrpi.network_install_record.load_package(package_info)
    except FastrPINotInstalled as exc:
        click.echo(exc)
        if fastrpi.network_package_repo.check_available(package_info):
            click.echo("It is available for installation from the remote repository.")
    else:
        try:
            package.run(source_sink_path, tmp_dir_path)
        except FastrPIRunError as exc:
            click.echo(exc)
            click.echo(f"The network {package_info}, could not be run.")
        else:
            click.echo(f"Running network {package_info} complete.")


@click.command('runlocal', short_help="Run a local network file.")
@click.argument('file', required=True, type=click.Path(exists=True, dir_okay=False))
@click.option('--source_sink', required=True,
              type=click.Path(exists=True, dir_okay=False),
              help="Python file containing get_source_data().")
@click.option('--tmp_dir', required=False,
              type=click.Path(exists=True, file_okay=False),
              help="Directory for temporary files.")
def run_local(file: click.Path, source_sink: click.Path,
              tmp_dir: Union[click.Path, None] = None) -> None:
    """
    Runs a network file given files containing functions generating
    Source and Sink data.
    """
    network_path = Path(click.format_filename(str(file)))
    source_sink_path = Path(click.format_filename(str(source_sink)))
    if tmp_dir is None:
        # tmp_dir_path = 'vfs://tmp/'
        tmp_dir_path = None
    else:
        tmp_dir_path = Path(click.format_filename(str(tmp_dir)))
    network_module = load_module_from_file(network_path, 'network_module')
    source_sink_module = load_module_from_file(source_sink_path, 'source_sink_module')

    network = network_module.create_network()
    source_data = source_sink_module.get_source_data()
    sink_data = source_sink_module.get_sink_data()
    network.execute(source_data, sink_data, tmpdir=tmp_dir_path)
