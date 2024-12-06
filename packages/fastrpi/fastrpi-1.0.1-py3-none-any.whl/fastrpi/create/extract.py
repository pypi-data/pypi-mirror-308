import ast
from abc import abstractmethod

import click

from ..helpers import read_yaml
from ..packageinfo import PackageInfo


class Extractor:
    def __init__(self, package_files):
        self.package_files = package_files
        self.datatypes = []
        self.report_out = []
        self.report_err = []

    @abstractmethod
    def extract_info(self) -> None:
        pass

    def report(self) -> None:
        click.echo("Report:")
        if self.report_out:
            for out_string in self.report_out:
                click.echo(out_string)
        else:
            click.echo("Nothing to report.")
        click.echo("Errors:")
        if self.report_err:
            for err_string in self.report_err:
                click.echo(err_string)
        else:
            click.echo("No errors.")

    def expand_typegroups(self) -> None:
        import fastr
        from fastr.datatypes import TypeGroup
        for dtype in self.datatypes:
            if dtype in fastr.types.keys() and issubclass(fastr.types[dtype], TypeGroup):
                typegroup_members = [m.name for m in fastr.types[dtype].members]
                self.report_out.append(f"TypeGroup {dtype} expanded to members {typegroup_members}.")
                self.datatypes.extend(typegroup_members)
        self.datatypes = list(set(self.datatypes))


class NetworkExtractor(Extractor):
    def __init__(self, network_file):
        super().__init__([network_file])
        self.network_file = network_file
        self.network_name = ''
        self.network_version = ''
        self.tool_tags = []
        self.tools = []
        self.sources = []
        self.sinks = []

    def extract_info(self) -> None:
        click.echo(f"Extracting data from Network {self.network_file}...")
        with open(self.network_file, 'r') as fname:
            tree = ast.parse(fname.read())

        for node in ast.walk(tree):
            if self.get_network_info(node)[0] is not None:
                self.network_name, self.network_version = self.get_network_info(node)
            if self.get_source(node) is not None:
                source_dict = self.get_source(node)
                self.sources.append(source_dict)
                self.datatypes.append(source_dict['datatype'])
            elif self.get_sink(node) is not None:
                sink_dict = self.get_sink(node)
                self.sinks.append(sink_dict)
                self.datatypes.append(sink_dict['datatype'])
            # if self.get_datatypes(node) is not None:
            #     self.datatypes.append(self.get_datatypes(node))
            if self.get_tool_node(node)[0] is not None:
                tool_string, tool_package_version = self.get_tool_node(node)
                tool_string_colon = tool_string.split(':')
                tool_version = tool_string_colon.pop()
                tool_string_split = tool_string_colon[0].split('/')
                if tool_version == tool_package_version:
                    if (len(tool_string_split) < 3
                            or tool_string_split[1] != tool_package_version):
                        self.report_err.append(f"Tool {tool_string} not correctly formatted for FastrPI.")
                        continue
                    elif (tool_string_split[1] == tool_version
                          and tool_string_split[2] == tool_package_version):
                        self.report_err.append(f"Tool {tool_string} not correctly formatted for FastrPI. " +
                                   "Version folder should be written once when version and package version are equal.")
                        continue
                else:
                    if (len(tool_string_split) < 4
                            or tool_string_split[1] != tool_version
                            or tool_string_split[2] != tool_package_version):
                        self.report_err.append(f"Tool {tool_string} not correctly formatted for FastrPI.")
                        continue
                tool_name = tool_string_split[0]
                tool = {
                    'name': tool_name,
                    'version': tool_version,
                    'package_version': tool_package_version
                }
                package_info = PackageInfo(name=tool_name,
                                           package_version=tool_package_version,
                                           version=tool_version)
                self.report_out.append(f"Found Tool {package_info} as {tool_string}.")
                tool_tag = package_info.tag
                if tool_tag not in self.tool_tags:
                    self.tool_tags.append(tool_tag)
                    self.tools.append(tool)
        self.datatypes = list(set(self.datatypes))
        self.expand_typegroups()

    def report(self) -> None:
        for source_dict in self.sources:
            self.report_out.append(f"Found Source {source_dict['id']} with datatype {source_dict['datatype']}.")
        for sink_dict in self.sinks:
            self.report_out.append(f"Found Sink {sink_dict['id']} with datatype {sink_dict['datatype']}.")
        super().report()

    @staticmethod
    def check_function_name(node, function_name):
        try:
            if node.value.func.attr == function_name:
                return True
        except AttributeError:
            # Node.value.func.attr fails for non-functions
            return False

    @staticmethod
    def get_keyword_value(node, keyword_name):
        try:
            return [keyword.value.value for keyword in node.value.keywords if keyword.arg == keyword_name][0]
        except AttributeError:
            return None

    def get_index_or_keyword_value(self, node, index, keyword_name):
        try:
            value = node.value.args[index].value
            return value
        except IndexError:
            return self.get_keyword_value(node, keyword_name)

    def get_network_info(self, node):
        network_name = None
        network_version = None
        if (isinstance(node, ast.Assign)
                and isinstance(node.value, ast.Call)):
            if self.check_function_name(node, 'create_network'):
                network_name = self.get_keyword_value(node, 'id')
                network_version = self.get_keyword_value(node, 'version')
        return network_name, network_version

    def get_datatypes(self, node):
        if (isinstance(node, ast.Assign)
                and isinstance(node.value, ast.Call)):
            if (self.check_function_name(node, 'create_source')
                    or self.check_function_name(node, 'create_sink')):
                return self.get_index_or_keyword_value(node, 0, 'datatype')
        return None

    def get_tool_node(self, node):
        tool_string = None
        tool_version = None
        if (isinstance(node, ast.Assign)
                and isinstance(node.value, ast.Call)):
            if self.check_function_name(node, 'create_node'):
                tool_string = self.get_index_or_keyword_value(node, 0, 'tool')
                tool_version = self.get_keyword_value(node, 'tool_version')
        return tool_string, tool_version

    def get_source(self, node):
        if (isinstance(node, ast.Assign)
                and isinstance(node.value, ast.Call)):
            if self.check_function_name(node, 'create_source'):
                return_dict = {
                    'id': self.get_keyword_value(node, 'id'),
                    'datatype': self.get_index_or_keyword_value(node, 0, 'datatype')
                }
                return return_dict
        return None

    def get_sink(self, node):
        if (isinstance(node, ast.Assign)
                and isinstance(node.value, ast.Call)):
            if self.check_function_name(node, 'create_sink'):
                return_dict = {
                    'id': self.get_keyword_value(node, 'id'),
                    'datatype': self.get_index_or_keyword_value(node, 0, 'datatype')
                }
                return return_dict
        return None


class ToolExtractor(Extractor):
    def __init__(self, package_files):
        super().__init__(package_files)
        self.tool_dicts = []

    def extract_info(self) -> None:
        for tool_file in self.package_files:
            click.echo(f"Extracting data from Tool {tool_file}...")
            tool = read_yaml(tool_file)
            self.tool_dicts.append({
                'id': tool['id'],
                'tool_version': tool['version'],
                'command_version': tool['command']['version'],
                'tool_file': str(tool_file)
            })
            interface = tool['interface']
            interface_io = interface['inputs'] + interface['outputs']
            for io_obj in interface_io:
                try:
                    self.datatypes.append(io_obj['datatype'])
                except KeyError:
                    self.report_out.append(f"Input/output {io_obj['id']}, from {tool['id']} has no Datatype.")
        self.datatypes = list(set(self.datatypes))
        self.expand_typegroups()
        




