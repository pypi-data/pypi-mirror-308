from collections import UserDict
from copy import deepcopy
from pathlib import Path
from typing import Dict, List, Union

from ruamel.yaml import YAML
from schema import Schema, SchemaError, Use

from .exceptions import FastrPIManifestError
from .helpers import check_valid_yaml, read_yaml, walk_dict_list
from .manifest_schemas import (MacroNodeManifestSchema, NetworkManifestSchema,
                               ToolManifestSchema)


class Manifest(UserDict):
    """
    Manifest object

    Contains the content of the package manifest. After the manifest YAML
    file is loaded, the data is stored in this object as if it were
    a dictionary. Derivative variables are accessed through property methods.
    """
    _CLASS_TYPE = 'package'
    subclasses = {}

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        cls.subclasses[cls._CLASS_TYPE] = cls

    @classmethod
    def create(cls, manifest_path: Union[Path, str]) -> 'Manifest':
        manifest_path = Path(manifest_path)
        if not check_valid_yaml(manifest_path):
            raise FastrPIManifestError("Manifest is not valid YAML.")
        data = read_yaml(manifest_path)
        try:
            package_type = data['package_type']
        except KeyError:
            raise FastrPIManifestError("Manifest must contain 'package_type'")
        return cls.subclasses[package_type](manifest_path)

    def __init__(self, manifest_path: Union[Path, str],  **kwargs):
        """
        Initialize a Manifest object.

        :param manifest_path: Path to manifest YAML file.
        """
        super().__init__(self, **kwargs)
        self.path = manifest_path
        self.folder = self.path.parent
        self._package_specific_init()

        self.yaml = YAML()
        self._check_valid_yaml()
        self._load_file()
        self.update(**kwargs)
        self._cast_types()

    @property
    def container(self) -> Union[Dict[str, str], None]:
        """
        Information on the associated Docker container for the appropriate `package_type`.
        Returns None when `package_type` has no associated container.

        :return: Dictionary with keys `name`, `version`, `image` and `dockerurl` or None
        """
        print(f"Package type {self['package_type']} has no associated container.")
        return None

    @property
    def files(self) -> List[Path]:
        """
        List of files which are part of the package. Predominantly used for
        moving and copying these files.
        """
        filelist = [self.path.resolve()]

        for var in self.file_vars:
            try:
                if isinstance(var, list):
                    itemlist = self[var[0]]
                    for item in itemlist:
                        if ((var[0] == 'files') and item['type'] != 'local'):
                            continue
                        filepath = item[var[1]]
                        filelist.append(filepath)
                else:
                    filepath = self[var]
                    filelist.append(filepath)
            except KeyError:
                pass
        filelist = [(self.folder / filepath).resolve() for filepath in filelist]
        return filelist

    def update_file(self) -> None:
        """
        Update manifest YAML file after changing it.
        """
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

        data_obj = deepcopy(self.data)
        data_obj = walk_dict_list(data_obj)
        with open(self.path, 'w') as fname:
            self.yaml.dump(data_obj, fname)

    def run_checks(self) -> None:
        """
        Run checks to validate the manifest file.
        """
        self._check_valid_yaml()
        print("Manifest is valid YAML.")
        self._check_schema()

    def _package_specific_init(self) -> None:
        self.file_vars = []
        self.schema = Schema({
            'name': Use(str),
            'package_type': Use(str)})

    def _load_file(self) -> None:
        with open(self.path, 'r') as fname:
            data = self.yaml.load(fname)
        self.update(data)

    def _check_valid_yaml(self) -> None:
        if not check_valid_yaml(self.path):
            raise FastrPIManifestError("Manifest is not valid YAML.")

    def _check_schema(self) -> None:
        _ = self._validate_schema()

    def _validate_schema(self) -> Dict:
        if 'package_type' not in self.keys():
            raise FastrPIManifestError("Manifest must contain 'package_type'")
        try:
            validated = self.schema.validate(self.data)
        except SchemaError as schemaexc:
            raise FastrPIManifestError(f"Manifest schema is not valid. {schemaexc}") from None
        return validated

    def _cast_types(self) -> None:
        self.update(self._validate_schema())


class ToolManifest(Manifest):
    _CLASS_TYPE = 'tool'

    def __init__(self, manifest_path: Union[Path, str],  **kwargs):
        super().__init__(manifest_path, **kwargs)

    def _package_specific_init(self) -> None:
        self.file_vars = ['dockerfile', 'license',
                          ['tools', 'tool_definition'],
                          ['tools', 'license'],
                          ['files', 'path']]
        self.schema = ToolManifestSchema(self.folder)

    @property
    def container(self) -> Dict[str, str]:
        """
        Information on the associated Docker container for the appropriate `package_type`.
        Raises FastrPIDockerError when `package_type` has no associated container.

        :return: Dictionary with keys `name`, `version`, `image` and 'dockerurl'.
        """

        container_dict = {
            "name": f"{self['name']}-v{self['version']}",
            "package_version": self['package_version'],
            "image": f"{self['name']}-v{self['version']}:{self['package_version']}",
            "image_version": self['package_version'],
            "dockerurl": None
        }
        try:
            if self['external_container']:
                container_dict['dockerurl'] = self['dockerurl'].split(':')[0]
                container_dict['image_version'] = self['dockerurl'].split(':')[-1]
        except KeyError:
            pass
        return container_dict


class MacroNodeManifest(Manifest):
    _CLASS_TYPE = 'macronode'

    def __init__(self, manifest_path: Union[Path, str],  **kwargs):
        super().__init__(manifest_path, **kwargs)

    def _package_specific_init(self) -> None:
        self.file_vars = ['license',
                          ['tools', 'tool_definition'],
                          ['tools', 'license'],
                          ['files', 'path']]
        self.schema = MacroNodeManifestSchema(self.folder)


class NetworkManifest(Manifest):
    _CLASS_TYPE = 'network'

    def __init__(self, manifest_path: Union[Path, str],  **kwargs):
        super().__init__(manifest_path, **kwargs)

    def _package_specific_init(self) -> None:
        self.file_vars = ['license',
                          'network',
                          'readme',
                          ['files', 'path']]
        self.schema = NetworkManifestSchema(self.folder)
