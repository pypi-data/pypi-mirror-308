from pathlib import Path

from .. import fastrpi_config
from ..exceptions import FastrPIPublishTestError


def split_commit_message(commit_message: str) -> (str, str):
    commit_message_split = commit_message.split(' ')
    package_type = commit_message_split[1]
    package_tag = commit_message_split[2]
    return package_type, package_tag


def tool_manifest_path(base_path: Path, tag: str) -> Path:
    tag_split = tag.split('-v')
    name = tag_split[0]
    tag_split = tag_split[1].split('-p')
    version = tag_split[0]
    package_version = tag_split[1]
    return base_path / name / version / package_version / fastrpi_config.manifest_name


def network_manifest_path(base_path: Path, tag: str) -> Path:
    tag_split = tag.split('-v')
    name = tag_split[0]
    package_version = tag_split[1]
    return base_path / name / package_version / fastrpi_config.manifest_name


def get_manifest_path(base_path: Path, commit_message: str) -> Path:
    package_type, package_tag = split_commit_message(commit_message)

    if package_type in ['tool', 'macronode']:
        manifest_path = tool_manifest_path(base_path, package_tag)
    elif package_type in ['network']:
        manifest_path = network_manifest_path(base_path, package_tag)
    else:
        raise FastrPIPublishTestError(f'Package type {package_type} is unknown.')
    return manifest_path


def get_manifest_path_tag(base_path: Path, package_tag: str, repo_type: str) -> Path:
    if repo_type == 'tool':
        manifest_path = tool_manifest_path(base_path, package_tag)
    elif repo_type == 'network':
        manifest_path = network_manifest_path(base_path, package_tag)
    return manifest_path
