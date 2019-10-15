import click
import os
import difflib
import yaml

from jinja2 import Environment, FileSystemLoader
from ndct.core.configuration import Configuration
from ndct.core.log import log

@click.command(short_help = 'Generate a configuration')
@click.option('-n', '--name', help='Name', required = True)
@click.option('-os', '--os', help='Operating system', required = True)
def generate(name, os):
	'''
	Summary:
	Generates a configuration file for a specified device of a specified operating system.
	'''
	for device in name:
		with open('../core/device_metadata/' + name + '_metadata.yaml', 'r') as metadata:
			device_metadata = (yaml.safe_load(metadata))

		environments = {
			'juniper': '../core/os/juniper/',
			'cisco_ios': '../core/os/cisco_ios/',
			'cisco_nxos': '../core/os/cisco_nxos/',
			'cisco_asa': '../core/os/cisco_asa/'
		}
		j2_env = Environment(loader=FileSystemLoader(environments[os]), trim_blocks=True, lstrip_blocks=True)
		configuration_templates = {
			'juniper': 'generate_juniper_config.j2',
			'cisco_ios': 'generate_cisco_ios_config.j2',
			'cisco_nxos': 'generate_cisco_nxos_config.j2',
			'cisco_asa': 'generate_cisco_asa_config.j2'
		}

		for device, data in device_metadata.items():
			configuration = j2_env.get_template(configuration_templates[os]).render(data)
			
		with open('../core/device_configuration/' + name + '_' + os + '_generated.txt', 'w') as generated_config_file:
			generated_config_file.write(configuration)

		log('Generated {} configuration for {}'.format(name, os), 'info')

@click.command(short_help = 'Verify a configuration')
@click.option('-n', '--name', help='Name', required = True)
@click.option('-os', '--os', help='Operating system', required = True)
def verify(name, os):
	'''
	Summary:
	Marks a generated configuration file as verified, ready to deploy.
	'''
	with open('../core/device_configuration/' + name + '_' + os + '_generated.txt', 'r') as generated_config_file:
		config_to_verify = generated_config_file.read()
	with open('../core/device_configuration/' + name + '_' + os + '_verified.txt', 'w') as verified_config_file:
		verified_config_file.write(config_to_verify)
	log('Marked generated configuration for {} as verified'.format(name), 'info')

@click.command(short_help = 'List configuration files')
def display():
	'''
	Summary:
	Lists all stored configuration files.
	'''
	configurations = os.listdir('../core/device_configuration/')

	if configurations:
		for configuration_file in configurations:
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
	config1_lines = open('../core/device_configuration/' + config_1).read().splitlines()
	config2_lines = open('../core/device_configuration/' + config_2).read().splitlines()
	diff = difflib.unified_diff(config1_lines, config2_lines)

	log('Diff for [{}] < > [{}]'.format(config_1, config_2), 'info')
	for line in diff:
		if line[0] == '+' and line[1] != '+':
			log('\033[0;32m {}\033[m'.format(line))
		elif line[0] == '-' and line[1] != '-': 
			log('\033[0;31m {}\033[m'.format(line))

@click.group(short_help = 'Configuration operations')
def configuration():
	pass

configuration.add_command(generate)
configuration.add_command(verify)
configuration.add_command(display)
configuration.add_command(diff)