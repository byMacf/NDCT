import json
import os
 
from datetime import datetime
from ndct.core.connection import Connection
from ndct.core.device import Device
from ndct.core.log import log
from ndct.core.paths import MODULE_PATH, CONFIG_PATH

class Configuration:
	@staticmethod
	def send_command_to_device(device, command):
		'''
			Summary:
			Sends command(s) to a device.

			Takes:
			device: Device to send command(s) to
			command: Command(s) to send
		'''
		device_information = Device.get_device_information(device)
		if command == 'custom':
			try:
				device_connection = Configuration.snapshot_config(device)
				
				with open(CONFIG_PATH + device + '_custom_commands.txt') as custom_commands_from_file:
					command_list = custom_commands_from_file.read()
				
				commands = command_list.splitlines()
				device_connection.send_config_from_file(CONFIG_PATH + device + '_custom_commands.txt')

				for command in commands:
					Configuration.check_configuration(device, device_connection, device_information['os'], command)

				#Connection.close_connection(device_connection)
			except AttributeError:
				log('Could not send commands to {}'.format(device), 'error')
		elif command == 'routes':
			try: 
				with open(MODULE_PATH + device_information['os'] + '/commands.json') as command_list_from_file:
					command_list = json.load(command_list_from_file)

				connection_object = Connection(device_information['name'], device_information['ip'], device_information['username'], device_information['password'], device_information['os'])
				device_connection = connection_object.get_connection()

				output = device_connection.send_command(command_list['commands'][command])

				print('\nOutput from {}\n'.format(device))
				log(output + '\n', 'info')

				connection_object.close_connection(device_connection)
			except AttributeError:
				log('Could not send commands to {}, device unreachable'.format(device), 'error')
		elif command == 'config':
			try:
				with open(MODULE_PATH + device_information['os'] + '/commands.json') as command_list_from_file:
					command_list = json.load(command_list_from_file)
				
				connection_object = Connection(device_information['name'], device_information['ip'], device_information['username'], device_information['password'], device_information['os'])
				device_connection = connection_object.get_connection()

				log('Getting device configuration for {}...'.format(device), 'info')

				output = device_connection.send_command(command_list['commands'][command])
				connection_object.close_connection(device_connection)
				
				config_lines = output.splitlines()

				with open(CONFIG_PATH + device + '_latest.txt', 'w+') as config_file:
					for line in config_lines:
						config_file.write(line + '\n')
						
				log('Device configuration stored as {}_latest.txt in {}'.format(device, CONFIG_PATH), 'info')
			except AttributeError:
				log('Could not send commands to {}, device unreachable'.format(device), 'error')
		elif command == 'deploy':
			try: 
				Configuration.snapshot_config(device)

				connection_object = Connection(device_information['name'], device_information['ip'], device_information['username'], device_information['password'], device_information['os'])
				device_connection = connection_object.get_connection()

				output = device_connection.send_config_from_file(CONFIG_PATH + device + '_generated.txt')

				print('\nOutput from {}\n'.format(device))
				log(output + '\n', 'info')

				for command in output:
					Configuration.check_configuration(device, device_connection, device_information['os'], command)

				Configuration.mark_config_deployed(device)
				connection_object.close_connection(device_connection)
			except AttributeError:
				log('Could not send commands to {}, device unreachable'.format(device), 'error')

		Configuration.delete_rollback_config(device)

	@staticmethod
	def check_configuration(device, connection, os, config_line):
		'''
			Summary:
			Checks if configuration has been pushed to device.

			Takes:
			device: Device name
			connection: Device connection object
			os: Operating system of device
			config_line: Configuration to check for
		'''
		with open(MODULE_PATH + os + '/commands.json') as command_file_temp:
			command_file = json.load(command_file_temp)

		configuration = connection.send_command(command_file['commands']['config'])

		if config_line in configuration:
			log('Configuration check passed for "{}"'.format(config_line), 'info')
		else:
			log('Configuration check failed for "{}", rolling back'.format(config_line), 'info')
			Configuration.rollback_config(device, connection)

	@staticmethod
	def mark_config_deployed(device):
		'''
			Summary:
			Marks a generated configuration file as deployed.

			Takes:
			device: Name of device to mark configuration as deployed for
		'''
		device_information = Device.get_device_information(device)

		with open(CONFIG_PATH + device + '_' + device_information['os'] + '_generated.txt', 'r') as generated_config_file:
			deployed_config = generated_config_file.read()

		with open(CONFIG_PATH + device + '_' + device_information['os'] + '_deployed_' + datetime.now().strftime('%Y-%m-%d_%H:%M:%S') + '.txt', 'w') as deployed_config_file:
			deployed_config_file.write(deployed_config)

		log('Marked generated configuration for {} as deployed'.format(device), 'info')

	@staticmethod
	def snapshot_config(device):
		device_information = Device.get_device_information(device)

		try:
			with open(MODULE_PATH + device_information['os'] + '/commands.json') as command_list_from_file:
				command_list = json.load(command_list_from_file)
				
			connection_object = Connection(device_information['name'], device_information['ip'], device_information['username'], device_information['password'], device_information['os'])
			device_connection = connection_object.get_connection()

			log('Creating configuration snapshot for {}...'.format(device), 'info')

			output = device_connection.send_command(command_list['commands']['config'])
				
			config_lines = output.splitlines()

			with open(CONFIG_PATH + device + '_rollback.txt', 'w+') as config_file:
				for line in config_lines:
					config_file.write(line + '\n')
						
			log('Configuration snapshot stored as {}_rollback.txt in {}'.format(device, CONFIG_PATH), 'info')

			return device_connection
		except AttributeError:
			log('Could not send commands to {}, device unreachable'.format(device), 'error')

	@staticmethod 
	def rollback_config(device, device_connection):
		try: 
			device_connection.send_config_from_file(CONFIG_PATH + device + '_rollback.txt')

			log('Device configuration for {} rolled back'.format(device), 'info')
		except AttributeError:
			log('Could not send commands to {}, device unreachable'.format(device), 'error')

	@staticmethod
	def delete_rollback_config(device):
		os.remove(CONFIG_PATH + device + '_rollback.txt')
		log("Removed rollback file for {}".format(device), 'info')