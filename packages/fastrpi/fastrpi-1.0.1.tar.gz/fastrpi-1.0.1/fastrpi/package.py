import shutil
from pathlib import Path
from typing import TYPE_CHECKING

from .checks import (MacroNodePackageChecks, NetworkPackageChecks,
                     PackageChecks, ToolPackageChecks)
from .exceptions import FastrPINotInstalled
from .helpers import load_module_from_file
from .packageinfo import PackageInfo

if TYPE_CHECKING:
    from .manifest import Manifest


class Package(object):
    _CLASS_TYPE = 'package'
    subclasses = {}
    package_type = 'Package'

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        cls.subclasses[cls._CLASS_TYPE] = cls

    @classmethod
    def create(cls, manifest: 'Manifest') -> 'Package':
        package_type = manifest['package_type']
        return cls.subclasses[package_type](manifest)

    def __init__(self, manifest: 'Manifest'):
        self.manifest = manifest
        self.checks = PackageChecks(self)
        if 'version' in self.manifest:
            self.info = PackageInfo(name=self.manifest['name'],
                                    version=self.manifest['version'],
                                    package_version=self.manifest['package_version'])
        else:
            self.info = PackageInfo(name=self.manifest['name'],
                                    package_version=self.manifest['package_version'])

    @property
    def tag(self) -> str:
        return self.info.tag

    @property
    def name(self) -> str:
        return self.manifest['name']

    @property
    def package_version(self) -> str:
        return self.manifest['package_version']

    def run_checks(self):
        self.checks.run_checks()

    @classmethod
    def make_tag(cls, info: PackageInfo) -> str:
        return info.tag

    def copy_files(self, dest_folder):
        for filename in self.manifest.files:
            dest_path = dest_folder / filename.relative_to(self.manifest.folder.resolve())
            if not dest_path.parent.exists():
                dest_path.parent.mkdir(parents=True)
            if filename.is_dir():
                shutil.copytree(filename, dest_path, dirs_exist_ok=True)
            else:
                shutil.copy(filename, dest_path)


class ToolPackage(Package):
    _CLASS_TYPE = 'tool'
    package_type = 'Tool'

    def __init__(self, manifest: 'Manifest'):
        super().__init__(manifest)
        self.checks = ToolPackageChecks(self)
        self.package_type = 'Tool'

    def __str__(self) -> str:
        return f"{self.info}"

    @property
    def version(self) -> str:
        return self.manifest['version']


class MacroNodePackage(ToolPackage):
    _CLASS_TYPE = 'macronode'
    package_type = 'MacroNode'

    def __init__(self, manifest: 'Manifest'):
        super().__init__(manifest)
        self.checks = MacroNodePackageChecks(self)
        self.package_type = 'MacroNode'


class NetworkPackage(Package):
    _CLASS_TYPE = 'network'
    package_type = 'Network'

    def __init__(self, manifest: 'Manifest'):
        super().__init__(manifest)
        self.checks = NetworkPackageChecks(self)
        self.package_type = 'Network'

    def __str__(self) -> str:
        return f"{self.info}"

    def run(self, source_sink_path: Path, tmp_dir: Path) -> None:
        # Run network
        network_path = self.manifest.folder / self.manifest['network']
        network_module = load_module_from_file(network_path, 'network_module')
        source_sink_module = load_module_from_file(source_sink_path,
                                                   'source_sink_module')
        network = network_module.create_network()
        source_data = source_sink_module.get_source_data()
        sink_data = source_sink_module.get_sink_data()
        network.execute(source_data, sink_data,
                        tmpdir=tmp_dir)
        pycache_path = network_path.parent / '__pycache__'
        if pycache_path.exists():
            shutil.rmtree(pycache_path)

    def copy_source_sink(self, dest_folder):
        source_sink_files = [Path('source_sink.py'), Path('source_sink_data.py')]
        source_sink_files = [self.manifest.folder.resolve() / fname for fname in source_sink_files]
        for filename in source_sink_files:
            if filename in self.manifest.files:
                dest_path = dest_folder / filename.relative_to(self.manifest.folder.resolve())
                if not dest_path.parent.exists():
                    dest_path.parent.mkdir(parents=True)
                shutil.copy(filename, dest_path)
                return
        raise FastrPINotInstalled(f"Network {self.info} does not a have a Source-Sink file.")
