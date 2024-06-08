from setuptools import setup, find_packages
import subprocess

# Getting version from github
try:
    tag = subprocess.check_output([
        'git',
        'describe',
        '--abbrev=0',
        '--tags',
    ]).strip().decode()
except subprocess.CalledProcessError:
    tag = ' 0.0.6'

version = tag[1:]

setup(
    name='windows_botify',
    version=version,
    url='https://github.com/Cavecake/windows-botify',
    author='cavecake',
    author_email='cavecake@web.de',
    description=('A simple libary to control windows'),
    license='MIT',
    packages=['windows_botify'
    ],
    install_requires = [

    ]
)