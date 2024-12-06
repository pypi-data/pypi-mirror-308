import os
import shutil
from pathlib import Path
from typing import Union

from .helpers import read_yaml, write_yaml, walk_dict_list


class Config(object):
    """
    Configuration class for FastrPI.

    Contains information on the home folder and remote repositories.
    """

    def __init__(self, config_file: Union[Path, str, None] = None):
        self.public = True
        self.fastr_home = Path.home() / '.fastr'
        self.fastrpi_home = Path.home() / '.fastrpi'
        self.manifest_name = 'manifest.fastrpi_yaml'

        self._set_homefolder()
        self.tool_record_path = self.fastrpi_home / 'installed_tools.json'
        self.network_record_path = self.fastrpi_home / 'installed_networks.json'
        self.tools_folder = self.fastrpi_home / 'tools'
        self.networks_folder = self.fastrpi_home / 'networks'
        self.datatypes_folder = self.fastrpi_home / 'datatypes'
        if not self.fastrpi_home.exists() or not self.fastrpi_home.is_dir():
            self._create_homedir()

        self.config_file = self.fastrpi_home / 'config.yaml'
        if config_file is not None:
            config_file = Path(config_file).resolve()
            shutil.copy(config_file, self.config_file)

        self.container_type = ['docker']
        self.singularity_dir = Path(self.fastrpi_home / 'singularity')

        self.gitlab_token = None
        self.gitlab_token_file = None
        self.slurm_pull_partition = None
        self.repository_urls = None
        self.git_main_branch = 'master'
        self._read_config()
        self._set_gitlab_token()
        self._set_repository_urls()
        
        
        self.singularity_dir = Path(self.singularity_dir)
        if not self.singularity_dir.exists():
            self.singularity_dir.mkdir(parents=True)
        os.environ['FASTRPI_SINGULARITY_DIR'] = str(self.singularity_dir)

        # Metadata path is relative to the repository path
        self.metadata_path = 'metadata.fastrpi_json'

    def _set_homefolder(self):
        fastr_home_envvar = os.environ.get('FASTRHOME', None)
        if fastr_home_envvar is not None:
            fastr_home = Path(fastr_home_envvar).expanduser().resolve()
            if not fastr_home.exists():
                print(f"Directory {fastr_home} is set as environment variable FASTRHOME, but it doesn't exist.")
                raise SystemExit
        else:
            fastr_home = Path.home() / '.fastr'

        if fastr_home.exists():
            self.fastrpi_home = fastr_home / 'fastrpi'
            self.fastr_home = fastr_home

        fastrpi_home_envvar = os.environ.get('FASTRPIHOME', None)
        if fastrpi_home_envvar is not None:
            self.fastrpi_home = Path(fastrpi_home_envvar).expanduser().resolve()
        if fastrpi_home_envvar is not None and not self.fastrpi_home.exists():
            print(f"Directory {self.fastrpi_home} is set as environment variable FASTRPIHOME, but it doesn't exist.")
            raise SystemExit

    def _set_gitlab_token(self):
        if self.gitlab_token_file:
            if not Path(self.gitlab_token_file).exists():
                print("File 'gitlab_token_file' does not exist.")
                raise SystemExit
            with open(self.gitlab_token_file, 'r') as fname:
                gitlab_token = fname.read().strip()
            self.gitlab_token = gitlab_token
        else:
            try:
                self.gitlab_token = os.environ['FASTRPI_GITLAB_TOKEN']
            except KeyError:
                print("Configuration option 'gitlab_token_file' and environment variable 'FASTRPI_GITLAB_TOKEN' "
                      + "are both not set. "
                      + "Publishing packages will not be possible.")

    def _create_homedir(self) -> None:
        """
        Create the FastrPI home directory.
        """
        self.fastrpi_home.mkdir(parents=True, exist_ok=False)
        self.datatypes_folder.mkdir(parents=True, exist_ok=False)

    def _set_repository_urls(self) -> None:
        if not self.repository_urls:
            if not self.public:
                self.repository_urls = {
                    'networks_git': 'git@gitlab.com:radiology/infrastructure/resources/fastrpi/fastrpi-networks.git',
                    'tools_git': 'git@gitlab.com:radiology/infrastructure/resources/fastrpi/fastrpi-tools.git',
                    'tools_docker': 'registry.gitlab.com/radiology/infrastructure/resources/fastrpi/fastrpi-tools',
                }
                self.git_main_branch = 'master'
            else:
                self.repository_urls = {
                    'networks_git': 'https://gitlab.com/radiology/infrastructure/resources/fastrpi/fastrpi-networks-public.git',
                    'tools_git': 'https://gitlab.com/radiology/infrastructure/resources/fastrpi/fastrpi-tools-public.git',
                    'tools_docker': 'registry.gitlab.com/radiology/infrastructure/resources/fastrpi/fastrpi-tools-public',
                }
                self.git_main_branch = 'master'
        pass

    def _read_config(self) -> None:
        config_vars = [
            'repository_urls',
            'container_type',
            'tool_record_path',
            'network_record_path',
            'datatypes_folder',
            'manifest_name',
            'singularity_dir',
            'gitlab_token_file',
            'slurm_pull_partition',
            'git_main_branch',
            'public'
        ]
        if self.config_file.exists():
            print("Config file found.")
            data = read_yaml(self.config_file)
            for var in config_vars:
                try:
                    setattr(self, var, data[var])
                except KeyError:
                    pass
                
    def write(self, attribute) -> None:
        # def walk_dict_list(d):
        #     if isinstance(d, dict):
        #         for k, v in d.items():
        #             if isinstance(v, (dict, list)):
        #                 d[k] = walk_dict_list(v)
        #             elif isinstance(v, Path):
        #                 d[k] = str(v)
        #             else:
        #                 pass
        #     elif isinstance(d, list):
        #         for idx, item in enumerate(d):
        #             if isinstance(item, (dict, list)):
        #                 d[idx] = walk_dict_list(item)
        #             elif isinstance(item, Path):
        #                 d[idx] = str(item)
        #             else:
        #                 pass
        #     return d
        if self.config_file.exists():
            print("Config file found.")
            data = read_yaml(self.config_file)
        else:
            data = {}
        data.update({
            attribute: walk_dict_list(getattr(self, attribute))
        })
        write_yaml(data, self.config_file)
        print(f"Written attribute {attribute}")
