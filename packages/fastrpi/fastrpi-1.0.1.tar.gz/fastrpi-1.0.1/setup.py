import os
from setuptools import setup, find_packages

version = '1.0.1'

# When building something else than a release (tag) append the job id to the version.
if os.environ.get('CI_COMMIT_TAG'):
    pass
elif os.environ.get('CI_JOB_ID'):
    version += ".{}".format(os.environ['CI_JOB_ID'])

if __name__ == '__main__':
    setup(
        name='fastrpi',
        version=version,
        author='A.G.J. Harms, H.C. Achterberg, A. Versteeg',
        author_email='a.harms@erasmusmc.nl, h.achterberg@erasmusmc.nl, a.versteeg@erasmusmc.nl',
        url='https://gitlab.com/radiology/infrastructure/resources/fastrpi/fastrpi',
        license='Apache 2.0',
        description='FastrPI is a client to interact with a FastrPI repository storing Fastr Networks and (Dockerized) Tools.',
        long_description=open('README.rst').read(),
        long_description_content_type='text/x-rst',
        classifiers=[
            'Development Status :: 4 - Beta',
            'Intended Audience :: Developers',
            'Intended Audience :: Science/Research',
            'Intended Audience :: Healthcare Industry',
            'Intended Audience :: Information Technology',
            'Intended Audience :: Education',
            'License :: OSI Approved :: Apache Software License',
            'Natural Language :: English',
            'Operating System :: OS Independent',
            'Programming Language :: Python :: 3.8',
            'Programming Language :: Python :: 3.9',
            'Programming Language :: Python :: 3.10',
            'Programming Language :: Python :: 3.11',
            'Programming Language :: Python :: 3 :: Only',
            'Topic :: Scientific/Engineering :: Information Analysis',
            'Topic :: System :: Distributed Computing',
            'Topic :: Utilities',
        ],
        packages=find_packages(),
        include_package_data=True,
        install_requires=[
            'Click',
            'docker',
            'fastr>=3.4.0',
            'gitpython',
            'schema',
            'pyyaml',
            'ruamel.yaml',
            'tabulate',
            'requests',
            'questionary'
        ],
        entry_points={
            'console_scripts': [
                'fastrpi = fastrpi.cli:cli',
                'fastrpi-server = fastrpi.server:cli'
            ],
        },
    )
