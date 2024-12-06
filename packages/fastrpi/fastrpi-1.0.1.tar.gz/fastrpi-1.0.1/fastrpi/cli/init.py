import os
import shutil
from pathlib import Path

import click
import questionary

from fastrpi import fastrpi_config, on_rtd
from fastrpi.exceptions import FastrPIError


class RTDDummy:
    def __init__(self):
        self.installed_packages = []


if on_rtd:
    tool_install_record = RTDDummy()
    network_install_record = RTDDummy()
else:
    from fastrpi import tool_install_record, network_install_record


@click.command('init', short_help="Initialize the FastrPI setup.")
def init() -> None:
    """
    Initialize the FastrPI setup.
    """
    questionary.print("Welcome to initialization wizard of the FastrPI client.", style='bold')
    try:
        questionary.print("Git: To use FastrPI Git >=1.7.0 needs to be installed. \n"
                          + "This can be checked by running 'git --version'.", style="bold")
        if not questionary.confirm("Git: Do you have Git >=1.7.0 installed?").unsafe_ask():
            questionary.print("- FastrPI needs Git >=1.7.0.", style='bold')
            raise FastrPIError
        questionary.print("Git: The name and email of the user need to be configured. \n" +
                          "The values can be checked by running 'git config user.name' and 'git config user.email'.",
                          style='bold')
        if not questionary.confirm("Git: Is Git configured?").unsafe_ask():
            questionary.print(
                "Configure Git with the following commands, replacing the placeholders with your actual name and email:",
                style='bold')
            questionary.print("git config --global user.name 'your_username'", style='bold')
            questionary.print("git config --global user.email your@email.com", style='bold')
        # questionary.print("-- Install Fastr --", style='bold')
        if not questionary.confirm(
                "Do you want to setup the private FastrPI repositories? Choose 'No' for the tutorial.",
                default=False).unsafe_ask():
            fastrpi_config.public = True
            fastrpi_config.write('public')
        else:
            fastrpi_config.public = False
            fastrpi_config.write('public')
            questionary.print("To use the private FastrPI repositories you will need to: \n"
                              + "- Set up an SSH key and share it with the GitLab repositories \n"
                              + "- Create an GitLab Access Token with 'read_api' scope. For publishing 'api' scope is also needed.",
                              style='bold')
            response = questionary.path("Give a path to a text file with the GitLab Access Token.").unsafe_ask()
            fastrpi_config.gitlab_token_file = str(Path(os.path.expanduser(response)).resolve())
            fastrpi_config.write('gitlab_token_file')
            removal_msg = "In order to use the private FastrPI repositories instead of the public ones, " \
                          + "the local FastrPI folders need to be removed. These folders will be regenerated the " \
                          + "next time FastrPI runs.\n"
            if tool_install_record.installed_packages or network_install_record.installed_packages:
                removal_msg += f"There are {len(tool_install_record.installed_packages)} Tool packages " \
                               + f"and {len(network_install_record.installed_packages)} Network packages installed. "
            else:
                removal_msg += f"There are no Tool or Network packages installed.\n"
            questionary.print("The FastrPI folders and files are:", style='bold')
            questionary.print(f"- {fastrpi_config.tool_record_path}", style='bold')
            questionary.print(f"- {fastrpi_config.network_record_path}", style='bold')
            questionary.print(f"- {fastrpi_config.tools_folder}", style='bold')
            questionary.print(f"- {fastrpi_config.networks_folder}", style='bold')
            questionary.print(f"- {fastrpi_config.datatypes_folder}", style='bold')
            if questionary.confirm(removal_msg
                                   + f"Do you want to remove the content of {fastrpi_config.fastrpi_home}?").unsafe_ask():
                os.remove(fastrpi_config.tool_record_path)
                os.remove(fastrpi_config.network_record_path)
                shutil.rmtree(fastrpi_config.tools_folder)
                shutil.rmtree(fastrpi_config.networks_folder)
                shutil.rmtree(fastrpi_config.datatypes_folder)
                questionary.print("The files and folders have been removed.", style='bold')
            else:
                questionary.print("The files and folders have not been removed.", style='bold')
                questionary.print("Please remove them yourself or define another FastrPI home directory.",
                                  style='bold')

        response = questionary.select("What container system will you use?",
                                      choices=['Docker', 'Singularity', 'Singularity through Slurm']).unsafe_ask()
        if response == 'Docker':
            if questionary.confirm(
                    "To use Docker you will need to set \n\npreferred_target = 'DockerTarget' \n\nin your Fastr configuration. Do you want to do that now?").unsafe_ask():
                click.edit(filename=fastrpi_config.fastr_home / 'config.py')
            fastrpi_config.container_type = ['docker']
        elif response == 'Singularity':
            if questionary.confirm(
                    "To use Singularity you will need to set \n\npreferred_target = 'SingularityTarget' \n\nin your Fastr configuration. Do you want to do that now?").unsafe_ask():
                click.edit(filename=fastrpi_config.fastr_home / 'config.py')
            fastrpi_config.singularity_dir = questionary.path(
                "What path do you want to use for your Singularity images?",
                default=str(fastrpi_config.singularity_dir)).unsafe_ask()
            fastrpi_config.container_type = ['singularity']
        elif response == 'Singularity through Slurm':
            if questionary.confirm("To use Singularity through Slurm you will need to set \n\n" +
                                   "preferred_target = 'SingularityTarget' \n" +
                                   "execution_plugin = 'SlurmExecution' \n" +
                                   "slurm_partition = --your Slurm partition-- \n" +
                                   "\n" +
                                   f"in your Fastr configuration {str(fastrpi_config.fastr_home / 'config.py')}. " +
                                   "Do you want to do that now?").unsafe_ask():
                click.edit(filename=fastrpi_config.fastr_home / 'config.py')
            fastrpi_config.singularity_dir = questionary.path(
                "What path do you want to use for your Singularity images?",
                default=str(fastrpi_config.singularity_dir)).unsafe_ask()
            fastrpi_config.slurm_pull_partition = questionary.text("What Slurm partition should be used for pulling the images?").unsafe_ask()
            fastrpi_config.container_type = ['singularity_slurm']
        fastrpi_config.write("singularity_dir")
        if fastrpi_config.slurm_pull_partition:
            fastrpi_config.write("slurm_pull_partition")
        fastrpi_config.write('container_type')
        questionary.print("Your FastrPI configuration will be set accordingly.", style='bold')

        if not fastrpi_config.public:
            if fastrpi_config.container_type[0] == 'docker':
                questionary.print("To use the private repositories through Docker, you will need to login with: \n\n"
                                  + "docker login registry.gitlab.com \n\n"
                                  + "Your username and password are your Gitlab username and Access Token respectively.",
                                  style='bold')
            elif fastrpi_config.container_type[0] == 'singularity':
                questionary.print(
                    "To use the private repositories through Singularity, you will need to set the following environment variables: \n\n"
                    + "SINGULARITY_DOCKER_USERNAME=<gitlab_username> \n"
                    + "SINGULARITY_DOCKER_PASSWORD=<gitlab_api_token> \n"
                    + "\n"
                    + "Your username and password are your Gitlab username and Access Token respectively.",
                    style='bold')
            elif fastrpi_config.container_type[0] == 'singularity_slurm':
                questionary.print(
                    "To use the private repositories through Singularity through Slurm, you will need to set the following environment variables: \n\n"
                    + "SINGULARITY_DOCKER_USERNAME=<gitlab_username> \n"
                    + "SINGULARITY_DOCKER_PASSWORD=<gitlab_api_token> \n"
                    + "\n"
                    + "Your username and password are your Gitlab username and Access Token respectively.",
                    style='bold')

    except KeyboardInterrupt as exc:
        questionary.print("Initialization interrupted.", style='bold')
    except FastrPIError as exc:
        questionary.print("Initialization failed.", style='bold')
    else:
        questionary.print("Initialization completed.", style='bold')
