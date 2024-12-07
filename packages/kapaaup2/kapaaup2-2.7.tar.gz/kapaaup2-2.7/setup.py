from distutils.core import setup
import setuptools
packages = ['kapaaup2']
setup(name='kapaaup2',
	version='2.7',
	author='szblack',
    packages=packages, 
    package_dir={'requests': 'requests'},)