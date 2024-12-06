import os
from pathlib import Path
import shutil
import pytest

from fastrpi.config import Config
from fastrpi.manifest import Manifest
from fastrpi.package import Package


@pytest.fixture
def correct_manifests_path():
    tool_manifest_path = "./tests/files/manifest/addint_tool/manifest.fastrpi_yaml"
    tool_without_files_manifest_path = "./tests/files/manifest/addint_tool/manifest_without_files.fastrpi_yaml"
    network_manifest_path = "./tests/files/manifest/addint_network/manifest.fastrpi_yaml"
    macronode_manifest_path = "./tests/files/manifest/addint_macronode/manifest.fastrpi_yaml"
    manifest_path_dict = {
        'tool': tool_manifest_path, 
        'tool-without_files': tool_without_files_manifest_path, 
        'network': network_manifest_path,
        'macronode': macronode_manifest_path,
    }
    manifest_path_dict = {packagetype: Path(pathname).resolve() 
        for packagetype, pathname in manifest_path_dict.items()}
    return manifest_path_dict


@pytest.fixture
def correct_manifests(correct_manifests_path):
    manifest_dict = {packagetype: Manifest.create(Path(pathname))
                     for packagetype, pathname in correct_manifests_path.items()
                     if packagetype in ['tool', 'network', 'macronode']}
    return manifest_dict


@pytest.fixture
def correct_packages(correct_manifests):
    package_dict = {packagetype: Package.create(manifest)
                    for packagetype, manifest in correct_manifests.items()}
    return package_dict

@pytest.fixture
def acceptable_manifests_path(tmp_path, correct_manifests_path):
    acceptable_dict = correct_manifests_path
    for package_type, pathname in correct_manifests_path.items():
        shutil.copytree(pathname.parent, tmp_path / package_type)
        acceptable_dict[package_type] = tmp_path / package_type / pathname.name
        with open(acceptable_dict[package_type], 'a') as fname:
            fname.write("extra_key: 'should_not_raise_exception'")
    yield acceptable_dict
    shutil.rmtree(tmp_path)


@pytest.fixture
def incorrect_manifests_path(tmp_path, correct_manifests_path):
    package_type_list = ['tool-without_files', 'network']
    path_dict = {package_type: pathname 
                 for package_type, pathname in correct_manifests_path.items()
                 if package_type in package_type_list}
    new_path_dict = {} 
    for package_type, pathname in path_dict.items():
        with open(pathname, 'r') as fname:
            original_lines = fname.readlines()
            num_lines = len(original_lines)
        new_names = ['-'.join([package_type, str(num)]) for num in range(num_lines)]
        for idx, name in enumerate(new_names):
            shutil.copytree(pathname.parent, tmp_path / name)
            new_path_dict[name] = tmp_path / name / pathname.name
            with open(tmp_path / name / pathname.name, 'w') as fname:
                new_lines = original_lines[:idx] + original_lines[idx+1:]
                fname.writelines(new_lines)
    print(tmp_path)
    yield new_path_dict
    shutil.rmtree(tmp_path)


@pytest.fixture
def correct_manifests_dict():
    manifest_dict = {
        'tool': {
            'name': 'addint',
            'version': '1.0',
            'package_type': 'tool',
            'package_version': '1.0',
            'dockerfile': Path("./Dockerfile"),
            'license': Path("./LICENSE"),
            'tools': [
                {'tool_definition': Path("./addint.yaml"), }
            ],
            'required_datatypes': ['Int'],
            'files': [{
                 'type': 'local',
                 'path': Path("./bin/"),
                 }]
            },
        'tool-without_files': {
            'name': 'addint',
            'version': '1.0',
            'package_type': 'tool',
            'package_version': '1.0',
            'dockerfile': Path("./Dockerfile"),
            'license': Path("./LICENSE"),
            'tools': [
                {'tool_definition': Path("./addint.yaml"), }
            ],
            'required_datatypes': ['Int'],
            },
        'network': {
            'name': 'addint',
            'package_type': 'network',
            'package_version': '1.0',
            'network': Path("./network.py"),
            'license': Path("./LICENSE"),
            'readme': Path("./README.md"),
            'cite': ["@article{vanrossum1995python, title={Python reference manual}, author={vanRossum, Guido}, journal={Department of Computer Science [CS]}, number={R 9525}, year={1995}, publisher={CWI}}"],
            'required_datatypes': ['Int'],
            'tool_packages': [
                {'name': 'addint',
                 'version': '1.0',
                 'package_version': '1.0'}],
        },
        'macronode': {
            'name': 'macro_addint',
            'network_name': 'addint',
            'package_type': 'macronode',
            'package_version': '1.0',
            'version': '1.0.0',
            'license': Path("./LICENSE"),
            'tools': [
                {'tool_definition': Path('./macro_addint.yaml'),
                 'license': Path('./LICENSE_macro_addint'),
                }],
        }
    }
    container_dict = {
        'tool': {
            'name': 'addint-v1.0',
            'package_version': '1.0',
            'image': 'addint-v1.0:1.0',
            'image_version': '1.0',
            'dockerurl': None
        },
        'tool-without_files': {
            'name': 'addint-v1.0',
            'package_version': '1.0',
            'image': 'addint-v1.0:1.0',
            'image_version': '1.0',
            'dockerurl': None
        },
        'network': None,
        'macronode': None,
    }
    return manifest_dict, container_dict


@pytest.fixture
def correct_files_dict():
    files_dict = {
        'tool': [
            "./tests/files/manifest/addint_tool/manifest.fastrpi_yaml",
            "./tests/files/manifest/addint_tool/Dockerfile",
            "./tests/files/manifest/addint_tool/LICENSE",
            "./tests/files/manifest/addint_tool/addint.yaml",
            "./tests/files/manifest/addint_tool/bin",
        ],
        'tool-without_files': [
            "./tests/files/manifest/addint_tool/manifest_without_files.fastrpi_yaml",
            "./tests/files/manifest/addint_tool/Dockerfile",
            "./tests/files/manifest/addint_tool/LICENSE",
            "./tests/files/manifest/addint_tool/addint.yaml",
        ],
        'network': [
            "./tests/files/manifest/addint_network/manifest.fastrpi_yaml",
            "./tests/files/manifest/addint_network/network.py",
            "./tests/files/manifest/addint_network/LICENSE",
            "./tests/files/manifest/addint_network/README.md",
        ],
        'macronode': [
            "./tests/files/manifest/addint_macronode/manifest.fastrpi_yaml",
            "./tests/files/manifest/addint_macronode/LICENSE",
            "./tests/files/manifest/addint_macronode/LICENSE_macro_addint",
            "./tests/files/manifest/addint_macronode/macro_addint.yaml",
        ]
    }
    return files_dict


@pytest.fixture
def updatable_manifest_path(tmp_path, correct_manifests_path):
    manifest_path = correct_manifests_path['tool']
    shutil.copytree(manifest_path.parent, tmp_path / 'updatable') 
    yield tmp_path / 'updatable' / manifest_path.name
    shutil.rmtree(tmp_path)


@pytest.fixture(scope="function")
def mock_path_home(tmp_path, monkeypatch):
    mock_home_path = tmp_path / 'mock_home'
    mock_home_path.mkdir()

    def mock_home():
        mock_home_path = tmp_path / 'mock_home'
        return mock_home_path

    monkeypatch.setattr(Path, "home", mock_home)
    yield mock_home_path
    shutil.rmtree(tmp_path)


@pytest.fixture
def mock_fastr_home(monkeypatch, mock_path_home):
    fastrhome = mock_path_home / ".fastr"
    fastrhome.mkdir()

    yield Path(fastrhome)
    shutil.rmtree(fastrhome)


@pytest.fixture
def mock_fastr_home_env(monkeypatch, mock_path_home, mock_fastr_home):
    mock_env_path = mock_path_home / 'fastr_env'
    mock_env_path.mkdir()
    monkeypatch.setenv("FASTRHOME", str(mock_env_path))
    yield mock_env_path
    shutil.rmtree(mock_env_path)


@pytest.fixture
def mock_fastrpi_home_env(monkeypatch, mock_path_home, mock_fastr_home_env):
    mock_env_path = mock_path_home / 'fastrpi_env'
    mock_env_path.mkdir()
    monkeypatch.setenv("FASTRPIHOME", str(mock_env_path))
    yield mock_env_path
    shutil.rmtree(mock_env_path)


@pytest.fixture(scope="function")
def mock_config(mock_fastrpi_home_env):
    config = Config()
    print("CI environment variable", os.environ.get("CI"))
    print(os.environ.get("CI_COMMIT_MESSAGE"))
    is_gitlab_cicd = (os.environ.get("CI") == "true")
    print(is_gitlab_cicd)
    if is_gitlab_cicd:
        ci_job_token = os.environ.get("CI_JOB_TOKEN")
        repository_urls = {
            'tools_git': f"https://gitlab-ci-token:{ci_job_token}@gitlab.com/radiology/infrastructure/projects/fastrpi/fastrpi-tools.git",
            'networks_git': f"https://gitlab-ci-token:{ci_job_token}@gitlab.com/radiology/infrastructure/projects/fastrpi/fastrpi-networks.git",
            'tools_docker': "registry.gitlab.com/radiology/infrastructure/projects/fastrpi/fastrpi-tools"
        }
        config.repository_urls = repository_urls
    yield config
