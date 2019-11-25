import click
import os
import difflib
import yaml

from jinja2 import Environment, FileSystemLoader
from ndct.core.device import Device
from ndct.core.log import log
from ndct.core.paths import METADATA_PATH, MODULE_PATH, CONFIG_PATH

@click.command(short_help = 'Generate a configuration')
@click.option('-n', '--name', help='Name', required = True)
def generate(name):
	'''
	Summary:
	Generates a configuration file for a specified device.
	'''
	Device.get_devices_from_file()

	with open(METADATA_PATH + name + '_metadata.yaml', 'r') as metadata:
		device_metadata = (yaml.safe_load(metadata))

	device_os = Device.get_device_information(name)['os']

	environment = MODULE_PATH + device_os + '/'

	j2_env = Environment(loader=FileSystemLoader(environment), trim_blocks=True, lstrip_blocks=True)

	for device, data in device_metadata.items():
		configuration = j2_env.get_template('template.j2').render(data)
		
	with open(CONFIG_PATH + name + '_generated.txt', 'w') as generated_config_file:
		generated_config_file.write(configuration)

	log('Generated configuration for {}'.format(name), 'info')

@click.command(short_help = 'Verify a configuration')
@click.option('-n', '--name', help='Name', required = True)
@click.option('-os', '--os', help='Operating system', required = True)
def verify(name, os):
	'''
	Summary:
	Marks a generated configuration file as verified, ready to deploy.
	'''
	with open(CONFIG_PATH + name + '_' + os + '_generated.txt', 'r') as generated_config_file:
		config_to_verify = generated_config_file.read()
	with open(CONFIG_PATH + name + '_' + os + '_verified.txt', 'w') as verified_config_file:
		verified_config_file.write(config_to_verify)
	log('Marked generated configuration for {} as verified'.format(name), 'info')

@click.command(short_help = 'List configuration files')
def display():
	'''
	Summary:
	Lists all stored configuration files.
	'''
	configurations = os.listdir(CONFIG_PATH)

	if configurations:
		log('Stored configuration files:', 'info')
		for configuration_file in configurations:
			if configuration_file != '__init__.py':
				log(configuration_file, 'info')
	else:
		log('No configuration files stored', 'info')

@click.command(short_help = 'Show the difference between two configuration files')
@click.option('-c1', '--config1', help='Configuration file 1', required = True)
@click.option('-c2', '--config2', help='Password to authenticate with', required = True)
def diff(config1, config2):
	'''
	Summary:
	Creates and outputs the difference between two device configuration files by comparing them line by line.
	'''
	config1_lines = open(CONFIG_PATH + config1).read().splitlines()
	config2_lines = open(CONFIG_PATH + config2).read().splitlines()
	diff = difflib.unified_diff(config1_lines, config2_lines)

	log('Diff for [{}] < > [{}]'.format(config1, config2), 'info')
	for line in diff:
		if line[0] == '+' and line[1] != '+':
			log('\033[0;32m {}\033[m'.format(line), 'info')
		elif line[0] == '-' and line[1] != '-': 
			log('\033[0;31m {}\033[m'.format(line), 'info')

@click.group(short_help = 'Configuration operations')
def configuration():
	pass

configuration.add_command(generate)
configuration.add_command(verify)
configuration.add_command(display)
configuration.add_command(diff)