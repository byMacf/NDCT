import json
 
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
				with open(CONFIG_PATH + device + '_custom_commands.txt') as custom_commands_from_file:
					command_list = custom_commands_from_file.read()

				connection_object = Connection(device_information['name'], device_information['ip'], device_information['username'], device_information['password'], device_information['os'])
				device_connection = connection_object.get_connection()

				output = device_connection.send_command(command_list)

				for command in command_list:
					Configuration.check_configuration(device_connection, device_information['os'], command)

				print('\n')
				log(output + '\n', 'info')

				connection_object.close_connection(device_connection)

			except AttributeError:
				log('Could not send commands to {}, device unreachable'.format(device), 'error')
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
				connection_object = Connection(device_information['name'], device_information['ip'], device_information['username'], device_information['password'], device_information['os'])
				device_connection = connection_object.get_connection()

				output = device_connection.send_config_from_file(CONFIG_PATH + device + '_generated.txt')

				print('\nOutput from {}\n'.format(device))
				log(output + '\n', 'info')

				Configuration.mark_config_deployed(device)
				connection_object.close_connection(device_connection)

			except AttributeError:
				log('Could not send commands to {}, device unreachable'.format(device), 'error')

	@staticmethod
	def check_configuration(connection, os, config_line):
		'''
			Summary:
			Checks if configuration has been pushed to device.

			Takes:
			connection: Device connection object
			os: Operating system of device
			config_line: Configuration to check for
		'''
		command_file = MODULE_PATH + os + 'commands.json'
		configuration = connection.send_command(command_file['commands']['config'])

		if config_line in configuration:
			log('Config check passed for {}'.format(config_line), 'info')
		else:
			log('Config check failed for {}, please review deployment log'.format(config_line), 'info')

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
