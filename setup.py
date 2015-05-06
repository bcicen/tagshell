import os
import shutil
from pwd import getpwnam
from setuptools import setup, find_packages
from tagshell import __version__

requires = [ 'pyyaml', 'pssh' ]

if os.environ.has_key('SUDO_USER'):
    user = os.environ['SUDO_USER']
else:
    user = os.environ['USER']

home = getpwnam(user).pw_dir
uid  = getpwnam(user).pw_uid
gid  = getpwnam(user).pw_gid

config_dir = home + '/.tagshell'
config_file = home + '/.tagshell/config.yaml'
tag_file = home + '/.tagshell/tags.yaml'

if not os.path.isdir(config_dir):
    os.mkdir(config_dir)
    os.chown(config_dir,uid,gid)

if not os.path.isfile(config_file):
    shutil.copyfile('config_example.yaml', config_file)
    os.chown(config_dir,uid,gid)

if not os.path.isfile(tag_file):
    shutil.copyfile('tags_example.yaml', tag_file)
    os.chown(config_dir,uid,gid)

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
