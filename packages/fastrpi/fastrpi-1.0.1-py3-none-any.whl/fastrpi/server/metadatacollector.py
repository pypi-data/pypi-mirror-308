import json
import os
from copy import deepcopy
from datetime import date
from pathlib import Path
from typing import Union, List

from .utils import network_manifest_path, tool_manifest_path
from .. import fastrpi_config
from ..create.extract import NetworkExtractor, ToolExtractor
from ..exceptions import FastrPIError
from ..helpers import walk_dict_list
from ..manifest import Manifest
from ..packageinfo import PackageInfo


class MetadataCollector:
    def __init__(self, metadata_path: Union[str, Path]):
        self.metadata_path = Path(metadata_path).resolve()
        self.metadata = {}
        self.load_metadata()

        self.repository_path = self.metadata_path.parent

    def load_metadata(self) -> None:
        if self.metadata_path.exists():
            with open(self.metadata_path, 'r') as fname:
                self.metadata = json.load(fname)
        else:
            raise FastrPIError(f"Can't find {self.metadata_path}.")

    def write_metadata(self) -> None:
        # def walk_dict_list(d):
        #     if isinstance(d, dict):
        #         for k, v in d.items():
        #             if isinstance(v, (dict, list)):
        #                 d[k] = walk_dict_list(v)
        #             elif isinstance(v, Path):
        #                 d[k] = str(v)
        #             else:
        #                 pass
        #     else:
        #         for idx, item in enumerate(d):
        #             if isinstance(item, (dict, list)):
        #                 d[idx] = walk_dict_list(item)
        #             elif isinstance(item, Path):
        #                 d[idx] = str(item)
        #             else:
        #                 pass
        #     return d

        metadata_obj = deepcopy(self.metadata)
        metadata_obj = walk_dict_list(metadata_obj)
        with open(self.metadata_path, 'w') as fname:
            json.dump(metadata_obj, fname, indent=4)

    def add_from_manifest(self, manifest: Union[Manifest, Path]) -> Manifest:
        if isinstance(manifest, Path):
            manifest = Manifest.create(manifest)
        packageinfo = PackageInfo.from_dict(manifest)
        self.update_item(packageinfo.tag, manifest)
        return manifest

    def update_item(self, package_tag: str, input_dict: dict) -> None:
        self.metadata[package_tag] = self.metadata.get(package_tag, {})
        self.metadata[package_tag].update(input_dict)

    def set_published(self, package_tag: str):
        published_dict = {
            'status': 'Published',
            'date_published': str(date.today())
        }
        self.update_item(package_tag, published_dict)

    def reinit(self, repository_path: Union[Path, str], keep: Union[str, List[str]]) -> None:
        repository_path = Path(repository_path)
        keep_metadata = {}
        if isinstance(keep, str):
            keep = [keep]
        for key, value in self.metadata.items():
            keep_metadata[key] = keep_metadata.get(key, {})
            for item in keep:
                if value.get(item, False):
                    keep_metadata[key][item] = keep_metadata[key].get(item, None)
                    keep_metadata[key][item] = value[item]
        self.metadata = keep_metadata

        for pathname, dirnames, fnames in os.walk(repository_path):
            for f in fnames:
                if f == fastrpi_config.manifest_name:
                    self.add_from_manifest(Path(pathname) / f)


class NetworkMetadataCollector(MetadataCollector):
    def __init__(self, metadata_path: Union[str, Path]):
        super().__init__(metadata_path)
        # self.repository_path = fastrpi_config.networks_folder

    def add_from_extractor(self, network_file) -> None:
        extractor = NetworkExtractor(network_file)
        extractor.extract_info()
        input_dict = {
            'sinks': extractor.sinks,
            'sources': extractor.sources
        }
        packageinfo = PackageInfo(name=extractor.network_name,
                                  package_version=extractor.network_version)
        self.update_item(packageinfo.tag, input_dict)

    def add_from_manifest(self, manifest: Union[Manifest, Path]) -> None:
        manifest = super().add_from_manifest(manifest)
        manifest_path = network_manifest_path(self.repository_path, PackageInfo.from_dict(manifest).tag)
        self.add_from_extractor(manifest_path.parent / manifest['network'])


class ToolMetadataCollector(MetadataCollector):
    def __init__(self, metadata_path: Union[str, Path]):
        super().__init__(metadata_path)
        # self.repository_path = fastrpi_config.tools_folder

    def add_from_extractor(self, package_files, package_tag) -> None:
        import fastr
        metadata = self.metadata[package_tag]
        name = metadata['name']
        version = metadata['version']
        package_version = metadata['package_version']
        package_files = [package_file.resolve() for package_file in package_files]
        extractor = ToolExtractor(package_files)
        extractor.extract_info()

        tool_path_list = []
        describe_dict = {}
        for tool_dict in extractor.tool_dicts:
            rel_tool_path = Path(tool_dict['tool_file']).relative_to(
                tool_manifest_path(self.repository_path, package_tag).parent)
            rel_tool_parent = rel_tool_path.parent
            if version == package_version:
                if rel_tool_parent.parts:
                    tool_path = '/'.join([name, version, str(rel_tool_parent), tool_dict['id']])
                else:
                    tool_path = '/'.join([name, version, tool_dict['id']])
            else:
                if rel_tool_parent.parts:
                    tool_path = '/'.join(
                        [name, version, package_version, str(rel_tool_parent), tool_dict['id']])
                else:
                    tool_path = '/'.join([name, version, package_version, tool_dict['id']])
            tool_path = tool_path + f':{version}'
            tool_path_list.append(tool_path)
            describe_dict[tool_path] = {'repr': repr(fastr.tools[tool_path, package_version]),
                                        'tool_definition': rel_tool_path,
                                        'id': tool_dict['id']}

        input_dict = {
            'fastr_tool_ids': tool_path_list,
        }
        self.update_item(package_tag, input_dict)
        print(describe_dict)
        self.update_item(package_tag, {'describe': describe_dict})

    def add_from_manifest(self, manifest: Union[Manifest, Path]) -> None:
        manifest = super().add_from_manifest(manifest)
        manifest_path = tool_manifest_path(self.repository_path, PackageInfo.from_dict(manifest).tag)
        package_tag = PackageInfo.from_dict(manifest).tag
        package_files = []
        for tool in manifest['tools']:
            package_files.append(manifest_path.parent / tool['tool_definition'])
        self.add_from_extractor(package_files, package_tag)
