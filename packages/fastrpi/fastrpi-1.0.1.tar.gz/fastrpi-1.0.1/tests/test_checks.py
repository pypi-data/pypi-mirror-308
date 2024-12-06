import pytest

import fastrpi
from fastrpi.exceptions import FastrPIPublishTestError
from fastrpi.repository import PackageRepository, ToolPackageRepository, NetworkPackageRepository


def test_checks_check_name(correct_packages, monkeypatch):
    package = correct_packages['tool']
    monkeypatch.setitem(package.manifest, 'name', 'test-name')
    with pytest.raises(FastrPIPublishTestError, match="Name is not correctly formatted; name cannot contain '-'"):
        package.checks._check_name()
    monkeypatch.setitem(package.manifest, 'name', '_testname')
    with pytest.raises(FastrPIPublishTestError, match="Name is not correctly formatted; name cannot start with '_'"):
        package.checks._check_name()
    monkeypatch.setitem(package.manifest, 'name', 'datatypes')
    with pytest.raises(FastrPIPublishTestError, match="A tool cannot be named 'datatypes'. This name is reserved."):
        package.checks._check_name()

def test_checks_check_tag(correct_packages, monkeypatch, mock_config):
    class TestToolPackageRepo(ToolPackageRepository):
        @property
        def avail_packages(self):
            return [correct_packages['tool'].info]
    testtoolrepo = TestToolPackageRepo(mock_config)

    class TestMacronodePackageRepo(ToolPackageRepository):
        @property
        def avail_packages(self):
            return [correct_packages['macronode'].info]
    testmacrorepo = TestMacronodePackageRepo(mock_config)

    class TestNetworkPackageRepo(NetworkPackageRepository):
        @property
        def avail_packages(self):
            return [correct_packages['network'].info]
    testnetworkrepo = TestNetworkPackageRepo(mock_config)

    monkeypatch.setattr(fastrpi, 'tool_package_repo', testtoolrepo)
    with pytest.raises(FastrPIPublishTestError, match="Tag (.*) already taken."):
        correct_packages['tool'].checks._check_tag_taken()

    monkeypatch.setattr(fastrpi, 'tool_package_repo', testmacrorepo)
    with pytest.raises(FastrPIPublishTestError, match="Tag (.*) already taken."):
        correct_packages['macronode'].checks._check_tag_taken()

    monkeypatch.setattr(fastrpi, 'network_package_repo', testnetworkrepo)
    with pytest.raises(FastrPIPublishTestError, match="Tag (.*) already taken."):
        correct_packages['network'].checks._check_tag_taken()


def test_checks_check_datatype(correct_packages, monkeypatch, mock_config):
    package = correct_packages['tool']
    class TestToolPackageRepo(ToolPackageRepository):
        @property
        def avail_datatypes(self):
            return ['notthatone']
    testtoolrepo = TestToolPackageRepo(mock_config)

    monkeypatch.setattr(fastrpi, 'tool_package_repo', testtoolrepo)
    monkeypatch.setitem(package.manifest, 'required_datatypes', ['thisoneplease'])
    with pytest.raises(FastrPIPublishTestError, match="Datatype (.*) is not available within FastrPI."):
        package.checks._check_required_datatypes()


def test_checks_check_tool_valid(correct_packages, monkeypatch, mocker):
    package = correct_packages['tool']
    monkeypatch.setattr("fastrpi.checks.check_valid_yaml", lambda x: False)
    tool = {'tool_definition': 'path_to_tool_definition'}
    with pytest.raises(FastrPIPublishTestError, match="Tool definition (.*) is not valid YAML."):
        package.checks._check_tool_valid(tool)

    monkeypatch.setattr("fastrpi.checks.check_valid_yaml", lambda x: True)
    def mock_raise(path, perform_tests):
        raise Exception
    monkeypatch.setattr('fastr.utils.verify.verify_tool', mock_raise)
    with pytest.raises(FastrPIPublishTestError, match="Tool definition is not valid."):
        package.checks._check_tool_valid(tool)

    monkeypatch.setattr("fastrpi.checks.check_valid_yaml", lambda x: True)
    mocker.patch('fastr.utils.verify.verify_tool')

def test_checks_check_tool_version(correct_packages, monkeypatch, mocker):
    package = correct_packages['tool']
    tool = {'id': 'tool_id', 'tool_definition': 'path_to_tool_definition'}

    monkeypatch.setitem(package.manifest, 'version', '1.0')
    monkeypatch.setitem(package.manifest, 'package_version', '2.0')
    def mock_read_pack_version(path):
        return {'id': 'tool_id', 'version': '3.0', 'command': {'version': '2.0'}}
    monkeypatch.setattr('fastrpi.checks.read_yaml', mock_read_pack_version)
    with pytest.raises(FastrPIPublishTestError, match="Version for (.*) is not equal to the package version."):
        package.checks._check_tool_version(tool)

    def mock_read_version(path):
        return {'id': 'tool_id', 'version': '2.0', 'command': {'version': '2.0'}}
    monkeypatch.setattr('fastrpi.checks.read_yaml', mock_read_version)
    with pytest.raises(FastrPIPublishTestError, match="Command version for (.*) is not equal to the version in the"
                                                      + " manifest."):
        package.checks._check_tool_version(tool)

    def mock_read_correct(path):
        return {'id': 'tool_id', 'version': '2.0', 'command': {'version': '1.0'}}
    monkeypatch.setattr('fastrpi.checks.read_yaml', mock_read_correct)
    monkeypatch.setattr(package.checks, '_tool_versions', ['0.1', '0.2'])
    with pytest.raises(FastrPIPublishTestError, match="Versions for the Fastr Tools are not all equal."):
        package.checks._check_tool_version(tool)
