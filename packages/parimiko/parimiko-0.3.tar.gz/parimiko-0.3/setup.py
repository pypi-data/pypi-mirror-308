from setuptools import setup, find_packages
from setuptools.command.install import install


setup(
    name='parimiko',
    version='0.3',
    author='Varied Master',
    author_email='variedadesmaster@mit.edu',
    description='Corresponding package installer',
    install_requires=[
        'paramiko',
        'layoutspecs'
    ]

)
