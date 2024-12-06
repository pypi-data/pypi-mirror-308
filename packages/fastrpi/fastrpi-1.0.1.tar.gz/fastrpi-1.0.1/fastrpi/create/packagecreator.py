import os
from pathlib import Path
from typing import List

import click
import questionary

from .extract import ToolExtractor, NetworkExtractor
from ..exceptions import FastrPICreateError, FastrPIManifestError
from ..helpers import read_yaml, write_yaml
from ..manifest import Manifest


class PackageCreator:
    def __init__(self, package_files):
        self.name = None
        self.package_files = package_files
        self.filelist = [str(fname) for fname in Path().rglob('*')]
        self.datatypes = []
        self.manifest_path = Path("./manifest.fastrpi_yaml")
        self.manifest_obj = {}
        self.manifest = None
        self.manifest_order = []

    def extract_info(self) -> None:
        pass

    def request_input(self) -> None:
        pass

    def _select_manifest_path(self) -> None:
        manifest_exists = self.manifest_path.exists()
        select_manifest = [
            {
                'type': 'confirm',
                'name': 'use_another_manifest',
                'message': f"Manifest {self.manifest_path} already exists. Use another?",
                'default': True,
                'when': lambda x: manifest_exists,
            },
            {
                'type': 'print',
                'name': 'print_manifest_doesnt_exist',
                'message': f"Manifest doesn't exist. Will use {self.manifest_path}.",
                'when': lambda x: not manifest_exists
            },
            {
                'type': 'text',
                'name': 'new_manifest_path',
                'message': f"Manifest filename:",
                'when': lambda x: manifest_exists and x["use_another_manifest"],
                'validate': lambda val: True if not Path(val).exists() else "Invalid filename. File already exists."
            }
        ]

        response = questionary.unsafe_prompt(select_manifest)
        if not manifest_exists:
            questionary.print(f"Manifest {self.manifest_path} doesn't exist. This file will be created.")
        self.manifest_path = Path(response.get('new_manifest_path', self.manifest_path))
        self.manifest_path = self.manifest_path.resolve()

    def _select_licence(self) -> None:
        license_exists = Path("./LICENSE").resolve().exists()
        licence_exists = Path("./LICENCE").resolve().exists()
        select_license = [
            {
                'type': 'confirm',
                'name': 'use_license',
                'message': f"LICENSE found in current directory. Do you want to use this file?",
                'default': True,
                'when': lambda x: license_exists,
            },
            {
                'type': 'confirm',
                'name': 'use_licence',
                'message': f"LICENCE found in current directory. Do you want to use this file?",
                'default': True,
                'when': lambda x: licence_exists,
            },
            {
                'type': 'path',
                'name': 'license_path',
                'message': f"Where is the license?",
                'when': lambda x: (not license_exists and not licence_exists) or (not x.get('use_license', True) or not x.get('use_licence', True)),
                'validate': lambda val: True if Path(val).is_file() else "License needs to be a file."
            }
        ]

        response = questionary.unsafe_prompt(select_license)
        if response.get('use_license', False):
            self.manifest_obj['license'] = './LICENSE'
        elif response.get('use_licence', False):
            self.manifest_obj['license'] = './LICENCE'
        elif response.get('license_path', False):
            self.manifest_obj['license'] = str(Path(response['license_path']))

    def _calc_remaining_files(self) -> List[Path]:
        manifest_files = [fname.relative_to(self.manifest.folder) for fname in self.manifest.files]

        manifest_obj_files = [str(fname) for fname in manifest_files]
        remaining_files = list(set(self.filelist) - set(manifest_obj_files))
        not_remaining_files = []
        for fname in remaining_files:
            for manifest_fname in manifest_obj_files:
                try:
                    Path(fname).relative_to(Path(manifest_fname))
                    not_remaining_files.append(fname)
                    break
                except ValueError:
                    pass
        remaining_files = list(set(remaining_files) - set(not_remaining_files))
        remaining_files = [Path(x) for x in remaining_files]
        return remaining_files

    def _select_files(self) -> None:
        try:
            write_yaml(self.manifest_obj, self.manifest_path)
            self.manifest = Manifest.create(self.manifest_path)

            remaining_files = self._calc_remaining_files()
            if len(remaining_files) > 0:
                while True:
                    if questionary.confirm("Do you want to add any more files? ").unsafe_ask():
                        response = questionary.path("Which file or folder do you want to add? Leave blank to cancel.",
                                                    default="",
                                                    file_filter=lambda x: Path(x) in remaining_files).unsafe_ask()
                        if not response:
                            break
                        else:
                            questionary.print(f"- Adding {response}.", style='bold')
                        if 'files' not in self.manifest_obj.keys():
                            self.manifest_obj['files'] = [{'type': 'local', 'path': str(Path(response))}]
                        else:
                            self.manifest_obj['files'] += [{'type': 'local', 'path': str(Path(response))}]
                        self.manifest.update(**self.manifest_obj)
                        remaining_files = self._calc_remaining_files()
                        if len(remaining_files) == 0:
                            break
                    else:
                        questionary.print("- Not adding any more files.", style='bold')
                        break
        except FastrPIManifestError as exc:
            click.echo(exc)
            if self.manifest_path.exists():
                os.remove(self.manifest_path)
        except KeyboardInterrupt as exc:
            if self.manifest_path.exists():
                os.remove(self.manifest_path)
            raise KeyboardInterrupt from exc
        else:
            if self.manifest_path.exists():
                os.remove(self.manifest_path)

    def create_manifest(self) -> None:
        self.sort_manifest_obj()
        try:
            write_yaml(self.manifest_obj, self.manifest_path)
            questionary.print("- Manifest file created.", style='bold')
            if questionary.confirm("Do you want to edit the Manifest?", default=False).unsafe_ask():
                click.edit(filename=str(self.manifest_path))
        except Exception as exc:
            print(exc)
            # Clean up Manifest file if it is not successful
            if self.manifest_path.exists() & self.manifest_path.is_file():
                os.remove(self.manifest_path)
        pass

    def sort_manifest_obj(self) -> None:
        sorted_manifest = {}
        for key in self.manifest_order:
            if key in self.manifest_obj.keys():
                sorted_manifest[key] = self.manifest_obj[key]
        for key in self.manifest_obj.keys():
            if key not in self.manifest_order:
                sorted_manifest[key] = self.manifest_obj[key]
        self.manifest_obj = sorted_manifest

    def modify_files(self) -> None:
        pass

    def create(self) -> None:
        self.extract_info()
        self.request_input()
        self.create_manifest()
        self.modify_files()


class ToolPackageCreator(PackageCreator):
    def __init__(self, package_files):
        super().__init__(package_files)
        self.extractor = ToolExtractor(package_files)
        self.tool_versions = []
        self.command_versions = []
        self.manifest_order = ['name', 'version', 'package_version', 'license', 'required_datatypes', 'package_type',
                               'dockerfile', 'external_container', 'dockerurl', 'tools', 'files']

    def extract_info(self) -> None:
        self.extractor.extract_info()
        self.extractor.report()
        self.datatypes = self.extractor.datatypes
        self.tool_versions = [val['tool_version'] for val in self.extractor.tool_dicts]
        self.command_versions = [val['command_version'] for val in self.extractor.tool_dicts]
        self.datatypes = self.extractor.datatypes

    def request_input(self) -> None:
        try:
            self._select_manifest_path()
            self._select_name()
            self._select_version()
            self._select_licence()
            self._select_dockerfile()
            self._add_tools()
            self.manifest_obj['required_datatypes'] = self.datatypes
            self.manifest_obj['package_type'] = 'tool'
            self._select_files()
        except KeyboardInterrupt:
            raise FastrPICreateError

    def _select_name(self) -> None:
        self.manifest_obj['name'] = questionary.text("What is the package name?").unsafe_ask()

    def _select_version(self) -> None:
        self.manifest_obj['version'] = self._select_version_tool(self.command_versions, 'version')
        self.manifest_obj['package_version'] = self._select_version_tool(self.tool_versions, 'package_version')

    def _select_version_tool(self, versions, version_type) -> str:
        if len(set(versions)) == 1:
            questionary.print(f"- Found {version_type}s {versions[0]} for all Tools", style='bold')
            return versions[0]
        versions = list(set(versions))
        questionary.print(f"- Found {versions} as {version_type}s.", style='bold')
        version_input = questionary.select("Which one would you like for the package (and therefore all the tools)?",
                                           choices=versions).unsafe_ask()
        return version_input

    def _select_dockerfile(self) -> None:
        dockerfile_exists = Path("./Dockerfile").resolve().exists()
        select_license = [
            {
                'type': 'confirm',
                'name': 'use_dockerfile',
                'message': f"Dockerfile found in current directory. Do you want to use this file?",
                'default': True,
                'when': lambda x: dockerfile_exists,
            },
            {
                'type': 'confirm',
                'name': 'use_external_container',
                'message': f"No Dockerfile is found, or you don't want to use it. Will an external Docker image be used?",
                'default': True,
                'when': lambda x: not dockerfile_exists or not x['use_dockerfile'],
            },
            {
                'type': 'text',
                'name': 'dockerurl',
                'message': f"What is the URL of the Docker image?",
                'when': lambda x: not x['use_dockerfile'] and x['use_external_container'],
            },
            {
                'type': 'path',
                'name': 'dockerfile_path',
                'message': f"Where is the Dockerfile?",
                'when': lambda x: (not dockerfile_exists and not x['use_external_container']) or not x['use_dockerfile'],
                'validate': lambda val: True if Path(val).is_file() else "Dockerfile needs to be a file."
            }
        ]

        response = questionary.unsafe_prompt(select_license)
        if response.get('use_dockerfile', False):
            self.manifest_obj['dockerfile'] = './Dockerfile'
        elif response.get('use_external_container', False):
            self.manifest_obj['external_container'] = True
            self.manifest_obj['dockerurl'] = response.get('dockerurl', '')
        elif response.get('dockerfile_path', False):
            self.manifest_obj['dockerfile'] = str(Path(response['dockerfile_path']))

    def _add_tools(self) -> None:
        tools_list = []
        for tool in self.package_files:
            tool_dict = {'tool_definition': str(tool), }
            if f'LICENSE_{tool.stem}' in self.filelist:
                tool_dict['license'] = f'./LICENSE_{tool.stem}'
            tools_list.append(tool_dict)
        self.manifest_obj['tools'] = tools_list

    def modify_files(self) -> None:
        self._correct_version_tool(self.package_files, 'command_version', self.manifest_obj['version'])
        self._correct_version_tool(self.package_files, 'tool_version', self.manifest_obj['package_version'])
        self._correct_targets()

    def _correct_targets(self) -> None:
        for tool_file in self.package_files:
            tool = read_yaml(tool_file)
            docker_images = [target['docker_image'] for target in tool['command']['targets']
                             if target.get('class', 'NotFound') == 'DockerTarget']
            singularity_images = [target['container'] for target in tool['command']['targets']
                                  if target.get('class', 'NotFound') == 'SingularityTarget']
            docker_image_manifest = f"{self.manifest_obj['name']}-v{self.manifest_obj['version']}:" \
                                    + f"{self.manifest_obj['package_version']}"
            singularity_image_manifest = f"{self.manifest_obj['name']}-v{self.manifest_obj['version']}_" \
                                         + f"{self.manifest_obj['package_version']}.sif"
            for idx, target in enumerate(tool['command']['targets']):
                if target.get('class', 'NotFound') == 'DockerTarget' and target['docker_image'] != docker_image_manifest:
                    questionary.print(f"- {tool_file}: Replacing Docker image {target['docker_image']} with {docker_image_manifest}.",
                                      style='bold')
                    tool['command']['targets'][idx]['docker_image'] = docker_image_manifest
                elif target.get('class', 'NotFound') == 'SingularityTarget' and target['container'] != singularity_image_manifest:
                    questionary.print(
                        f"- {tool_file}: Replacing Singularity image {target['container']} with {singularity_image_manifest}.",
                        style='bold')
                    tool['command']['targets'][idx]['container'] = singularity_image_manifest
            write_yaml(tool, tool_file)

            while not docker_images or not singularity_images:
                if not docker_images:
                    if questionary.confirm(f"No DockerTarget is known for {tool_file}. Do you want to add one?").unsafe_ask():
                        tool['command']['targets'].append({
                            'arch': '*', 'os': '*', 'class': 'DockerTarget',
                            'docker_image': docker_image_manifest, 'interpreter': '', 'binary': '',
                        })
                        write_yaml(tool, tool_file)
                        if questionary.confirm("Do you want to manually add the interpreter and binary now?").unsafe_ask():
                            click.edit(filename=str(tool_file))
                    tool = read_yaml(tool_file)
                elif docker_images and not singularity_images:
                    if questionary.confirm(
                            f"No SingularityTarget is known for {tool_file}. Do you want to automatically add one?").unsafe_ask():
                        docker_targets = [target for target in tool['command']['targets']
                                          if target.get('class', 'NotFound') == 'DockerTarget']
                        singularity_target = {
                            'arch': '*', 'os': '*', 'class': 'SingularityTarget',
                            'container': singularity_image_manifest,
                            'binary': docker_targets[0].get('binary', ''),
                        }
                        if docker_targets[0].get('interpreter', False):
                            singularity_target['interpreter'] = docker_targets[0].get('interpreter')
                        tool['command']['targets'].append(singularity_target)
                        write_yaml(tool, tool_file)
                        if questionary.confirm(f"Do you want to edit {tool_file} now?").unsafe_ask():
                            click.edit(filename=str(tool_file))
                    elif questionary.confirm("Do you want to manually add one?").unsafe_ask():
                        click.edit(filename=str(tool_file))
                    tool = read_yaml(tool_file)
                docker_images = [target['docker_image'] for target in tool['command']['targets']
                                 if target.get('class', 'NotFound') == 'DockerTarget']
                singularity_images = [target['container'] for target in tool['command']['targets']
                                      if target.get('class', 'NotFound') == 'SingularityTarget']

    @staticmethod
    def _correct_version_tool(tool_files, version_type, version) -> None:
        for tool_file in tool_files:
            tool = read_yaml(tool_file)
            if version_type == 'command_version':
                tool['command']['version'] = version
            elif version_type == 'tool_version':
                tool['version'] = version
            write_yaml(tool, tool_file)


class MacroNodePackageCreator(PackageCreator):
    def __init__(self, name, version):
        super().__init__(name, [])
        self.version = version
        if Path(f'./macro_{self.name}.yaml').exists():
            self.tool_def_exists = True
            self.tool_def = read_yaml(Path(f'./macro_{self.name}.yaml'))
        else:
            self.tool_def_exists = False
            self.tool_def = {
                'id': f'Macro-{self.name}',
                'name': f'Macronode of Network {self.name}, version {self.version}',
                'version': '1.0',
                'description': f'Macronode of Network {self.name}, version {self.version}',
                'authors': [{'name': '', 'email': '', 'url': ''}],
                'class': 'MacroNode',
                'command': {
                    'version': self.version,
                    'url': '',
                    'targets': [
                        {'os': '*', 'arch': '*', 'network_file': f'{self.name}-v{self.version}.py',
                         'function': 'create_network'}
                    ],
                    'description': '',
                    'authors': [{'name': '', 'email': '', 'url': ''}]
                },
                'interface': {'inputs': [], 'outputs': []}
                }
            write_yaml(self.tool_def, Path(f'./macro_{self.name}.yaml'))
        self.manifest_order = ['name', 'network_name', 'version', 'package_version', 'license', 'package_type',
                               'tools']

    def _select_name(self):
        self.manifest_obj['name'] = 'macro_' + self.name
        self.manifest_obj['network_name'] = self.name

    def _select_version(self):
        self.manifest_obj['version'] = self.version
        if self.tool_def_exists:
            self.manifest_obj['package_version'] = self.tool_def['version']
        else:
            self.manifest_obj['package_version'] = '1.0'

    def request_input(self) -> None:
        self._select_name()
        self._select_version()
        self.manifest_obj['package_type'] = 'macronode'
        self.manifest_obj['tools'] = [{'tool_definition': f'macro_{self.name}.yaml'}]
        self._select_files()


class NetworkPackageCreator(PackageCreator):
    def __init__(self, package_files):
        super().__init__(package_files)
        self.network_path = package_files
        self.tools = []
        self.network_name = None
        self.network_version = None
        self.datatypes = None
        self.extractor = NetworkExtractor(package_files)
        self.manifest_order = ['name', 'package_version', 'license', 'required_datatypes', 'readme', 'package_type',
                               'network', 'cite', 'tool_packages', 'files']
        
    def extract_info(self) -> None:
        self.extractor.extract_info()
        self.extractor.report()
        self.network_name = self.extractor.network_name
        self.network_version = self.extractor.network_version
        self.tools = self.extractor.tools
        self.datatypes = self.extractor.datatypes
    
    def request_input(self) -> None:
        self._select_manifest_path()
        self._select_name()
        self._select_version()
        self._select_licence()
        self._select_readme()
        self._select_reference()
        self.manifest_obj['required_datatypes'] = self.datatypes
        self.manifest_obj['package_type'] = 'network'
        self.manifest_obj['network'] = str(self.network_path)
        self.manifest_obj['tool_packages'] = self.tools
        self._select_files()

    def _select_name(self) -> None:
        questionary.print(f"- Found network name {self.network_name}.", style='bold')
        self.manifest_obj['name'] = self.network_name

    def _select_version(self) -> None:
        questionary.print(f"- Found network version {self.network_version}.", style='bold')
        self.manifest_obj['package_version'] = self.network_version

    def _select_readme(self) -> None:
        readme_md_exists = Path("./README.md").resolve().exists()
        readme_txt_exists = Path("./README.txt").resolve().exists()
        select_readme = [
            {
                'type': 'confirm',
                'name': 'use_readme_md',
                'message': f"README.md found in current directory. Do you want to use this file?",
                'default': True,
                'when': lambda x: readme_md_exists,
            },
            {
                'type': 'confirm',
                'name': 'use_readme_txt',
                'message': f"README.txt found in current directory. Do you want to use this file?",
                'default': True,
                'when': lambda x: readme_txt_exists,
            },
            {
                'type': 'path',
                'name': 'readme_path',
                'message': f"Where is the readme?",
                'when': lambda x: (not readme_md_exists and not readme_txt_exists) or (not x.get('use_readme_md', True) or not x.get('use_readme_txt', True)),
                'validate': lambda val: True if Path(val).is_file() else "Readme needs to be a file."
            }
        ]

        response = questionary.unsafe_prompt(select_readme)
        if response.get('use_readme_md', False):
            self.manifest_obj['readme'] = './README.md'
        elif response.get('use_readme_txt', False):
            self.manifest_obj['readme'] = './README.txt'
        elif response.get('readme_path', False):
            self.manifest_obj['readme'] = str(Path(response['readme_path']))

    def _select_reference(self) -> None:
        cite_string = questionary.text('Please enter a reference to cite upon using this Network').unsafe_ask()
        cite_list = [cite_string]
        while True:
            if questionary.confirm('Do you want to add more references?', default=False).unsafe_ask():
                cite_list.append(questionary.text('Please enter a reference to cite upon using this Network').unsafe_ask())
            else:
                break
        self.manifest_obj['cite'] = cite_list
