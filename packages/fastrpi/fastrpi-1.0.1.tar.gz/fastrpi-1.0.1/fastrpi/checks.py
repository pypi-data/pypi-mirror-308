from abc import abstractmethod
from pathlib import Path
from typing import TYPE_CHECKING

import click

import fastrpi
from .exceptions import (FastrPIAlreadyInstalled, FastrPIPublishError,
                         FastrPIPublishTestError)
from .helpers import check_valid_yaml, load_module_from_file, read_yaml
from .packageinfo import PackageInfo

if TYPE_CHECKING:
    from .package import MacroNodePackage, NetworkPackage, Package, ToolPackage


class PackageChecks(object):
    """
    Checks to assure proper formatting and functionality of the packages.
    These checks are run before publishing and in the CI/CD pipeline.

    This class can be subclassed to implement specific checks for
    different package types.
    """

    def __init__(self, package: 'Package') -> None:
        """
        Create a PackageChecks object.

        :param package: Parent Package object.
        """
        self.package = package
        self.manifest = package.manifest

    @abstractmethod
    def run_checks(self) -> None:
        """
        Run the checks.
        """
        pass

    def _check_name(self) -> None:
        if '-' in self.manifest['name']:
            raise FastrPIPublishTestError("Name is not correctly formatted; name cannot contain '-'")
        if self.manifest['name'].startswith('_'):
            raise FastrPIPublishTestError("Name is not correctly formatted; name cannot start with '_'")


class ToolPackageChecks(PackageChecks):
    """
    Checks to assure proper formatting and functionality of the tool packages.
    These checks are run before publishing and in the CI/CD pipeline.
    """

    def __init__(self, package: 'ToolPackage') -> None:
        """
        Create a ToolPackageChecks object.

        :param package: Parent ToolPackage object.
        """
        super().__init__(package)
        self._tool_versions = []

    def run_checks(self) -> None:
        """
        Run all checks.

        Raises FastrPIPublishTestError when a test fails.
        Raises FastrPIPublishError when the user cancels publishing.
        """
        self.manifest.run_checks()
        self._check_name()
        self._check_tag_taken()
        self._check_required_datatypes()
        for tool_idx, tool in enumerate(self.manifest['tools']):
            self._check_tool_valid(tool)
            self._check_tool_version(tool)
            self._check_tool_target(tool)
            if 'licence' not in tool.keys():
                license_path = (self.manifest.folder / tool['tool_definition']).parent \
                    / f"LICENSE_{tool['tool_definition'].stem}"
                self._create_tool_license(tool, license_path)
                self.manifest['tools'][tool_idx]['license'] = \
                    license_path.relative_to(self.manifest.folder)
                self.manifest.update_file()

    def _check_name(self) -> None:
        super()._check_name()
        reserved_names = ['datatypes']
        if self.package.name in reserved_names:
            raise FastrPIPublishTestError(
                f"A tool cannot be named '{self.package.name}'. This name is reserved.")

    def _check_tag_taken(self) -> None:
        if self.package.info in fastrpi.tool_package_repo.avail_packages:
            raise FastrPIPublishTestError(f"Tag {self.package.tag} already taken.")

    def _check_required_datatypes(self) -> None:
        for datatype in self.manifest['required_datatypes']:
            if datatype not in fastrpi.tool_package_repo.avail_datatypes:
                raise FastrPIPublishTestError(f"Datatype {datatype} is not available within FastrPI.")

    def _check_tool_valid(self, tool: dict) -> None:
        from fastr.utils.verify import verify_tool
        if not check_valid_yaml(self.manifest.folder / tool['tool_definition']):
            raise FastrPIPublishTestError(f"Tool definition {tool['tool_definition']} is not valid YAML.")

        print("Checking the tool definition...")
        try:
            verify_tool(self.manifest.folder / tool['tool_definition'], perform_tests=False)
        except Exception as exc:
            print(exc)
            raise FastrPIPublishTestError("Tool definition is not valid.") from exc
        else:
            print("The tool definition is valid.")

    def _check_tool_version(self, tool: dict) -> None:
        version = self.manifest['version']
        package_version = self.manifest['package_version']
        tool_data = read_yaml(self.manifest.folder / tool['tool_definition'])
        if tool_data['version'] != package_version:
            raise FastrPIPublishTestError(f"Version for {tool_data['id']} is not equal to the package version.")
        if tool_data['command']['version'] != version:
            raise FastrPIPublishTestError(f"Command version for {tool_data['id']}"
                                          + " is not equal to the version in the manifest.")
        self._tool_versions.append(tool_data['version'])
        if len(list(set(self._tool_versions))) != 1:
            raise FastrPIPublishTestError("Versions for the Fastr Tools are not all equal.")

    def _check_tool_target(self, tool: dict) -> None:
        tool_data = read_yaml(self.manifest.folder / tool['tool_definition'])
        docker_images = [target['docker_image'] for target in tool_data['command']['targets']
                         if target.get('class', 'NotFound') == 'DockerTarget']
        singularity_images = [target['container'] for target in tool_data['command']['targets']
                              if target.get('class', 'NotFound') == 'SingularityTarget']
        if docker_images and singularity_images:
            manifest_image = self.manifest.container['image']
            singularity_image_local = f"{manifest_image.split(':')[0]}_{manifest_image.split(':')[1]}.sif"
            singularity_image_remote = f"docker://{fastrpi.fastrpi_config.repository_urls['tools_docker']}/{manifest_image}"

            if manifest_image not in docker_images:
                error_message = f"Docker image {manifest_image} in manifest, "\
                    + f"does not correspond to images {docker_images} in the tool definition."
                raise FastrPIPublishTestError(error_message)
            if ((singularity_image_local not in singularity_images)
                    and (singularity_image_remote not in singularity_images)):
                error_message = f"Docker image {manifest_image} in manifest, " \
                                + f"should correspond to Singularity images {singularity_image_local} \nor " \
                                + f"{singularity_image_remote} in the tool definition.\nFound" \
                                  f"{singularity_images}."
                raise FastrPIPublishTestError(error_message)
        elif docker_images and not singularity_images:
            raise FastrPIPublishTestError(f"No SingularityTarget known for {tool_data['id']}") from None
        elif not docker_images and singularity_images:
            raise FastrPIPublishTestError(f"No DockerTarget known for {tool_data['id']}") from None
        else:
            raise FastrPIPublishTestError(f"No DockerTarget or SingularityTarget known for {tool_data['id']}") from None

    def _create_tool_license(self, tool: dict, license_path: Path) -> None:
        license_check_text = (
                f"By uploading this tool to FastrPI the Fastr tool definition {tool['tool_definition'].name}\n"
                + "will be licensed under the Creative Commons Attribution 4.0 International License.\n"
                + "To view a copy of this license, visit http://creativecommons.org/licenses/by/4.0/.\n"
                + "The underlying software will be licensed under the license you provide in the LICENSE file.\n\n"
                + "Please enter 'y' if you agree. "
        )
        if not license_path.exists():
            if click.confirm(license_check_text, default=False):
                license_text = (
                    f"The file {tool['tool_definition'].name} is licensed under the Creative Commons Attribution \n"
                    + "4.0 International License. To view a copy of this license, visit \n"
                    + "http://creativecommons.org/licenses/by/4.0/ or send a letter to \n"
                    + "Creative Commons, PO Box 1866, Mountain View, CA 94042, USA."
                )
                with open(license_path, 'w') as license_file:
                    license_file.write(license_text)
                click.echo(f"The file {license_path} has been added.")
            else:
                raise FastrPIPublishError("Publishing canceled.")


class MacroNodePackageChecks(ToolPackageChecks):
    """
    Checks to assure proper formatting and functionality of the tool packages.
    These checks are run before publishing and in the CI/CD pipeline.
    """

    def __init__(self, package: 'MacroNodePackage') -> None:
        """
        Create a MacroNodePackageChecks object.

        :param package: Parent MacroNodePackage object.
        """
        self.network_package_info = None
        super().__init__(package)

    def run_checks(self) -> None:
        """
        Run all checks.

        Raises FastrPIPublishTestError when a test fails.
        Raises FastrPIPublishError when the user cancels publishing.
        """
        self.manifest.run_checks()
        self._check_name()
        self.network_package_info = PackageInfo(name=self.package.manifest['name'][len('macro_'):],
                                                package_version=self.package.manifest['version'])
        self._check_tag_taken()
        self._check_network_present()
        for tool_idx, tool in enumerate(self.manifest['tools']):
            self._check_tool_valid(tool)
            self._check_tool_version(tool)
            self._check_tool_target(tool)
            if 'licence' not in tool.keys():
                license_path = (self.manifest.folder / tool['tool_definition']).parent \
                    / f"LICENSE_{tool['tool_definition'].stem}"
                self._create_tool_license(tool, license_path)
                self.manifest['tools'][tool_idx]['license'] = \
                    license_path.relative_to(self.manifest.folder)
                self.manifest.update_file()

    def _check_name(self) -> None:
        super()._check_name()
        if not self.manifest['name'].startswith('macro_'):
            raise FastrPIPublishTestError("Name is not correctly formatted; MacroNode names must start with 'macro_'")

    def _check_network_present(self) -> None:
        if not fastrpi.network_package_repo.check_available(self.network_package_info):
            raise FastrPIPublishTestError(f"Network {self.network_package_info} is not present in FastrPI.")

    def _check_tool_target(self, tool: dict) -> None:
        tool_data = read_yaml(self.manifest.folder / tool['tool_definition'])
        macro_node_targets = []
        for target in tool_data['command']['targets']:
            if 'network_file' in target.keys():
                macro_node_targets.append(target)
        if macro_node_targets:
            for target in macro_node_targets:
                if ('network_file' not in target.keys()) or ('function' not in target.keys()):
                    raise FastrPIPublishTestError("MacroNode target does not contain 'network_file' and 'function'.")
                if target['network_file'] != f"{self.network_package_info.tag}.py":
                    raise FastrPIPublishTestError(f"Argument 'network_file' for target is not equal to "
                                                  + f"'{self.network_package_info.tag}.py'.")
                if target['function'] != 'create_network':
                    raise FastrPIPublishTestError("Argument 'function' for target is not equal to 'create_network'.")
        else:
            raise FastrPIPublishTestError("No MacroNode targets specified.")

    def _check_tool_version(self, tool: dict) -> None:
        version = self.manifest['version']
        package_version = self.manifest['package_version']
        tool_data = read_yaml(self.manifest.folder / tool['tool_definition'])
        if tool_data['version'] != package_version:
            raise FastrPIPublishTestError(f"Version for {tool_data['id']} is not equal to the package version.")
        if tool_data['command']['version'] != self.network_package_info.package_version:
            raise FastrPIPublishTestError(f"Command version for {tool_data['id']}"
                                          + " is not equal to the Network package version.")
        if tool_data['command']['version'] != version:
            raise FastrPIPublishTestError(f"Command version for {tool_data['id']}"
                                          + " is not equal to the version in the manifest.")


class NetworkPackageChecks(PackageChecks):
    """
    Checks to assure proper formatting and functionality of the network packages.
    These checks are run before publishing and in the CI/CD pipeline.
    """

    def __init__(self, package: 'NetworkPackage') -> None:
        """
        Create a NetworkPackageChecks object.

        :param package: Parent NetworkPackage object.
        """
        super().__init__(package)

    def run_checks(self) -> None:
        """
        Run all checks.

        Raises FastrPIPublishTestError when a test fails.
        """
        self._check_name()
        self._check_tag_taken()
        self._check_required_datatypes()
        self._check_required_tools()
        self._check_network_def()
        self._check_avail_files()

    def _check_tag_taken(self) -> None:
        if self.package.info in fastrpi.network_package_repo.avail_packages:
            raise FastrPIPublishTestError(f"Tag {self.package.tag} already taken.")

    def _check_required_datatypes(self) -> None:
        for datatype in self.manifest['required_datatypes']:
            if datatype not in fastrpi.tool_package_repo.avail_datatypes:
                raise FastrPIPublishTestError(f"Datatype {datatype} is not available within FastrPI.")

    def _check_required_tools(self) -> None:
        for tool_package in self.manifest['tool_packages']:
            package_info = PackageInfo(
                name=tool_package['name'],
                package_version=tool_package['package_version'],
                version=tool_package['version'])
            if not fastrpi.tool_package_repo.check_available(package_info):
                raise FastrPIPublishTestError(
                    f"Tool package {package_info} is not available within FastrPI.")

    def _check_network_def(self) -> None:
        print("Checking the network definition...")
        # Install tools to test the network
        for tool in self.manifest.get('tool_packages', []):
            try:
                package_info = PackageInfo(
                    name=tool['name'],
                    package_version=tool['package_version'],
                    version=tool['version'],
                )
                fastrpi.tool_package_repo.install(package_info)
            except FastrPIAlreadyInstalled:
                pass
        try:
            network_module = load_module_from_file(self.manifest.folder / self.manifest['network'], 
                                                   'network_module')
        except Exception as exc:
            print(exc)
            raise FastrPIPublishTestError("Network file not a valid Python file.") from exc

        try:
            network = network_module.create_network()
        except Exception as exc:
            print(f"Error message: {exc}.")
            raise FastrPIPublishTestError("Network file does not contain function create_network() "
                                          + "or another error occurred during execution.") from exc
        if not network.is_valid():
            raise FastrPIPublishTestError("Function create_network() in network.py does not create Fastr network.")
        if not str(network.version) == self.manifest['package_version']:
            raise FastrPIPublishTestError("Version in the network file does not correspond with the package version.")

    def _check_avail_files(self) -> None:
        """
        Check if the required auxillary files are accesible.
        """
        print("Make sure that any auxillary files, e.g. masks, deep learning models, are accessible.")
