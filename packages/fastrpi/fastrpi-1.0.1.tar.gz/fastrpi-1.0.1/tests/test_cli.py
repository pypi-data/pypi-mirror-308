import pytest
from click.testing import CliRunner
import fastrpi
from fastrpi.cli import cli


@pytest.fixture
def runner():
    return CliRunner()


def test_install_network_success(runner, mocker):
    mocker.patch("fastrpi.network_package_repo.install")
    with runner.isolated_filesystem():
        result = runner.invoke(cli, ["install", "network", "--version", "1.0", "network_name"])
    assert result.exit_code == 0
    assert "Network network_name, package version 1.0 installed successfully." in result.output


def test_install_network_already_installed(runner, mocker):
    mocker.patch(
        "fastrpi.network_package_repo.install",
        side_effect=fastrpi.exceptions.FastrPIAlreadyInstalled("Already installed."),
    )
    with runner.isolated_filesystem():
        result = runner.invoke(cli, ["install", "network", "--version", "1.0", "network_name"])
    assert result.exit_code == 0
    assert "Already installed." in result.output


def test_install_network_install_error(runner, mocker):
    mocker.patch(
        "fastrpi.network_package_repo.install",
        side_effect=fastrpi.exceptions.FastrPIInstallError(),
    )
    with runner.isolated_filesystem():
        result = runner.invoke(cli, ["install", "network", "--version", "1.0", "network_name"])
    assert result.exit_code == 0
    assert "Network network_name, package version 1.0 could not be installed." in result.output


def test_install_network_exception(runner, mocker):
    exception_obj = Exception()
    mocker.patch(
        "fastrpi.network_package_repo.install",
        side_effect=exception_obj,
    )
    with runner.isolated_filesystem():
        result = runner.invoke(cli, ["install", "network", "--version", "1.0", "network_name"])
    assert result.exit_code == 0
    assert f"Unknown Exception raised when installing network network_name, package version 1.0.\n{exception_obj}" \
           in result.output


def test_install_tool_success(runner, mocker):
    mocker.patch("fastrpi.tool_package_repo.install")
    with runner.isolated_filesystem():
        result = runner.invoke(cli, ["install", "tool", "--version", "1.0", "--package_version", "2.0", "tool_name"])
    assert result.exit_code == 0
    assert "Tool tool_name, version 1.0, package version 2.0 installed successfully." in result.output


def test_install_tool_already_installed(runner, mocker):
    mocker.patch(
        "fastrpi.tool_package_repo.install",
        side_effect=fastrpi.exceptions.FastrPIAlreadyInstalled("Already installed."),
    )
    with runner.isolated_filesystem():
        result = runner.invoke(cli, ["install", "tool", "--version", "1.0", "--package_version", "2.0", "tool_name"])
    assert result.exit_code == 0
    assert "Already installed." in result.output


def test_install_tool_install_error(runner, mocker):
    mocker.patch(
        "fastrpi.tool_package_repo.install",
        side_effect=fastrpi.exceptions.FastrPIInstallError(),
    )
    with runner.isolated_filesystem():
        result = runner.invoke(cli, ["install", "tool", "--version", "1.0", "--package_version", "2.0", "tool_name"])
    assert result.exit_code == 0
    assert "Tool tool_name, version 1.0, package version 2.0 could not be installed." in result.output


def test_install_too_exception(runner, mocker):
    exception_obj = Exception()
    mocker.patch(
        "fastrpi.tool_package_repo.install",
        side_effect=exception_obj,
    )
    with runner.isolated_filesystem():
        result = runner.invoke(cli, ["install", "tool", "--version", "1.0", "--package_version", "2.0", "tool_name"])
    assert result.exit_code == 0
    assert f"Unknown Exception raised when installing tool tool_name, version 1.0, package version 2.0.\n{exception_obj}" \
           in result.output