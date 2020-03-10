import json
import os
 
from datetime import datetime
from ndct.core.connection import Connection
from ndct.core.device import Device
from ndct.core.log import log
from ndct.core.paths import MODULE_PATH, CONFIG_PATH

class Configuration:
	@staticmethod
	def deploy_custom_configuration(device):
		'''
			Summary:
			Deploys custom configuration from a file to a device.

			Takes:
			device: Device to deploy configuration to
		'''
		rolled_back = False
		device_information = Device.get_device_information(device)

		connection_object = Connection(
			device_information['name'], 
			device_information['ip'], 
			device_information['username'], 
			device_information['password'], 
			device_information['os']
		)
		device_connection = connection_object.get_connection()

		try:
			Configuration.snapshot_configuration(device, device_connection, device_information['os'])
			
			with open(CONFIG_PATH + device + '_custom_commands.txt') as custom_commands_from_file:
				command_list = custom_commands_from_file.read().splitlines()

			log('Pushing configuration to {}...'.format(device), 'info')
			device_connection.send_config_set(command_list)

			Configuration.save_configuration(device_information['os'], device_connection)

			for command in command_list:
				if command != 'no shutdown' and rolled_back == False:
					rolled_back = Configuration.check_configuration_line(
						device, 
						device_connection, 
						device_information['os'], 
						command
					)

			connection_object.close_connection(device_connection)

			Configuration.delete_rollback_configuration(device)
		except AttributeError:
			log('Could not send commands to {}'.format(device), 'error')

	@staticmethod
	def deploy_generated_configuration(device):
		'''
			Summary:
			Deploys configuration generated from device metadata to a device.

			Takes:
			device: Device to deploy configuration to
		'''
		device_information = Device.get_device_information(device)

		connection_object = Connection(
			device_information['name'], 
			device_information['ip'], 
			device_information['username'], 
			device_information['password'], 
			device_information['os']
		)
		device_connection = connection_object.get_connection()

		try: 
			Configuration.snapshot_configuration(device, device_connection, device_information['os'])

			log('Pushing configuration to {}...'.format(device), 'info')
			device_connection.send_config_from_file(CONFIG_PATH + device + '_generated.txt')

			Configuration.save_configuration(device_information['os'], device_connection)

			Configuration.check_full_configuration(
				device, 
				device_connection, 
				device_information['os']
			)

			Configuration.mark_configuration_as_deployed(device)
			connection_object.close_connection(device_connection)
			Configuration.delete_rollback_configuration(device)
		except AttributeError:
			log('Could not send commands to {}, device unreachable'.format(device), 'error')

	@staticmethod
	def get_configuration(device):
		'''
			Summary:
			Gets current configuration from a device and stores it in a file.

			Takes:
			device: Device to get configuration from
		'''
		device_information = Device.get_device_information(device)

		connection_object = Connection(
			device_information['name'], 
			device_information['ip'], 
			device_information['username'], 
			device_information['password'], 
			device_information['os']
		)
		device_connection = connection_object.get_connection()

		try:
			with open(MODULE_PATH + device_information['os'] + '/commands.json') as command_list_from_file:
				command_list = json.load(command_list_from_file)

			log('Getting device configuration for {}...'.format(device), 'info')

			output = device_connection.send_command(command_list['commands']['config'])
			connection_object.close_connection(device_connection)
				
			configuration_lines = output.splitlines()

			with open(CONFIG_PATH + device + '_latest.txt', 'w+') as configuration_file:
				for line in configuration_lines:
					configuration_file.write(line + '\n')
						
			log('Device configuration stored as {}_latest.txt in {}'.format(device, CONFIG_PATH), 'info')
		except AttributeError:
			log('Could not send commands to {}, device unreachable'.format(device), 'error')

	@staticmethod
	def check_configuration_line(device, device_connection, os, configuration_line):
		'''
			Summary:
			Checks if configuration line has been pushed to device.

			Takes:
			device: Device name
			device_connection: Device connection object
			os: Operating system of device
			configuration_line: Configuration line to check for
		'''
		with open(MODULE_PATH + os + '/commands.json') as command_file_temp:
			command_file = json.load(command_file_temp)

		configuration = device_connection.send_command(command_file['commands']['config'])

		if configuration_line in configuration:
			log('[{}] Configuration check passed for "{}"'.format(device, configuration_line), 'info')
			return False
		else:
			log('[{}] Configuration check failed for "{}", rolling back'.format(device, configuration_line), 'info')
			Configuration.rollback_configuration(device, os, device_connection)
			return True

	@staticmethod
	def check_full_configuration(device, device_connection, os):
		'''
			Summary:
			Checks if full configuration has been pushed to device.

			Takes:
			device: Device name
			device_connection: Device connection object
			os: Operating system of device
		'''
		full_configuration_pushed = True

		with open(MODULE_PATH + os + '/commands.json') as command_file_temp:
			command_file = json.load(command_file_temp)

		device_configuration = device_connection.send_command(command_file['commands']['config'])

		with open(CONFIG_PATH + device + '_generated.txt') as pushed_configuration_temp:
			pushed_configuration = pushed_configuration_temp.read().splitlines()

		log('[{}] Checking configuration...'.format(device), 'info')

		for configuration_line in pushed_configuration:
			if configuration_line not in device_configuration:
				full_configuration_pushed = False

		if full_configuration_pushed == True:
			log('[{}] Configuration check push was successful'.format(device), 'info')
		else:
			log('[{}] Configuration check failed, check configuration manually'.format(device), 'info')

	@staticmethod
	def save_configuration(os, device_connection):
		'''
			Summary:
			Saves device configuration persistently.

			Takes:
			os: Operating system of device
			device_connection: device_connection: Device connection object
		'''
		if os == 'vyos':
			device_connection.send_config_set(['commit', 'save', 'exit'])
		elif os == 'cisco_ios':
			output = device_connection.send_command_timing('copy run start')
			if 'Destination filename' in output:
				device_connection.send_command_timing(
					"\n", strip_prompt=False, strip_command=False
				)
			if 'Overwrite the previous' in output:
				device_connection.send_command_timing(
					"\n", strip_prompt=False, strip_command=False
				)
			if 'Warning: Attempting to overwrite an NVRAM configuration previously written' in output:
				device_connection.send_command_timing(
					"\n", strip_prompt=False, strip_command=False
				)

	@staticmethod
	def mark_configuration_as_deployed(device):
		'''
			Summary:
			Marks a generated configuration file as deployed.

			Takes:
			device: Name of device to mark configuration as deployed for
		'''
		with open(CONFIG_PATH + device + '_generated.txt') as generated_configuration_file:
			deployed_configuration = generated_configuration_file.read()

		with open(CONFIG_PATH + device + '_deployed_' + datetime.now().strftime('%Y-%m-%d_%H:%M:%S') + '.txt', 'w') as deployed_configuration_file:
			deployed_configuration_file.write(deployed_configuration)

		log('Marked generated configuration for {} as deployed'.format(device), 'info')

	@staticmethod
	def snapshot_configuration(device, device_connection, os):
		'''
			Summary:
			Takes a snapshot of device configuration for rollback configuration.

			Takes:
			device: Device name
		'''
		try:
			with open(MODULE_PATH + os + '/commands.json') as command_list_from_file:
				command_list = json.load(command_list_from_file)

			log('Creating configuration snapshot for {}...'.format(device), 'info')

			output = device_connection.send_command(command_list['commands']['config'])
				
			configuration_lines = output.splitlines()

			with open(CONFIG_PATH + device + '_rollback.txt', 'w+') as configuration_file:
				for line in configuration_lines:
					configuration_file.write(line + '\n')
						
			log('Configuration snapshot stored as {}_rollback.txt in {}'.format(device, CONFIG_PATH), 'info')
		except AttributeError:
			log('Could not send commands to {}, device unreachable'.format(device), 'error')

	@staticmethod 
	def rollback_configuration(device, os, device_connection):
		'''
			Summary:
			Performs a rollback of device configuration.

			Takes:
			device: Device name
			device_connection: Device connection object
		'''	
		try: 
			with open(CONFIG_PATH + device + '_custom_commands.txt') as custom_commands_from_file:
				command_list_temp = custom_commands_from_file.read().splitlines()

			if os == 'cisco_ios':
				command_list = ['no ' + command for command in command_list_temp]
			elif os == 'vyos':
				command_list = [command.replace('set', 'delete') for command in command_list_temp]

			device_connection.send_config_set(command_list)

			if os == 'vyos':
				device_connection.send_config_set(['commit', 'save'])
			elif os == 'cisco_ios':
					output = device_connection.send_command_timing('copy run start')
					if 'Destination filename' in output:
						device_connection.send_command_timing(
        					"\n", strip_prompt=False, strip_command=False
    					)
					if 'Overwrite the previous' in output:
						device_connection.send_command_timing(
        					"\n", strip_prompt=False, strip_command=False
    					)
					if 'Warning: Attempting to overwrite an NVRAM configuration previously written' in output:
						device_connection.send_command_timing(
        					"\n", strip_prompt=False, strip_command=False
    					)

			log('Device configuration for {} rolled back'.format(device), 'info')
		except AttributeError:
			log('Could not send commands to {}, device unreachable'.format(device), 'error')

	@staticmethod
	def delete_rollback_configuration(device):
		'''
			Summary:
			Delete rollback configuration once deployment succeeds..

			Takes:
			device: Device name
		'''
		os.remove(CONFIG_PATH + device + '_rollback.txt')
		log("Removed rollback file for {}".format(device), 'info')
