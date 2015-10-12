import os
import shutil
from pwd import getpwnam
from setuptools import setup, find_packages

exec(open('tagshell/version.py').read())

requires = [ 'pyyaml', 'pssh' ]

if os.environ.has_key('SUDO_USER'):
    user = os.environ['SUDO_USER']
else:
    user = os.environ['USER']

home = getpwnam(user).pw_dir
uid  = getpwnam(user).pw_uid
gid  = getpwnam(user).pw_gid

config_dir  = home + '/.tagshell'
log_dir     = config_dir + '/logs'
config_file = config_dir + '/config.yaml'
tag_file    = config_dir + '/tags.yaml'

for dir in config_dir,log_dir:
    if not os.path.isdir(dir):
        os.mkdir(dir)
        os.chown(dir,uid,gid)

if not os.path.isfile(config_file):
    shutil.copyfile('config_example.yaml', config_file)
    os.chown(config_dir,uid,gid)

if not os.path.isfile(tag_file):
    shutil.copyfile('tags_example.yaml', tag_file)
    os.chown(config_dir,uid,gid)

setup(name='tagshell',
        version=version,
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
