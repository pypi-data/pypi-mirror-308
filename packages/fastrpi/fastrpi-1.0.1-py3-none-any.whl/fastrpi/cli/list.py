import click
from tabulate import tabulate

import fastrpi
from ..helpers import read_yaml


def make_table_installed_tools(package_info_list, verbose=False):
    col_names = ['Name', 'Version', 'Package version']
    if verbose:
        col_names.extend(['Tool path'])
    table_dict = {col: [] for col in col_names}
    for package_info in package_info_list:
        if not verbose:
            table_dict.get('Name').append(str(package_info.name))
            table_dict.get('Version').append(str(package_info.version))
            table_dict.get('Package version').append(str(package_info.package_version))
        else:
            tool_package = fastrpi.tool_install_record.load_package(package_info)
            for tool in tool_package.manifest['tools']:
                tool_def_path = tool['tool_definition'].parent
                tool_def = read_yaml(tool_package.manifest.folder / tool['tool_definition'])
                if package_info.version == package_info.package_version:
                    if tool_def_path.parts:
                        tool_path = '/'.join([package_info.name, package_info.version, str(tool_def_path),
                                              tool_def['id']])
                    else:
                        tool_path = '/'.join([package_info.name, package_info.version, tool_def['id']])
                else:
                    if tool_def_path.parts:
                        tool_path = '/'.join(
                            [package_info.name, package_info.version, package_info.package_version,
                             str(tool_def_path), tool_def['id']])
                    else:
                        tool_path = '/'.join([package_info.name, package_info.version, package_info.package_version,
                                              tool_def['id']])
                tool_path = tool_path + f':{package_info.version}'
                table_dict.get('Name').append(str(package_info.name))
                table_dict.get('Version').append(str(package_info.version))
                table_dict.get('Package version').append(str(package_info.package_version))
                table_dict.get('Tool path').append(tool_path)

    table_string = tabulate(table_dict, headers="keys", disable_numparse=True)
    return table_string


def make_table_installed_networks(package_info_list, verbose=False):
    if verbose:
        click.echo('No verbose option; returning regular output:')
    col_names = ['Name', 'Package version']
    table_dict = {col: [] for col in col_names}
    for package_info in package_info_list:
        table_dict.get('Name').append(str(package_info.name))
        table_dict.get('Package version').append(str(package_info.package_version))

    table_string = tabulate(table_dict, headers="keys", disable_numparse=True)
    return table_string


@click.command('installed', short_help="List installed Tools and Networks.")
@click.option('--verbose', '-v', is_flag=True, required=False, default=False)
def list_installed(verbose: bool) -> None:
    click.echo('Installed tools:')
    click.echo(make_table_installed_tools(fastrpi.tool_install_record.installed_packages, verbose) + '\n')

    click.echo('Installed networks:')
    click.echo(make_table_installed_networks(fastrpi.network_install_record.installed_packages, verbose))


@click.command('tools', short_help="List available Tool packages on the FastrPI repository.")
@click.option('--verbose', '-v', is_flag=True, required=False, default=False)
def list_avail_tools(verbose: bool) -> None:
    if verbose:
        click.echo('No verbose option; returning regular output:')
        verbose = False
    click.echo('Available tools:')
    click.echo(make_table_installed_tools(fastrpi.tool_package_repo.avail_packages, verbose) + '\n')


@click.command('datatypes', short_help="List available Datatypes.")
@click.option('--verbose', '-v', is_flag=True, required=False, default=False)
def list_avail_types(verbose: bool) -> None:
    if verbose:
        click.echo('No verbose option; returning regular output:')
        verbose = False
    title = 'Available datatypes:'
    output = [title, '-' * len(title)]
    output.extend(fastrpi.tool_package_repo.avail_datatypes)
    output_string = '\n'.join(output)
    click.echo(output_string)


@click.command('networks', short_help="List available Network packages on the FastrPI repository.")
@click.option('--verbose', '-v', is_flag=True, required=False, default=False)
def list_avail_networks(verbose: bool) -> None:
    if verbose:
        click.echo('No verbose option; returning regular output:')
        verbose = False
    click.echo('Available networks:')
    click.echo(make_table_installed_networks(fastrpi.network_package_repo.avail_packages, verbose) + '\n')
