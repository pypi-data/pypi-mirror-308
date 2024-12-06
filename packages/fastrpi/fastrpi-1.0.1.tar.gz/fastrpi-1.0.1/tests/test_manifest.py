from pathlib import Path
import pytest
from schema import SchemaError

import fastrpi
from fastrpi.manifest import Manifest, MacroNodeManifest, NetworkManifest, ToolManifest
from fastrpi.exceptions import FastrPIManifestError


def test_correct_manifests(correct_manifests_path, correct_manifests_dict,
        correct_files_dict):
    correct_manifests_dict, correct_container_dict = correct_manifests_dict
    print("Testing:")
    for package_type in correct_manifests_path.keys():
        print(f"{package_type}...")
        manifest_path = correct_manifests_path[package_type]
        manifest_dict = correct_manifests_dict[package_type]
        files_list = [Path(fname).resolve() for fname in correct_files_dict[package_type]]
        container_dict = correct_container_dict[package_type]
        # Also test if `manifest_path` is str
        _ = Manifest.create(str(manifest_path))
        manifest_obj = Manifest.create(manifest_path)
        assert manifest_obj.path == Path(manifest_path)
        assert manifest_obj.folder == Path(manifest_path).parent
        assert manifest_obj == manifest_dict
        assert sorted(manifest_obj.files) == sorted(files_list)
        assert manifest_obj.container == container_dict
        manifest_obj.run_checks()


def test_acceptable_manifests(acceptable_manifests_path):
    for package_type, pathname in acceptable_manifests_path.items():
        print(package_type)
        _ = Manifest.create(pathname)


def test_incorrect_manifests(incorrect_manifests_path):
    for package_type, pathname in incorrect_manifests_path.items():
        print(f"{package_type}...")
        print(pathname)
        with pytest.raises(FastrPIManifestError) as exc:
            _ = Manifest.create(pathname)


def test_update_manifest(updatable_manifest_path):
    manifest_obj = Manifest.create(updatable_manifest_path)
    tool_license_path = updatable_manifest_path.parent / 'LICENSE_addint'
    tool_license_path.touch()
    manifest_obj['tools'][0]['license'] = str(tool_license_path)
    manifest_obj.update_file()
    manifest_obj = Manifest.create(updatable_manifest_path)
    assert manifest_obj['tools'][0]['license'] == tool_license_path


def test_manifest_create_unvalidyaml(tmp_path, monkeypatch):
    monkeypatch.setattr("fastrpi.manifest.check_valid_yaml", lambda x: False)
    with pytest.raises(FastrPIManifestError, match="Manifest is not valid YAML."):
        _ = Manifest.create(tmp_path)


def test_manifest_create_unvalidyaml_meth(tmp_path, monkeypatch, correct_manifests):
    monkeypatch.setattr("fastrpi.manifest.check_valid_yaml", lambda x: False)
    for manifest_type, manifest in correct_manifests.items():
        with pytest.raises(FastrPIManifestError, match="Manifest is not valid YAML."):
            _ = manifest._check_valid_yaml()


def test_manifest_create_nopackagetype(tmp_path, monkeypatch):
    monkeypatch.setattr("fastrpi.manifest.check_valid_yaml", lambda x: True)
    monkeypatch.setattr("fastrpi.manifest.read_yaml", lambda x: {})
    with pytest.raises(FastrPIManifestError, match="Manifest must contain 'package_type'"):
        _ = Manifest.create(tmp_path)


def test_manifest_create_tool_type(tmp_path, monkeypatch, mocker):
    monkeypatch.setattr("fastrpi.manifest.check_valid_yaml", lambda x: True)
    monkeypatch.setattr("fastrpi.manifest.read_yaml", lambda x: {'package_type': 'tool'})
    mocker.patch("fastrpi.manifest.Manifest.__init__")
    manifest = Manifest.create(tmp_path)
    assert isinstance(manifest, ToolManifest)


def test_manifest_create_network_type(tmp_path, monkeypatch, mocker):
    monkeypatch.setattr("fastrpi.manifest.check_valid_yaml", lambda x: True)
    monkeypatch.setattr("fastrpi.manifest.read_yaml", lambda x: {'package_type': 'network'})
    mocker.patch("fastrpi.manifest.Manifest.__init__")
    manifest = Manifest.create(tmp_path)
    assert isinstance(manifest, NetworkManifest)


def test_manifest_create_macro_type(tmp_path, monkeypatch, mocker):
    monkeypatch.setattr("fastrpi.manifest.check_valid_yaml", lambda x: True)
    monkeypatch.setattr("fastrpi.manifest.read_yaml", lambda x: {'package_type': 'macronode'})
    mocker.patch("fastrpi.manifest.Manifest.__init__")
    manifest = Manifest.create(tmp_path)
    assert isinstance(manifest, MacroNodeManifest)


def test_manifest_validate_schema_notype(correct_manifests, monkeypatch):
    for manifest_type, manifest in correct_manifests.items():
        monkeypatch.setattr(manifest, 'keys', lambda: {})
        with pytest.raises(FastrPIManifestError, match="Manifest must contain 'package_type'"):
            manifest._validate_schema()


# def test_manifest_validate_schema_error(correct_manifests, mocker):
#     for manifest_type, manifest in correct_manifests.items():
#         mocker.patch(
#            "fastrpi.manifest.Manifest.schema",
#            side_effect=SchemaError
#         )
#         with pytest.raises(FastrPIManifestError, match="Manifest schema is not valid."):
#             manifest._validate_schema()
