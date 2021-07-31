# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

with open('requirements.txt') as f:
	install_requires = f.read().strip().split('\n')

# get version from __version__ variable in housing/__init__.py
from housing import __version__ as version

setup(
	name='housing',
	version=version,
	description='Thirumurugan Housing',
	author='Aerele Technologies Private Limited',
	author_email='vignesh@aerele.in',
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
