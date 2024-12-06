import shutil
import pytest

from fastrpi.exceptions import FastrPINotInstalled
from fastrpi.record import ToolInstallRecord, NetworkInstallRecord
from fastrpi.packageinfo import PackageInfo
from fastrpi.package import ToolPackage, NetworkPackage

def test_init_record(mock_config):
    """
    Init:
	- If no record file exists a record file should be created.
	- If a record file exists, it should be loaded.
	Request property installed packages:
	- Nothing is installed; should return an empty list.
    - Something is installed; should return the list of tags of the installed packages.
    """
    assert not mock_config.tool_record_path.exists()
    tool_install_record = ToolInstallRecord(mock_config)
    assert mock_config.tool_record_path.exists()
    assert tool_install_record.installed_packages == []

    shutil.copy("./tests/files/installrecord/tool_install_record.json", mock_config.tool_record_path)
    tool_install_record = ToolInstallRecord(mock_config)
    assert tool_install_record.installed_packages == [PackageInfo(name='addint', version='1.0', package_version='1.0')]

    assert not mock_config.network_record_path.exists()
    network_install_record = NetworkInstallRecord(mock_config)
    assert mock_config.network_record_path.exists()
    assert network_install_record.installed_packages == []

    shutil.copy("./tests/files/installrecord/network_install_record.json", mock_config.network_record_path)
    network_install_record = NetworkInstallRecord(mock_config)
    assert network_install_record.installed_packages == [PackageInfo(name='addint', package_version='1.0.0')]

def test_check_installed(mock_config):
    """
    Calling check_installed
    - Nothing is installed; should return False.
    - Something is installed, package is available; should return True
    - Something is installed, package is not available; should return False.
    """
    addint_tool = PackageInfo(
        name='addint',
        version='1.0',
        package_version='1.0'
    )
    multiply_tool = PackageInfo(
        name='multiply',
        version='1.0',
        package_version='1.0'
    )
    addint_network = PackageInfo(
        name='addint',
        package_version='1.0.0'
    )
    multiply_network = PackageInfo(
        name='multiply',
        package_version='1.0.0'
    )
    tool_install_record = ToolInstallRecord(mock_config)
    assert not tool_install_record.check_installed(addint_tool)
    network_install_record = NetworkInstallRecord(mock_config)
    assert not network_install_record.check_installed(addint_network)

    shutil.copy("./tests/files/installrecord/tool_install_record.json", mock_config.tool_record_path)
    tool_install_record = ToolInstallRecord(mock_config)
    shutil.copy("./tests/files/installrecord/network_install_record.json", mock_config.network_record_path)
    network_install_record = NetworkInstallRecord(mock_config)
    assert tool_install_record.check_installed(addint_tool)
    assert network_install_record.check_installed(addint_network)
    assert not tool_install_record.check_installed(multiply_tool)
    assert not network_install_record.check_installed(multiply_network)


def test_add_package(mock_config, correct_packages):
    """
    - After adding a package it should be marked as available when calling check_installed().
    """
    addint_tool = PackageInfo(
        name='addint',
        version='1.0',
        package_version='1.0'
    )
    addint_network = PackageInfo(
        name='addint',
        package_version='1.0'
    )
    tool_install_record = ToolInstallRecord(mock_config)
    tool_install_record.add(correct_packages['tool'])
    assert tool_install_record.check_installed(addint_tool)

    network_install_record = NetworkInstallRecord(mock_config)
    network_install_record.add(correct_packages['network'])
    assert network_install_record.check_installed(addint_network)


def test_load_package(mock_config, correct_packages):
    """
    Calling load_package():
    - Package is installed; should return the appropriate package.
    - Package is not installed; should raise a FastrPINotInstalled error.
    """
    addint_tool = PackageInfo(
        name='addint',
        version='1.0',
        package_version='1.0'
    )
    multiply_tool = PackageInfo(
        name='multiply',
        version='1.0',
        package_version='1.0'
    )
    addint_network = PackageInfo(
        name='addint',
        package_version='1.0'
    )
    multiply_network = PackageInfo(
        name='mulitply',
        package_version='1.0'
    )
    tool_install_record = ToolInstallRecord(mock_config)
    tool_install_record.add(correct_packages['tool'])
    loaded_tool = tool_install_record.load_package(addint_tool)
    assert type(loaded_tool) == ToolPackage
    assert loaded_tool.info == addint_tool

    network_install_record = NetworkInstallRecord(mock_config)
    network_install_record.add(correct_packages['network'])
    loaded_network = network_install_record.load_package(addint_network)
    assert type(loaded_network) == NetworkPackage
    assert loaded_network.info == addint_network

    with pytest.raises(FastrPINotInstalled):
        _ = tool_install_record.load_package(multiply_tool)
    with pytest.raises(FastrPINotInstalled):
        _ = network_install_record.load_package(multiply_network)


@pytest.mark.skip()
def test_remove_package():
    """
    - Package is installed
    - Package is not installed
    """
    pass
