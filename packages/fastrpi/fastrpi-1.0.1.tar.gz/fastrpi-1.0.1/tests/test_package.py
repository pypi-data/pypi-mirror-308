from fastrpi.manifest import Manifest
from fastrpi.package import Package, ToolPackage, NetworkPackage

def test_init_packages(correct_manifests_path):
    # Tool
    tool_manifest = Manifest.create(correct_manifests_path['tool'])
    tool_package = Package.create(tool_manifest)
    assert tool_package.manifest == tool_manifest
    assert tool_package.name == 'addint'
    assert tool_package.version == '1.0'
    assert tool_package.package_version == '1.0'
    assert tool_package.tag == 'addint-v1.0-p1.0'
    assert f"{tool_package}" == "addint, version 1.0, package version 1.0"
    assert type(tool_package) == ToolPackage

    # Network
    network_manifest = Manifest.create(correct_manifests_path['network'])
    network_package = Package.create(network_manifest)
    assert network_package.manifest == network_manifest
    assert network_package.name == 'addint'
    assert network_package.package_version == '1.0'
    assert network_package.tag == 'addint-v1.0'
    assert f"{network_package}" == "addint, package version 1.0"
    assert type(network_package) == NetworkPackage
