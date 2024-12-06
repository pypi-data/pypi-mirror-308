import git
from git.exc import InvalidGitRepositoryError
import pytest

from fastrpi.repositorybackend import ToolGitRepository, NetworkGitRepository

def skip_nogit_test():
    try:
        git.Repo(".")
    except OSError:
        return True
    else:
        return False

skip_nogit = pytest.mark.skipif(
    skip_nogit_test(), reason="No Git installed."
)

@skip_nogit
def test_git_folder_doesnt_exist(mock_config):
    """
    When a folder for the Git repository does not exist, a folder needs to be 
    created upon initialization of a subclass of a GitBackendRepository object.
    """
    assert not (mock_config.fastrpi_home / 'tools').exists()
    toolgitrepo = ToolGitRepository(mock_config)
    assert toolgitrepo.local_path == mock_config.fastrpi_home / 'tools'
    assert toolgitrepo.local_path.exists()

    assert not (mock_config.fastrpi_home / 'networks').exists()
    networkgitrepo = NetworkGitRepository(mock_config)
    assert networkgitrepo.local_path == mock_config.fastrpi_home / 'networks'
    assert networkgitrepo.local_path.exists()

def test_git_not_available(monkeypatch, mock_config):
    """
    When Git is not available upon initialization of a subclass of 
    a GitBackendRepository object, execution of FastrPI should seize
    because the core functionality revolves around the Git repositories 
    in the current implementation.
    Availability of Git is tested by running git.Repo. If Git cannot 
    be run, gitpython will return an OSError.
    """

    def mock_broken_git(*args, **kwargs):
        raise OSError("No Git")

    monkeypatch.setattr(git, "Repo", mock_broken_git)

    with pytest.raises(SystemExit) as exc:
        _ = ToolGitRepository(mock_config)
    with pytest.raises(SystemExit) as exc:
        _ = NetworkGitRepository(mock_config)

@skip_nogit
def test_git_repository_doesnt_exist(mock_config):
    """
    If Git is available but a Git repository is not yet initialized, 
    a repository should be created upon initialization of a subclass of 
    a GitBackendRepository object.
    Upon initalization of this object, the origin URL should be set and
    sparse checkout should be initialized with certain default values.
    """
    # Tools
    fastrpi_tools_folder = mock_config.fastrpi_home / 'tools'
    fastrpi_tools_folder.mkdir()
    with pytest.raises(InvalidGitRepositoryError):
        _ = git.Repo(mock_config.fastrpi_home / 'tools')
    toolgitrepo = ToolGitRepository(mock_config)
    _ = git.Repo(mock_config.fastrpi_home / 'tools')

    assert toolgitrepo.origin.url == mock_config.repository_urls['tools_git']

    sparse_checkout_file = toolgitrepo.local_path / '.git' / 'info' / 'sparse-checkout'
    assert sparse_checkout_file.exists()
    with open(sparse_checkout_file, 'r') as fname:
        fname_lines = fname.readlines()  
        print(fname_lines)
        fname_lines = [line.strip() for line in fname_lines]
        assert fname_lines == ['/*', '!/*/', '/datatypes/']

    # Networks
    fastrpi_networks_folder = mock_config.fastrpi_home / 'networks'
    fastrpi_networks_folder.mkdir()
    with pytest.raises(InvalidGitRepositoryError):
        _ = git.Repo(mock_config.fastrpi_home / 'networks')
    networkgitrepo = NetworkGitRepository(mock_config)
    _ = git.Repo(mock_config.fastrpi_home / 'networks')

    assert networkgitrepo.origin.url == mock_config.repository_urls['networks_git']

    sparse_checkout_file = networkgitrepo.local_path / '.git' / 'info' / 'sparse-checkout'
    assert sparse_checkout_file.exists()
    with open(sparse_checkout_file, 'r') as fname:
        fname_lines = fname.readlines()  
        print(fname_lines)
        fname_lines = [line.strip() for line in fname_lines]
        assert fname_lines == ['/*', '!/*/']

@skip_nogit
def test_git_repository_exists(mock_config):
    """
    If the Git repository exists, this repository should be used
    upon a second initialization of this object.
    """
    # Tools
    fastrpi_tools_folder = mock_config.fastrpi_home / 'tools'
    fastrpi_tools_folder.mkdir()
    _ = ToolGitRepository(mock_config)
    toolgitrepo = ToolGitRepository(mock_config)
    assert toolgitrepo.repository == git.Repo(fastrpi_tools_folder)

    # Networks
    fastrpi_networks_folder = mock_config.fastrpi_home / 'networks'
    fastrpi_networks_folder.mkdir()
    _ = NetworkGitRepository(mock_config)
    networkgitrepo = NetworkGitRepository(mock_config)
    assert networkgitrepo.repository == git.Repo(fastrpi_networks_folder)

@pytest.mark.skip()
def test_git_add_sparsecheckout():
    pass

@pytest.mark.skip()
def test_git_remove_sparsecheckout():
    pass

@pytest.mark.skip()
def test_fetch_origin():
    pass

@pytest.mark.skip()
def test_pull_origin():
    pass

@pytest.mark.skip()
def test_create_draft_branch():
    # Includes check_branch_present
    pass

@pytest.mark.skip()
def test_git_pull_package():
    """
    When pulling a package, if all goes well:
    - the sparse checkout folder needs to be added to sparse checkout
    - Origin needs to be pulled, retrieving the files
    - A Manifest object needs to be returned.
    If something goes wrong when pulling origin/ a GitCommandError is raised:
    - the sparse checkout folder needs to be removed from sparse checkout
    - a FastrPIGitError needs to be raised.
    """
    pass


@pytest.mark.skip()
def test_git_push_package():
    """
    When pushing a package, if all goes well:
    - the sparse checkout folder needs to be added to sparse checkout
    - Origin needs to be pulled
    - A draft branch needs to be created
    - To be sure that the folder is empty, it is removed, and a new folder is created.
    - All files from the Manifest need to be copied to the folder.
    - Git adds & commits the file and pushes it.
    """
    pass

