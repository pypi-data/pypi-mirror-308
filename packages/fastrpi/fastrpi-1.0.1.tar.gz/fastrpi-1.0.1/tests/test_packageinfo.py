from fastrpi.packageinfo import PackageInfo


def test_packageinfo_tool():
    packageinfo = PackageInfo(name='toolname', version="1.0", package_version="2.0")
    assert packageinfo.tag == "toolname-v1.0-p2.0"
    assert str(packageinfo) == "toolname, version 1.0, package version 2.0"
    packageinfo_equal = PackageInfo(name='toolname', version="1.0", package_version="2.0")
    packageinfo_uneq_name = PackageInfo(name='tool', version="1.0", package_version="2.0")
    packageinfo_uneq_ver = PackageInfo(name='toolname', version="2.0", package_version="2.0")
    packageinfo_uneq_packver = PackageInfo(name='toolname', version="1.0", package_version="3.0")
    assert packageinfo == packageinfo_equal
    assert packageinfo != packageinfo_uneq_name
    assert packageinfo != packageinfo_uneq_ver
    assert packageinfo != packageinfo_uneq_packver


def test_packageinfo_network():
    packageinfo = PackageInfo(name='networkname', package_version="1.0")
    assert packageinfo.tag == "networkname-v1.0"
    assert str(packageinfo) == "networkname, package version 1.0"
    packageinfo_equal = PackageInfo(name='networkname', package_version="1.0")
    packageinfo_uneq_name = PackageInfo(name='network', package_version="1.0")
    packageinfo_uneq_packver = PackageInfo(name='networkname', package_version="2.0")
    assert packageinfo == packageinfo_equal
    assert packageinfo != packageinfo_uneq_name
    assert packageinfo != packageinfo_uneq_packver


def test_packageinfo_tool_fromdict():
    packdict = {
        'name': 'toolname',
        'version': '1.0',
        'package_version': '2.0'
    }
    fromdict = PackageInfo.from_dict(packdict)
    packageinfo = PackageInfo(name='toolname', version="1.0", package_version="2.0")
    assert fromdict == packageinfo


def test_packageinfo_network_fromdict():
    packdict = {
        'name': 'networkname',
        'package_version': '1.0'
    }
    fromdict = PackageInfo.from_dict(packdict)
    packageinfo = PackageInfo(name='networkname', package_version="1.0")
    assert fromdict == packageinfo
