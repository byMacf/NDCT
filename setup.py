from setuptools import setup, find_packages

setup(
	name='ndct',

	# Information
	version='1.0',
	description='A configuration management tool for network device orchestration.',
	long_description='A configuration management tool for network device orchestration through the use of deployments.',

	# Author details
	author='Dominic James Macfarlane',
	author_email='m021859g@student.staffs.ac.uk',

	# Packages
	packages=find_packages(exclude=[""]),

	# Dependencies
	install_requires=['netmiko>=2.3.3', 'Jinja2>=2.10', 'cryptography>=2.6.1', 'Click>=7.0', 'PyYAML>=5.1.2', 'pythonping>=1.0.5'],

	# Entry points
	entry_points={
		'console_scripts': ['ndct = ndct.cli.main:main']
	}
)