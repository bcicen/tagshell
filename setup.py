import os
import shutil
from setuptools import setup, find_packages
from tagshell import __version__

requires = [ 'pyyaml', 'pssh' ]

setup(name='tagshell',
        version=__version__,
        description='tagshell',
        author='Bradley Cicenas',
        author_email='bradley.cicenas@gmail.com',
        packages=find_packages(),
        include_package_data=True,
        install_requires=requires,
        tests_require=requires,
        entry_points = {
        'console_scripts' : [ 'tagshell = tagshell.cli:main' ]
        }
)
