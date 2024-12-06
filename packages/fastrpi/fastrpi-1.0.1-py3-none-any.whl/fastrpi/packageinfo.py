class PackageInfo(object):

    @classmethod
    def from_dict(cls, info: dict) -> 'PackageInfo':
        if 'version' in info.keys():
            return PackageInfo(
                name=info['name'],
                package_version=info['package_version'],
                version=info['version']
            )
        else:
            return PackageInfo(
                name=info['name'],
                package_version=info['package_version']
            )

    def __init__(self, name: str, package_version: str, version: str = None):
        self.name = name
        self.package_version = package_version
        self.version = version
        self.package_type = 'Package'

    @property
    def tag(self):
        if self.version is None:
            return f"{self.name}-v{self.package_version}"
        else:
            return f"{self.name}-v{self.version}-p{self.package_version}"

    def __str__(self) -> str:
        if self.version is None:
            return f"{self.name}, package version {self.package_version}"
        else:
            return f"{self.name}, version {self.version}, package version {self.package_version}"

    def __eq__(self, other) -> bool:
        if ((self.name == other.name)
                and (self.package_version == other.package_version)
                and (self.version == other.version)):
            return True
        else:
            return False
