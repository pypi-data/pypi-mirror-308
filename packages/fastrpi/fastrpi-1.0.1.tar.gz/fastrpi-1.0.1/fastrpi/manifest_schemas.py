from pathlib import Path

from schema import And, Optional, Or, Schema, Use


def ToolManifestSchema(folder: Path):
    manifestschema = Schema({
                'name': Use(str),
                'version': Use(str),
                'package_type': 'tool',
                'package_version': Use(str),
                Or('dockerfile', 'dockerurl', only_one=True):
                    Or(And(Use(Path), lambda p: (folder / p).exists()), Use(str)),
                'license': And(Use(Path), lambda p: (folder / p).exists()),
                'tools': [
                    {'tool_definition': And(Use(Path), lambda p: (folder / p).exists()),
                     Optional('license'): And(Use(Path), lambda p: (folder / p).exists())}
                ],
                'required_datatypes': [str],
                Optional('files'): [
                    {'type': 'local',
                     'path': And(Use(Path), lambda p: (folder / p).exists())}
                ]}, ignore_extra_keys=True)
    return manifestschema


def MacroNodeManifestSchema(folder: Path):
    manifestschema = Schema({
            'name': And(Use(str), lambda name: name.startswith('macro_')),
            'network_name': Use(str),
            'version': Use(str),
            'package_type': Use(str),
            'package_version': Use(str),
            'license': And(Use(Path), lambda p: (folder / p).exists()),
            'tools': [
                {'tool_definition': And(Use(Path), lambda p: (folder / p).exists()),
                 Optional('license'): And(Use(Path), lambda p: (folder / p).exists())}
            ],
            Optional('files'): [
                {'type': 'local',
                 'path': And(Use(Path), lambda p: (folder / p).exists())}
            ]}, ignore_extra_keys=True)
    return manifestschema


def NetworkManifestSchema(folder: Path):
    manifestschema = Schema({
            'name': Use(str),
            'package_version': Use(str),
            'package_type': 'network',
            'network': And(Use(Path), lambda p: (folder / p).exists()),
            'license': And(Use(Path), lambda p: (folder / p).exists()),
            'tool_packages': [
                {'name': Use(str),
                 'version': Use(str),
                 'package_version': Use(str)}
            ],
            'required_datatypes': [str],
            'readme': And(Use(Path), lambda p: (folder / p).exists()),
            Optional('cite'): [Use(str)],
            Optional('files'): [
                {'type': 'local',
                 'path': And(Use(Path), lambda p: (folder / p).exists())}
            ],
        }, ignore_extra_keys=True)
    return manifestschema
