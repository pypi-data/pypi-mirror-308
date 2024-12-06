import json
import shutil
from abc import abstractmethod
from typing import TYPE_CHECKING, List

import fastrpi
from .exceptions import (FastrPIAlreadyInstalled, FastrPIDockerError,
                         FastrPIGitError, FastrPIInstallError,
                         FastrPIPublishError)
from .package import Package
from .packageinfo import PackageInfo
from .repositorybackend import (ContainerRepository, NetworkGitRepository,
                                ToolGitRepository)

if TYPE_CHECKING:
    from .config import Config


class PackageRepository(object):
    """ Package repository API 
    
    To encapsulate the technical implementation of the package storage, the
    PackageRepository objects are used to form a facade.
    """

    def __init__(self, config: 'Config') -> None:
        self.config = config
        self._backends = {}

    @property
    def avail_packages_info(self) -> List[PackageInfo]:
        avail_packages = []
        return avail_packages

    @property
    def avail_packages(self) -> List:
        avail_packages = []
        return avail_packages

    @abstractmethod
    def install(self, package_info: PackageInfo) -> Package:
        pass

    def publish(self, package: Package) -> None:
        git_backend = self._backends['git']
        package_folder = git_backend.folder_path_package(package)
        package.run_checks()
        try:
            git_backend.push(package)
        except (FastrPIGitError, FastrPIPublishError) as exc:
            print(exc.message)
            if package_folder.exists():
                shutil.rmtree(package_folder)
            raise FastrPIPublishError from exc
        finally:
            git_backend.remove_sparse_checkout(
                str(package_folder.relative_to(git_backend.local_path)))
            git_backend.checkout_main()
            git_backend.delete_draft_branch()

    def check_available(self, package_info: PackageInfo) -> bool:
        return package_info in self.avail_packages


class ToolPackageRepository(PackageRepository):
    def __init__(self, config: 'Config') -> None:
        super().__init__(config)
        self._backends['git'] = ToolGitRepository(config)
        self._backends['container'] = ContainerRepository(config)

    @property
    def avail_packages(self) -> List[PackageInfo]:
        metadata_path = self.config.tools_folder / self.config.metadata_path
        with open(metadata_path, 'r') as fname:
            metadata_json = json.load(fname)

        avail_packages = []
        for metadata_dict in metadata_json.values():
            avail_packages.append(
                PackageInfo.from_dict(metadata_dict)
            )
        return sorted(avail_packages, key=lambda x: x.tag)

    @property
    def avail_datatypes(self) -> List:
        # Add default Fastr Datatypes that aren't in the FastrPI repository.
        avail_datatypes = ['AnyFile', 'AnyType', 'Deferred', 'Missing']
        filelist = self._backends['git'].filelist

        for filepath in filelist:
            if filepath.parts[0] == 'datatypes':
                datatype = filepath.stem
                avail_datatypes.append(datatype)
        avail_datatypes.remove('__init__')
        return sorted(list(set(avail_datatypes)))

    def install(self, package_info: PackageInfo) -> None:
        try:
            if not fastrpi.tool_install_record.check_installed(package_info):
                if self.check_available(package_info):
                    manifest = self._backends['git'].pull(package_info)
                    if manifest['package_type'] == 'macronode':
                        fastrpi.tool_install_record.add(Package.create(manifest))
                        self.install_macronode(manifest)
                    if manifest.container is not None:
                        self._backends['container'].pull(manifest.container)
                    fastrpi.tool_install_record.add(Package.create(manifest))
                else:
                    print(f"Tool {package_info} is not available.")
                    raise FastrPIInstallError
            else:
                raise FastrPIAlreadyInstalled(f"Tool {package_info} is already installed.")
        except (FastrPIGitError, FastrPIDockerError, KeyboardInterrupt) as exc:
            print(exc)
            try:
                fastrpi.tool_install_record.remove(Package.create(manifest).tag)
            except UnboundLocalError:
                pass
            tool_folder = self._backends['git'].folder_path(package_info)
            git_repo_folder = self._backends['git'].local_path
            self._backends['git'].remove_sparse_checkout(str(tool_folder.relative_to(git_repo_folder)))
            if tool_folder.is_dir():
                shutil.rmtree(tool_folder)
            raise FastrPIInstallError from exc

    def install_macronode(self, manifest: 'Manifest') -> None:
        network_package_info = PackageInfo(
            name=manifest['network_name'],
            package_version=manifest['version'])
        try:
            fastrpi.network_package_repo.install(network_package_info)
        except FastrPIAlreadyInstalled as exc:
            print(exc.message)
        except FastrPIInstallError as exc:
            print(exc.message)
            raise FastrPIInstallError from exc
        # Symlink network
        network_package = fastrpi.network_install_record.load_package(network_package_info)
        symlink_target = network_package.manifest.folder / network_package.manifest['network']
        network_symlink = manifest.folder / f"{network_package.tag}.py"
        network_symlink.symlink_to(symlink_target)


class NetworkPackageRepository(PackageRepository):
    def __init__(self, config: 'Config') -> None:
        super().__init__(config)
        self._backends['git'] = NetworkGitRepository(config)

    @property
    def avail_packages(self) -> List[PackageInfo]:
        metadata_path = self.config.networks_folder / self.config.metadata_path
        with open(metadata_path, 'r') as fname:
            metadata_json = json.load(fname)

        avail_packages = []
        for metadata_dict in metadata_json.values():
            avail_packages.append(
                PackageInfo.from_dict(metadata_dict)
            )
        return sorted(avail_packages, key=lambda x: x.tag)

    def install(self, package_info: PackageInfo) -> None:
        try:
            if not fastrpi.network_install_record.check_installed(package_info):
                if self.check_available(package_info):
                    print(f"Pulling network {package_info}")
                    manifest = self._backends['git'].pull(package_info)
                    fastrpi.network_install_record.add(Package.create(manifest))
                    for tool in manifest['tool_packages']:
                        try:
                            fastrpi.tool_package_repo.install(
                                PackageInfo(name=tool['name'],
                                            version=tool['version'],
                                            package_version=tool['package_version']))
                        except FastrPIAlreadyInstalled as exc:
                            print(exc.message)
                        except FastrPIInstallError as exc:
                            print(exc.message)
                            raise FastrPIInstallError from exc
                else:
                    raise FastrPIInstallError(f"Network {package_info} is not available.")
            else:
                raise FastrPIAlreadyInstalled(f"Network {package_info} is already installed.")
        except (FastrPIInstallError, FastrPIGitError, KeyboardInterrupt) as exc:
            print(exc)
            network_folder = self._backends['git'].folder_path(package_info)
            git_repo_folder = self._backends['git'].local_path
            self._backends['git'].remove_sparse_checkout(str(network_folder.relative_to(git_repo_folder)))
            fastrpi.network_install_record.remove(package_info.tag)
            if network_folder.exists():
                shutil.rmtree(network_folder)
            raise FastrPIInstallError from exc
