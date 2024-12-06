import click

from .create import create_macronode, create_network, create_tool
from .describe import describe_tool, describe_network
from .edit import edit_network, edit_tool
from .init import init
from .install import install_network, install_tool
from .list import (list_avail_networks, list_avail_tools, list_avail_types,
                   list_installed)
from .publish import publish_network, publish_tool
from .run import run_local, run_network


@click.group()
def cli():
    """ Client for the Fastr Package Index (FastrPI)."""
    pass


cli.add_command(run_network, name='run')
cli.add_command(run_local, name='runlocal')

cli.add_command(init, name='init')


@cli.group(short_help="Create a package.")
def create():
    """ Create a FastrPI package."""
    pass


create.add_command(create_tool, name='tool')
create.add_command(create_network, name='network')
create.add_command(create_macronode, name='macronode')


@cli.group(short_help="Install a package.")
def install():
    """ Install a FastrPI package. """
    pass


install.add_command(install_network, name='network')
install.add_command(install_tool, name='tool')


@cli.group(short_help="Edit a package.")
def edit():
    """ Copy an installed Network or Tool package to your current folder for editing. """
    pass


edit.add_command(edit_network, name='network')
edit.add_command(edit_tool, name='tool')


@cli.group(short_help="Publish a package.")
def publish():
    """ Publish your Network or Tool package to the FastrPI repository. """
    pass


publish.add_command(publish_network, name='network')
publish.add_command(publish_tool, name='tool')


@cli.group('list', short_help="List Tools, Networks and Datatypes; installed or available.")
def list_group():
    """ List installed or available FastrPI Tools, Networks and Datatypes. """
    pass


list_group.add_command(list_installed, name='installed')
list_group.add_command(list_avail_tools, name='tools')
list_group.add_command(list_avail_networks, name='networks')
list_group.add_command(list_avail_types, name='datatypes')


@cli.group('describe', short_help="Give more details on the Packages.")
def describe():
    """ Describe FastrPI Tools or Networks. """
    pass


describe.add_command(describe_tool, name='tool')
describe.add_command(describe_network, name='network')
