from pathlib import Path
from fastrpi.config import Config

def test_fastrhome_set(mock_fastr_home_env):
    """
    If $FASTRHOME is set, use that to make FastrPI home, $FASTRHOME/fastrpi.
    """
    config = Config()
    assert config.fastrpi_home == mock_fastr_home_env / 'fastrpi'

def test_fastrhome_exists(mock_fastr_home):
    """
    If default Fastr home, ~/.fastr is set, use that to make FastrPI home, ~/.fastr/fastrpi.
    """
    config = Config()
    print(config.fastrpi_home)
    assert config.fastrpi_home == mock_fastr_home / 'fastrpi'

def test_fastrpihome_set(mock_fastrpi_home_env):
    """
    If $FASTRPIHOME is set, use that to make FastrPI home $FASTRPIHOME
    """
    config = Config()
    assert config.fastrpi_home == mock_fastrpi_home_env 

def test_create_homedir(mock_path_home):
    """
    When instantiating Config() the FastrPI home folder needs to be created and the datatypes folder needs to be
    copied.
    """
    config = Config()
    assert config.fastrpi_home.exists()
    assert config.fastrpi_home == mock_path_home / '.fastrpi'
    assert config.datatypes_folder.exists()

def test_config_file(mock_fastrpi_home_env):
    """
    Tests the default settings for the Config files.
    Tests instantiating Config from a configuration YAML file.
    """

    config_file_urls = {
        'networks_git': 'none',
        'tools_git': 'none',
        'tools_docker': 'none',
    }
    default_urls = {
        'networks_git': 'https://gitlab.com/radiology/infrastructure/resources/fastrpi/fastrpi-networks-public.git',
        'tools_git': 'https://gitlab.com/radiology/infrastructure/resources/fastrpi/fastrpi-tools-public.git',
        'tools_docker': 'registry.gitlab.com/radiology/infrastructure/resources/fastrpi/fastrpi-tools-public',
    }
    config = Config()
    assert config.repository_urls == default_urls

    config = Config("./tests/files/config.yaml")
    assert config.repository_urls == config_file_urls

    config = Config(Path("./tests/files/config.yaml"))
    assert config.repository_urls == config_file_urls

    

