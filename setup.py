from setuptools import setup, find_packages

setup(
	name='ndct',

	# Information
	version='1.0',
	description='A configuration management tool for network device orchestration.',
	long_description='A configuration management tool for network device orchestration through the use of deployments.',

	# Author details
	author='Dominic Macfarlane',
	author_email='dominicmacfarlane1@hotmail.com',

	# Packages
	packages=find_packages(exclude=["frontend"]),

	# Dependencies
	install_requires=['netmiko>=2.3.3', 'Jinja2>=2.10', 'cryptography>=2.6.1', 'Flask>=1.0.2', 'Click>=7.0', 'PyYAML>=5.1.2'],

	# Entry points
	entry_points={
		'console_scripts': ['ndct = ndct.cli.main:main']
	}
)