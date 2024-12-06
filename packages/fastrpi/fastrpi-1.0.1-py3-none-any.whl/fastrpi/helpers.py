import importlib.machinery
import importlib.util
from pathlib import Path

import yaml
from ruamel.yaml import YAML
from yaml.parser import ParserError
from yaml.scanner import ScannerError

from .exceptions import FastrPIRunError

ruamel_yaml = YAML()


def load_module_from_file(filepath: Path, module_name: str):
    """
    Loads Python file as module. Used in the `run` command.

    :param filepath: Python file
    :param module_name: Name to give the module.
    :return mymodule: Loaded module.
    """
    try:
        loader = importlib.machinery.SourceFileLoader(module_name, str(filepath))
        spec = importlib.util.spec_from_loader(module_name, loader)
        if spec is None:
            raise FastrPIRunError("Spec from spec_from_loader is None")
        mymodule = importlib.util.module_from_spec(spec)
        loader.exec_module(mymodule)
    except Exception as exc:
        print(f"Error message: {exc}.")
        raise FastrPIRunError(f"Failed to retrieve module from {filepath}.") from exc
    return mymodule


def check_valid_yaml(path: Path) -> bool:
    """
    Check if the YAML file at `path` is valid YAML and can be loaded.

    :param path: Path to a YAML file.
    :return: True if valid, False if not.
    """
    with open(path, 'r') as yaml_file:
        try:
            _ = yaml.safe_load(yaml_file)
            return True
        except (ScannerError, ParserError) as exc:
            print(exc)
            return False


def read_yaml(yaml_path: Path) -> dict:
    """
    Read in a YAML file.

    :param yaml_path: Path to the YAML file.
    :return data: Dictionary.
    """
    with open(yaml_path, 'r') as stream:
        data = ruamel_yaml.load(stream)
    return data


def write_yaml(data: dict, yaml_path: Path) -> None:
    """
    Write to a YAML file.

    :param data: Data to write
    :param yaml_path: Path to the YAML file.
    """
    with open(yaml_path, 'w') as fname:
        _ = ruamel_yaml.dump(data, fname)


def walk_dict_list(d):
    if isinstance(d, dict):
        for k, v in d.items():
            if isinstance(v, (dict, list)):
                d[k] = walk_dict_list(v)
            elif isinstance(v, Path):
                d[k] = str(v)
            else:
                pass
    elif isinstance(d, list):
        for idx, item in enumerate(d):
            if isinstance(item, (dict, list)):
                d[idx] = walk_dict_list(item)
            elif isinstance(item, Path):
                d[idx] = str(item)
            else:
                pass
    return d
