import shutil
from pathlib import Path
from typing import Union

import click

from .metadatacollector import MetadataCollector, NetworkMetadataCollector, ToolMetadataCollector
from .utils import get_manifest_path, get_manifest_path_tag
from .. import fastrpi_config
from ..manifest import Manifest
from ..package import Package
from ..packageinfo import PackageInfo

SERVER_DICTIONARY = '_server'

@click.group()
def cli():
    """ Client for the Fastr Package Index (FastrPI)."""
    pass


@click.command('cicd-checks')
@click.argument('repository_folder', type=click.Path(exists=True, file_okay=False))
@click.argument('commit_message', type=str)
def cicd_checks(repository_folder: click.Path, commit_message: str) -> None:
    """
    CLI for tests to run during CI/CD.

    :param click.Path repository_folder: Folder for the tool or network repository.
    :param str commit_message: Commit message for the commit adding the network or tool.
    """
    repository_path = Path(click.format_filename(str(repository_folder)))
    manifest_path = get_manifest_path(repository_path, commit_message)
    manifest = Manifest.create(manifest_path)
    package = Package.create(manifest)

    package.run_checks()

    (repository_path / "test.env").touch()
    if package.package_type in ['Tool', 'MacroNode']:
        if package.package_type == 'MacroNode':
            lines = ["CONTAINER=0\n",
                     "DOCKER_BUILD=0\n"]
        elif 'external_container' in manifest.keys() and manifest['external_container']:
            lines = ["CONTAINER=1\n",
                     "DOCKER_BUILD=0\n",
                     f"CONTAINER_NAME={manifest['dockerurl']}\n"
                     ]
        else:
            lines = ["CONTAINER=1\n",
                     "DOCKER_BUILD=1\n",
                     f"TOOL_FOLDER={manifest_path.parent}\n",
                     f"CONTAINER_NAME={manifest.container['name']}\n",
                     f"CONTAINER_VERSION={manifest.container['package_version']}\n",
                     f"DOCKERFILE_PATH={manifest['dockerfile']}\n",
                     ]
        with open(str(repository_path / "test.env"), 'w') as fname:
            fname.writelines(lines)


cli.add_command(cicd_checks, name='cicd-checks')


@click.command('copy-reports')
@click.argument('repository_folder', type=click.Path(exists=True, file_okay=False))
@click.argument('commit_message', type=str)
@click.option('--container_scanning', required=True, type=click.Path(exists=True, dir_okay=False),
              help="Gitlab Container Scanning report.")
@click.option('--deps_scanning', required=True, type=click.Path(exists=True, dir_okay=False),
              help="Gitlab Dependency Scanning report.")
def copy_reports(repository_folder: click.Path, commit_message: str, container_scanning: click.Path,
                 deps_scanning: click.Path):
    """
    When a new Package is uploaded, read the package list, update it and write it back again.
    """
    repository_path = Path(click.format_filename(str(repository_folder)))
    container_scanning_path = Path(click.format_filename(str(container_scanning)))
    deps_scanning_path = Path(click.format_filename(str(deps_scanning)))
    manifest_path = get_manifest_path(repository_path, commit_message)
    shutil.copy(container_scanning_path,
                manifest_path.parent / ".".join([str(container_scanning_path.stem), "fastrpi_json"]))
    shutil.copy(deps_scanning_path, manifest_path.parent / ".".join([str(deps_scanning_path.stem), "fastrpi_json"]))


@click.command('update-list')
@click.argument('repository_folder', type=click.Path(exists=True, file_okay=False))
@click.argument('commit_message', type=str)
@click.option('--dockerdigest', required=False, type=str,
              help="Image digest of a Docker image.")
def update_list(repository_folder: click.Path, commit_message: str, dockerdigest: Union[str, None] = None):
    """
    When a new Package is uploaded, read the package list, update it and write it back again.
    """
    repository_path = Path(click.format_filename(str(repository_folder)))
    manifest_path = get_manifest_path(repository_path, commit_message)
    manifest = Manifest.create(manifest_path)
    packageinfo = PackageInfo.from_dict(manifest)

    if manifest['package_type'] == 'network':
        metadatacollector = NetworkMetadataCollector(repository_path / fastrpi_config.metadata_path)
    else:
        metadatacollector = ToolMetadataCollector(repository_path / fastrpi_config.metadata_path)

    metadatacollector.add_from_manifest(manifest)
    if manifest['package_type'] == 'tool':
        metadatacollector.update_item(packageinfo.tag, {'docker_digest': dockerdigest})
    metadatacollector.set_published(packageinfo.tag)
    metadatacollector.write_metadata()


@click.command('update-list-format')
@click.argument('repository_folder', type=click.Path(exists=True, file_okay=False))
@click.argument('repo_type', type=str)
def update_list_format(repository_folder: click.Path, repo_type: str):
    """
    When the package list format changes, use this function to update the list to the new format.
    """
    repository_path = Path(click.format_filename(str(repository_folder)))
    keep_tags = ['status', 'date_published']
    if repo_type == 'network':
        metadatacollector = NetworkMetadataCollector(repository_path / fastrpi_config.metadata_path)
    else:
        metadatacollector = ToolMetadataCollector(repository_path / fastrpi_config.metadata_path)
        keep_tags += ['docker_digest']
    metadatacollector.repository_path = repository_path
    metadatacollector.reinit(repository_path, keep=keep_tags)
    metadatacollector.write_metadata()


cli.add_command(update_list, name='update-list')
cli.add_command(update_list_format, name='update-list-format')
cli.add_command(copy_reports, name='copy-reports')
