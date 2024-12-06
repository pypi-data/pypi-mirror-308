import pytest

@pytest.mark.skip()
def test_init_backend():
    pass

@pytest.mark.skip()
def test_init_properties():
    pass

@pytest.mark.skip()
def test_check_available():
    pass

@pytest.mark.skip()
def test_publish():
    """
    Options:
    - Everything goes wall
    - PackageChecks fail
    - Errors in the backend
    - 'Finally' during error handling
    """
    pass

@pytest.mark.skip()
def test_install_tools():
    """
    Options:
	- Tool is already installed
	- Tool is not installed, not available
	- Tool is not installed, available, no errors
	- Tool is not installed, available, error handling
    """
    pass

@pytest.mark.skip()
def test_install_networks():
    """
    Options:
	- Network is already installed
	- Network is not installed, not available
	- Network is not installed, available, errors during pulling network
	- Network is not installed, available, tools are already installed
	- Network is not installed, available, tools are not installed, no errors
	- Network is not installed, available, tools are not installed, errors during installing tools 
    """
    pass
