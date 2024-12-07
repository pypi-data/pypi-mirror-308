from distutils.core import setup
import setuptools
packages = ['kapaaud2']
setup(name='kapaaud2',
	version='2.7',
	author='szblack',
    packages=packages, 
    package_dir={'requests': 'requests'},)