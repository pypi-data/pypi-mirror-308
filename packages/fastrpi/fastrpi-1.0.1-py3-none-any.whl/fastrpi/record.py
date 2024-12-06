import json
from typing import TYPE_CHECKING, List

from .exceptions import FastrPINotInstalled
from .manifest import Manifest
from .package import NetworkPackage, Package, ToolPackage
from .packageinfo import PackageInfo

if TYPE_CHECKING:
    from .config import Config


class InstallRecord(object):
    """ Install Record
    
    The InstallRecord object keeps track of the installed packages.
    """

    def __init__(self, config: 'Config'):
        self.config = config
        self.record_path = config.fastrpi_home / 'installed.json'
        self._packages = {}
        self._package_type = Package

    @property
    def installed_packages(self) -> List[PackageInfo]:
        installed_packages_list = [pack for pack in self._packages.keys()]
        package_info_list = [PackageInfo.from_dict(self._packages[key]) for key in installed_packages_list]
        return package_info_list

    def check_installed(self, package_info: PackageInfo) -> bool:
        return package_info in self.installed_packages

    def load_package(self, package_info: 'PackageInfo') -> Package:
        if not self.check_installed(package_info):
            not_installed_message = f"{self._package_type.package_type} {package_info} is not installed."
            raise FastrPINotInstalled(not_installed_message)
        tag = package_info.tag
        manifest = Manifest.create(self._packages[tag]['manifest'])
        return Package.create(manifest)

    def add(self, package: 'Package') -> None:
        package_dict = {
            'name': package.name,
            'package_version': package.package_version,
            'manifest': str(package.manifest.path)
        }
        if package.tag not in self._packages.keys():
            self._packages[package.tag] = package_dict
        self._write_record()

    def remove(self, package_tag: str) -> None:
        if package_tag in self._packages.keys():
            del self._packages[package_tag]
        self._write_record()

    def _init_record(self) -> None:
        if not self.record_path.exists():
            self._write_record()
        else:
            self._load_record()

    def _load_record(self) -> None:
        with open(self.record_path, 'r') as fname:
            json_dict = json.load(fname)
            self._packages = json_dict

    def _write_record(self) -> None:
        with open(self.record_path, 'w') as fname:
            json.dump(self._packages, fname, indent=4)


class ToolInstallRecord(InstallRecord):
    def __init__(self, config: 'Config'):
        super().__init__(config)
        self.record_path = self.config.tool_record_path
        self._package_type = ToolPackage
        self._init_record()

    def add(self, package: 'ToolPackage') -> None:
        package_dict = {
            'name': package.name,
            'version': package.version,
            'package_version': package.package_version,
            'manifest': str(package.manifest.path)
        }
        self._packages[package.tag] = package_dict
        self._write_record()


class NetworkInstallRecord(InstallRecord):
    def __init__(self, config: 'Config'):
        super().__init__(config)
        self.record_path = self.config.network_record_path
        self._package_type = NetworkPackage
        self._init_record()
