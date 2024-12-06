import json
import os
import shutil
import subprocess
import sys
from abc import abstractmethod
from pathlib import Path
from time import sleep
from typing import TYPE_CHECKING, Any, List, Union

import docker
import git
import requests
from docker.errors import APIError
from git.exc import GitCommandError, InvalidGitRepositoryError

from .exceptions import FastrPIDockerError, FastrPIGitError
from .manifest import Manifest
from .packageinfo import PackageInfo

if TYPE_CHECKING:
    from .config import Config
    from .package import Package


class RepositoryBackEnd(object):
    """ Package repository back-end

    All RepositoryBackEnd objects currently contain the implementation of the 
    local and remote storage of the packages.
    """
    def __init__(self, config: 'Config') -> None:
        self.config = config
        self.remote_url = ""


class GitRepository(RepositoryBackEnd):
    def __init__(self, config: 'Config') -> None:
        super().__init__(config)
        self.local_path = Path()
        self.draft_branch = None
        self.origin = None
        self.package_list = []
        self.sc_list = []

    @property
    def repository(self):
        return git.Repo(self.local_path)

    @property
    def git_direct(self):
        """
        Produces an object to directly access Git functionality.
        """
        return self.repository.git

    @property
    def filelist(self) -> List[Path]:
        self.pull_origin()
        filelist = self.git_direct.ls_files()
        filelist = [Path(filepath) for filepath in filelist.splitlines()]
        return filelist

    @property
    def _sparse_checkout_config_path(self):
        return self.local_path / '.git' / 'info' / 'sparse-checkout'

    def pull(self, package_info: 'PackageInfo') -> Manifest:
        """
        Retrieves a package from the repository by checking out the
        corresponding folder using sparse checkout.

        :param package_info: Package info
        """
        sparse_checkout_folder = str(
            self.folder_path(package_info).relative_to(self.local_path))
        self._add_sparse_checkout(sparse_checkout_folder)
        try:
            self.pull_origin()
            return Manifest.create(self.folder_path(package_info) / self.config.manifest_name)
        except GitCommandError as exc:
            self.remove_sparse_checkout(sparse_checkout_folder)
            raise FastrPIGitError(f"Failed to pull network {package_info} from remote.") from exc

    def push(self, package: 'Package') -> None:
        # Before pushing a branch, it should be checked if a CI/CD pipeline isn't running for the same Package.
        package_folder = self.folder_path_package(package)
        self._add_sparse_checkout(
            str(package_folder.relative_to(self.local_path)))

        self.pull_origin()
        self.create_draft_branch(package.tag)
        self._check_tests_running(package)
        if package_folder.exists():
            shutil.rmtree(package_folder)
        Path.mkdir(package_folder, parents=True)
        package.copy_files(package_folder)
        commit_message = f"Adds {package.manifest['package_type']} {package.tag}"
        self.git_direct.add(self.folder_path_package(package))
        self.git_direct.commit('-m', commit_message)
        self.repository.remotes.origin.push(self.draft_branch)

    def _check_tests_running(self, package: 'Package') -> None:
        if not self.config.gitlab_token:
            raise FastrPIGitError(f"Cannot determine if remote tests are running for {package.info}. "
                                  + "Gitlab token is not set.")
        headers = {'PRIVATE-TOKEN': self.config.gitlab_token}

        # Get project ID
        url = self.remote_url[:-4]
        url = url.split(':')[1]
        url = '%2F'.join(url.split('/'))
        try:
            req = requests.get(f'https://gitlab.com/api/v4/projects/{url}', headers=headers)
            project_id = req.json()['id']
        except KeyError:
            raise FastrPIGitError(f"Cannot determine if remote tests are running for {package.info}")

        scope = 'scope=running'
        page_num = 1
        req = requests.get(f'https://gitlab.com/api/v4/projects/{project_id}/pipelines?{scope}&page={page_num}',
                           headers=headers)
        request_bool = (req.status_code == 200) and (len(req.json()) > 0)
        while request_bool:
            package_tags = ['-'.join(pipeline['ref'].split('-')[2:]) for pipeline in req.json()]
            if package.info.tag in package_tags:
                raise FastrPIGitError(f"Remote tests are already running for {package.info}.")
            page_num += 1
            req = requests.get(f'https://gitlab.com/api/v4/projects/{project_id}/pipelines?{scope}&page={page_num}',
                               headers=headers)
            request_bool = (req.status_code == 200) and (len(req.json()) > 0)
        print(f"No remote tests are running for {package.info}.")

    def folder_path_package(self, package: 'Package') -> Path:
        return self.folder_path(package.info)

    @abstractmethod
    def folder_path(self, package_info: 'PackageInfo') -> Path:
        pass

    def checkout_main(self) -> None:
        """
        Checks out the main branch of the repository. Currently this is
        `master`.
        """
        try:
            self.git_direct.checkout(self.config.git_main_branch)
        except GitCommandError as exc:
            if exc.stderr != 'error: Sparse checkout leaves no entry on working directory':
                raise FastrPIGitError from exc

    def add_origin(self) -> None:
        """
        Adds remote repository URL under the name `origin`.
        """
        self.origin = self.repository.create_remote(
            'origin', self.remote_url)
        self.fetch_origin()

    def fetch_origin(self) -> None:
        """
        Fetches the remote repository at `origin`. Raises an exception when
        the remote repository cannot be fetched.
        """
        try:
            self.repository.remotes.origin.fetch()
        except GitCommandError as exc:
            print(exc)
            print(self.remote_url)
            print(self.origin.urls)
            raise FastrPIGitError("Failed to fetch remote repository.") from exc

    def pull_origin(self) -> None:
        """
        Pulls the remote repository at `origin`. Raises an exception when
        the remote repository cannot be pulled.
        """
        try:
            self.repository.remotes.origin.pull(self.config.git_main_branch)
        except GitCommandError as exc:
            raise FastrPIGitError("Failed to pull remote repository.") from exc

    def checkout_tag(self, tag: str) -> None:
        """
        Checks out a tagged commit. This process is canceled when the tag cannot
        be found locally. Raises an exception when the checkout process fails.

        :param tag: Tag to checkout.
        """
        try:
            if tag in self.repository.tags:
                self.git_direct.checkout(tag)
            else:
                print(f"Network with tag {tag} not found.")
                raise Exception
        except GitCommandError as exc:
            raise FastrPIGitError(f"Failed to checkout tag {tag}") from exc

    def create_draft_branch(self, tag: str) -> None:
        index = 0
        draft_branch = '-'.join(['draft', str(index), tag])
        while self._check_branch_present(draft_branch):
            index += 1
            draft_branch = '-'.join(['draft', str(index), tag])
        try:
            self.git_direct.checkout('HEAD', b=draft_branch)
        except GitCommandError:
            self.git_direct.checkout(b=draft_branch)
        self.draft_branch = draft_branch

    def delete_draft_branch(self) -> None:
        self.checkout_main()
        self.git_direct.branch('-D', self.draft_branch)
        self.draft_branch = None

    def remove_sparse_checkout(self, name: str) -> None:
        """
        Removes folder from sparse checkout if present.

        :param name: Folder to be removed from sparse checkout.
        """
        self._set_sc_list()
        if name in self.sc_list:
            self.sc_list.remove(name)
        self._write_sparse_checkout()
        self.checkout_main()

    def _init_repository(self) -> None:
        """
        Initializes a Git repository. Raises an exception when `gitpython`
        cannot execute Git. This can indicate that Git is not installed or
        added to the path.
        """
        if not self.local_path.exists():
            self.local_path.mkdir(parents=True, exist_ok=False)
            print("Folder does not exist. Creating...")
        try:
            _ = git.Repo(self.local_path)
        except InvalidGitRepositoryError:
            print("No Git repository known at the local path. Creating...")
            _ = git.Repo.init(self.local_path)
            self.add_origin()
            self._init_sparse_checkout()
        except OSError as exc:
            print(exc)
            print("Git is not installed or cannot be found.")
            sys.exit(1)
        self.pull_origin()

    def _init_sparse_checkout(self) -> None:
        """
        Initializes sparse checkout in the Git repository.
        Applies the 'cone' strategy for sparse checkout and adds the root
        folder of the repository.
        """

        self.repository.config_writer().set_value("core", "sparsecheckout", "true").release()
        self._set_sc_list()
        self._write_sparse_checkout()

    def _add_sparse_checkout(self, name: str) -> None:
        """
        Adds folder to sparse checkout.

        :param name: Folder to be added to sparse checkout. 
        """
        # If you add folder1/1.0/2.0 the result is
        # /folder1/
        # !/folder1/*/
        # /folder1/1.0/
        # !/folder1/1.0/*/
        # /folder1/1.0/2.0/
        self._set_sc_list()
        if name not in self.sc_list:
            self.sc_list.append(name)
            self._write_sparse_checkout()
        self.checkout_main()

    def _write_sparse_checkout(self) -> None:
        self.sc_list.sort(key=lambda x: Path(x).parts)
        write_list = ['/*\n', '!/*/\n']
        for name in self.sc_list:
            path_name_parts = Path(name).parts
            cumulative_parts = ""
            for idx, name_part in enumerate(path_name_parts):
                cumulative_parts = f"{cumulative_parts}/{name_part}"
                if f"{cumulative_parts}/\n" not in write_list:
                    write_list.append(f"{cumulative_parts}/\n")
                if idx != (len(path_name_parts) - 1):
                    if f"!{cumulative_parts}/*/\n" not in write_list:
                        write_list.append(f"!{cumulative_parts}/*/\n")

        with open(self._sparse_checkout_config_path, 'w') as fname:
            fname.writelines(write_list)

    def _check_branch_present(self, branch_name: str) -> bool:
        """
        Checks if the branch is already present locally or remotely.
        """
        local_branches = self.repository.heads
        local_branch_names = [branch.name for branch in local_branches]
        remote_branches = self.repository.remote().refs
        remote_branch_names = [r_branch.name.split('/')[-1] for r_branch in remote_branches]
        branch_present = (branch_name in local_branch_names) or (branch_name in remote_branch_names)
        return branch_present

    def _set_sc_list(self) -> None:
        self.sc_list = []


class NetworkGitRepository(GitRepository):
    def __init__(self, config: 'Config'):
        super().__init__(config)
        self.local_path = self.config.networks_folder
        self.remote_url = self.config.repository_urls['networks_git']
        print("Initializing network repository...")
        self._init_repository()
        print("Done.")

    @property
    def installed_list(self) -> Union[List[PackageInfo], List[Any]]:
        installed_list = []
        if self.config.network_record_path.exists():
            with open(self.config.network_record_path, 'r') as fname:
                json_dict = json.load(fname)
                installed_list = [PackageInfo.from_dict(info) for info in json_dict.values()]
        return installed_list

    def folder_path(self, package_info: 'PackageInfo') -> Path:
        return self.local_path / package_info.name / package_info.package_version

    def _set_sc_list(self) -> None:
        self.sc_list = [str(self.folder_path(info).relative_to(self.local_path))
                        for info in self.installed_list]


class ToolGitRepository(GitRepository):
    def __init__(self, config: 'Config'):
        super().__init__(config)
        self.local_path = self.config.tools_folder
        self.remote_url = self.config.repository_urls['tools_git']
        print("Initializing tools repository...")
        self._init_repository()
        print("Done.")

    @property
    def installed_list(self) -> Union[List[PackageInfo], List[Any]]:
        installed_list = []
        if self.config.tool_record_path.exists():
            with open(self.config.tool_record_path, 'r') as fname:
                json_dict = json.load(fname)
                installed_list = [PackageInfo.from_dict(info) for info in json_dict.values()]
        return installed_list

    def folder_path(self, package_info: 'PackageInfo') -> Path:
        return self.local_path / package_info.name / package_info.version / package_info.package_version

    def pull_origin(self) -> None:
        super().pull_origin()
        if (self.local_path / 'datatypes').exists():
            shutil.copytree(self.local_path / 'datatypes', self.config.datatypes_folder,
                            dirs_exist_ok=True)

    def _set_sc_list(self) -> None:
        self.sc_list = ['datatypes'] + [str(self.folder_path(info).relative_to(self.local_path))
                                        for info in self.installed_list]


class ContainerRepository(RepositoryBackEnd):
    def __init__(self, config: 'Config'):
        super().__init__(config)
        self.config = config
        self.remote_url = self.config.repository_urls['tools_docker']
        self.client = None
        self.available = False
        self.repository_available = False

        if self.config.container_type:
            self.backends = {container: None for container in self.config.container_type}
        else:
            self.backends = {
                'docker': None,
            }

        if type(self) == ContainerRepository:
            if 'docker' in self.backends.keys():
                self.backends['docker'] = DockerRepositoryBackEnd(self.config)
            if 'singularity' in self.backends.keys():
                self.backends['singularity'] = SingularityRepositoryBackEnd(self.config)
            if 'singularity_slurm' in self.backends.keys():
                self.backends['singularity_slurm'] = SingularitySlurmRepositoryBackEnd(self.config)

        self._instantiate_client()
        # Test repository connection
        self._ping_repository()

    def pull(self, container_info: dict) -> None:
        if not self.available:
            print("Not pulling a container: no container functionality available.")
            return
        if self.repository_available:
            for container in self.config.container_type:
                backend = self.backends[container]
                if backend.available and backend.repository_available:
                    backend.pull(container_info)
                    return
        else:
            print("Not pulling a container: no container repositories available.")

    def _instantiate_client(self) -> None:
        available_list = []
        for container in self.config.container_type:
            if container in self.backends.keys():
                available_list.append(self.backends[container].available)
            else:
                print(f"Support for container type {container} not implemented.")
        self.available = any(available_list)

    def _ping_repository(self) -> None:
        if self.available:
            available_list = []
            for container in self.config.container_type:
                if (container in self.backends.keys()) and self.backends[container].available:
                    available_list.append(self.backends[container].repository_available)
            self.repository_available = any(available_list)
        else:
            print("No container system initialized locally. Running Networks will not be possible!")


class DockerRepositoryBackEnd(ContainerRepository):
    def __init__(self, config: 'Config'):
        super().__init__(config)

    def pull(self, container_info: dict) -> None:
        """
        Retrieves the Docker image for a tool.

        :param container_info: Dictionary containing information on the container.
        """
        print("Getting the Docker image...")
        name = container_info['name']
        version = container_info['package_version']
        image_version = container_info['image_version']
        if container_info['dockerurl'] is not None:
            repository = container_info['dockerurl']
        else:
            repository = '/'.join([self.remote_url, name])
        if self.client is None:
            print(f"Local Docker repository is not initialized. Not pulling image {name}:{version}.")
            return
        if not self.repository_available:
            print(f"Docker repository flagged as 'not available'. Not pulling image {name}:{version}.")
            return
        try:
            image = self.client.images.pull(repository, tag=image_version)
        except Exception as exc:
            raise FastrPIDockerError(f"Failed to get Docker image {name}:{version}.") from exc
        else:
            image.tag(name, tag=version)  # type: ignore
            print("Done.")

    def _instantiate_client(self) -> None:
        """
        Instantiate Docker client.
        """
        try:
            self.client = docker.from_env()
            self.available = True
        except Exception as exc:
            self.available = False
            print("Docker could not be initialized.")

    def _ping_repository(self) -> None:
        repository = '/'.join([self.remote_url, 'ping'])
        if self.client is not None:
            try:
                _ = self.client.images.pull(repository, tag='1.0')
            except APIError:
                print("Can't reach the Docker repository. Check if you are logged in.")
            else:
                print("Remote Docker repository available through Docker.")
                self.repository_available = True
        else:
            self.repository_available = False


class SingularityRepositoryBackEnd(ContainerRepository):
    def __init__(self, config: 'Config'):
        super().__init__(config)

    def pull(self, container_info: dict) -> None:
        """
        Retrieves the Docker image for a tool.

        :param container_info: Dictionary containing information on the container.
        """
        print("Getting the Docker image through Singularity...")
        name = container_info['name']
        version = container_info['package_version']
        image_version = container_info['image_version']
        if container_info['dockerurl'] is not None:
            repository = container_info['dockerurl']
        else:
            repository = '/'.join([self.remote_url, name])

        if self.available and self.repository_available:
            command_list = ['singularity', 'pull', '--disable-cache',
                            str(self.config.singularity_dir / f'{name}_{version}.sif'),
                            f'docker://{repository}:{image_version}']
            try:
                # command_list = ['singularity', 'pull',
                #                 str(self.config.singularity_dir / f'{name}_{version}.sif'),
                #                 f'docker://{repository}:{image_version}']
                _ = subprocess.Popen(command_list,
                                     stdout=subprocess.DEVNULL,
                                     stderr=subprocess.STDOUT).wait()
            except Exception as exc:
                raise FastrPIDockerError(f"Failed to get Docker image {name}:{version}.") from exc
            else:
                print("Done.")
        else:
            print("Singularity is not available or the Docker repository is not available. "
                  + f"Not pulling image {name}:{version}.")

    def _instantiate_client(self) -> None:
        """
        Instantiate Singularity client.
        """
        try:
            command_list = ['singularity', '--help']
            _ = subprocess.Popen(command_list,
                                 stdout=subprocess.DEVNULL,
                                 stderr=subprocess.STDOUT).wait()
            self.available = True
        except Exception as exc:
            print("Singularity could not be initialized.")
            self.available = False

    def _ping_repository(self) -> None:
        if self.available:
            try:
                command_list = ['singularity', 'pull', '--disable-cache',
                                f'{self.config.singularity_dir}/ping_1.0.sif',
                                f'docker://{self.remote_url}/ping:1.0']
                _ = subprocess.Popen(command_list,
                                     stdout=subprocess.DEVNULL,
                                     stderr=subprocess.STDOUT).wait()
            except Exception as exc:
                print("Can't reach the Docker repository from Singularity. Check if you are logged in.")
                raise FastrPIDockerError from exc
            else:
                print("Remote Docker repository available through Singularity.")
                self.repository_available = True
        else:
            self.repository_available = False


class SingularitySlurmRepositoryBackEnd(SingularityRepositoryBackEnd):
    def __init__(self, config: 'Config'):
        super().__init__(config)
        self.job_id = None

    def pull(self, container_info: dict) -> None:
        """
         Retrieves the Docker image for a tool.

         :param container_info: Dictionary containing information on the container.
         """
        print("Getting the Docker image through Singularity...")
        name = container_info['name']
        image_version = container_info['image_version']
        version = container_info['package_version']
        if container_info['dockerurl'] is not None:
            repository = container_info['dockerurl']
        else:
            repository = '/'.join([self.remote_url, name])

        if self.available and self.repository_available:
            try:
                if self.config.slurm_pull_partition:
                    sbatch_partition = f"sbatch --partition={self.config.slurm_pull_partition} "
                else:
                    print("No partition is set for pulling container over Slurm. Slurm will fallback to the default.")
                    sbatch_partition = f"sbatch "
                command_list = ['bash', '-c', sbatch_partition +
                                '--job-name=fastrpi_pull ' +
                                '--cpus-per-task=1 ' +
                                '--mem=4G ' +
                                '--wrap=' +
                                "'/usr/bin/singularity pull --disable-cache " +
                                str(self.config.singularity_dir / f'{name}_{version}.sif') +
                                f" docker://{repository}:{image_version}'"]
                submission = subprocess.run(command_list, capture_output=True, env=os.environ) 
                if submission.returncode != 0:
                    raise FastrPIDockerError("Slurm submission failed.")
                self.job_id = submission.stdout.split()[-1]
                print(f"Slurm batch job: {str(self.job_id)}")
                sleep(30)
                while self._check_slurm_status():
                    sleep(30)

            except FastrPIDockerError as exc:
                raise FastrPIDockerError(f"Failed to get Docker image {name}:{version}.") from exc
            except Exception as exc:
                raise FastrPIDockerError(f"Failed to get Docker image {name}:{version}.") from exc
            else:
                print("Done.")
        else:
            print("Singularity is not available or the Docker repository is not available. "
                  + f"Not pulling image {name}:{version}.")

    def _check_slurm_status(self):
        command = ['sacct', '-j', self.job_id, '--format', 'State']
        status_check = subprocess.run(command, capture_output=True)
        if status_check.returncode != 0:
            sleep(60)
            status_check = subprocess.run(command, capture_output=True)
            if status_check.returncode != 0:
                raise FastrPIDockerError("Unable to check Slurm status")
        status = status_check.stdout.split()
        if b"PENDING" in status[2:] or b"RUNNING" in status[2:]:
            return True
        if all([status_state == b"COMPLETED" for status_state in status[2:]]):
            return False
        raise FastrPIDockerError(f"Slurm job for Singularity pull seems to have failed: {status}")

    def _instantiate_client(self) -> None:
        print("Using Singularity Slurm backend: Singularity availability check will be skipped.")
        self.available = True

    def _ping_repository(self) -> None:
        print("Using Singularity Slurm backend: repository availability check will be skipped.")
        self.repository_available = True
