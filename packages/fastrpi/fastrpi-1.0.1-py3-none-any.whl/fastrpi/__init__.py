import os

from .config import Config
from .record import NetworkInstallRecord, ToolInstallRecord
from .repository import NetworkPackageRepository, ToolPackageRepository

__version__ = '0.1.0dev'

fastrpi_config = Config()
on_rtd = os.environ.get('READTHEDOCS', None) == 'True'
if on_rtd:
    print("On ReadTheDocs: Not initializing.")
else:
    tool_install_record = ToolInstallRecord(fastrpi_config)
    network_install_record = NetworkInstallRecord(fastrpi_config)

    tool_package_repo = ToolPackageRepository(fastrpi_config)
    network_package_repo = NetworkPackageRepository(fastrpi_config)

    closing_statement = (['-'] * 30) + [' ', 'Initalization complete', ' '] + (['-'] * 30)
    print(''.join(closing_statement))
