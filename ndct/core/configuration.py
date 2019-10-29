import json
 
from datetime import datetime
from ndct.core.connection import Connection
from ndct.core.device import Device
from ndct.core.log import log
from ndct.core.paths import MODULE_PATH, CONFIG_PATH

class Configuration:
	@staticmethod
	def send_command_to_device(device, command):
		device_information = Device.get_device_information(device)
		if command == 'custom':
			with open(CONFIG_PATH + device + '_custom_commands.txt') as custom_commands_from_file:
				command_list = custom_commands_from_file.read()

			connection_object = Connection(device_information['name'], device_information['ip'], device_information['username'], device_information['password'], device_information['os'])
			device_connection = connection_object.get_connection()

			output = device_connection.send_command(command_list)

			print('\n')
			log(output + '\n', 'info')

			connection_object.close_connection(device_connection)

		elif command == 'routes':
			try: 
				with open(MODULE_PATH + '/' + device_information['os'] + '/commands.json') as command_list_from_file:
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
				with open(MODULE_PATH + '/' + device_information['os'] + '/commands.json') as command_list_from_file:
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

				#log('Generating device YAML', 'info')
				#generate_yaml(device)
			except AttributeError:
				log('Could not send commands to {}, device unreachable'.format(device), 'error')
		else:
			pass

	@staticmethod
	def generate_yaml(device):
		log('Generated YAML file for {}'.format(device), 'info')

	@staticmethod
	def mark_config_deployed(device):
		'''
			Summary:
			Marks a verified configuration file as deployed.

			Takes:
			device:					Device name
		'''
		device_information = Device.get_device_information(device)

		with open('../framework/device_configuration/' + device + '_' + device_information['os'] + '_verified.txt', 'r') as verified_config_file:
			deployed_config = verified_config_file.read()

		with open('../framework/device_configuration/' + device + '_' + device_information['os'] + '_deployed_' + datetime.now().strftime('%Y-%m-%d_%H:%M:%S') + '.txt', 'w') as deployed_config_file:
			deployed_config_file.write(deployed_config)

		log('Marked verified configuration for {} as deployed'.format(device), 'info')
