import json
 
from datetime import datetime
from ndct.core.connection import Connection
from ndct.core.device import Device
from ndct.core.log import log
from ndct.core.paths import MODULE_PATH

class Configuration:
	@staticmethod
	def send_command_to_device(device, command):
		device_information = Device.get_device_information(device)

		if command == 'custom':
			with open(MODULE_PATH + '/' + device_information['os'] + '/commands.json') as command_list_from_file:
				command_list = json.load(command_list_from_file)

			connection_object = Connection(device_information['name'], device_information['ip'], device_information['username'], device_information['password'], device_information['os'])
			device_connection = connection_object.get_connection()

			#output = device_connection.send_command(command_list['commands'][command])

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

	@staticmethod
	def collect_config(device):
		'''
			Summary:
			Collects and saves configuration from a device.

			Takes:
			device:					Device name
		'''
		device_information = Device.get_device_information(device)

		connection_object = Connection(device_information['name'], device_information['ip'], device_information['user'], device_information['password'], device_information['os'])
		show_commands = {
			'juniper': 'show configuration | display set', 
			'cisco_ios': 'show running-config', 
			'cisco_nxos': 'show running-config',
			'cisco_asa': 'show running-config'
		}
		log('Getting device configuration for {}...'.format(device))

		device_connection = connection_object.get_connection()
		device_output = device_connection.send_command(show_commands[os])
		connection_object.close_connection(device_connection)
		config_lines = device_output.splitlines()

		with open('../framework/device_configuration/' + device + '_collected.txt', 'w') as config_file:
			for line in config_lines[1:]:
				config_file.write(line + '\n')
					
		log('Device configuration stored as {}_collected.txt in ../framework/device_configuration/'.format(device), 'info')

		log('Generating device YAML', 'info')
		generate_yaml(device)

	@staticmethod
	def push_config(device):
		'''
			Summary:
			Push configuration to a device.

			Takes:
			device:					Device name
		'''
		device_information = Device.get_device_information(device)

		connection_object = Connection(device_information['name'], device_information['ip'], device_information['user'], device_information['password'], device_information['os'])
		'''save_commands = {
			'juniper': device_connection.commit,
			'cisco_ios': device_connection.save_config,
			'cisco_nxos': device_connection.save_config,
			'cisco_asa': device_connection.save_config
		}'''

		check_files = {
			'juniper': '../framework/checks/juniper.checks',
			'cisco_ios': '../framework/checks/cisco_ios.checks',
			'cisco_nxos': '../framework/checks/cisco_nxos.checks',
			'cisco_asa': '../framework/checks/cisco_asa.checks'
		}

		commands = '../framework/device_configuration/' + device + '_' + device_information['os'] + '_verified.txt'

		if os.stat(commands).st_size != 0:
			log('Got verified config to push', 'info')
		else:
			log('No verified config available to push for {}'.format(device), 'critical')
			return

		log('Pushing configuration to {}...'.format(device), 'info')

		device_connection = connection_object.get_connection()

		#log('Running deployment pre-checks for {}'.format(device), 'info')
		#with open(check_files[os]) as check_file:
			#checks = check_file.read().splitlines()

		#for check in checks:
			#device_connection.send_command(check)
		#Need to evaluate output

		device_output = device_connection.send_config_from_file(commands)
		save_commands[device_information['os']]()

		#log('Running deployment post-checks for {}'.format(device), 'info')
		#for check in checks:
			#device_connection.send_command(check)
		#Need to evaluate output

		connection_object.close_connection(device_connection)

		log('Configuration successfully pushed to {}'.format(device), 'info')

		mark_config_deployed(device)

	@staticmethod
	def get_attribute(device, attribute):
		'''
			Summary:
			Get a device attribute.

			Takes:
			device:					Device name
			attribute:				Attribute to get from device
		'''
		device_information = Device.get_device_information(device)

		connection_object = Connection(device_information['name'], device_information['ip'], device_information['username'], device_information['password'], device_information['os'])
		attribute_commands = {
			'juniper': {
				'bgp': 'show bgp summary',
				'ospf': 'show ospf summary',
				'interfaces': 'show interfaces terse',
				'routes': 'show route'
			},
			'cisco_ios': {
				'bgp': 'show ip bgp summary',
				'ospf': 'show ip ospf summary',
				'interfaces': 'show ip int brief',
				'routes': 'show ip route',
				'config': 'show run'
			},
			'cisco_nxos': {
				'bgp': 'show ip bgp summary'
			},
			'cisco_asa': {
				'bgp' 'show bgp summary'
			}
		}
		log('Getting {} attribute from {}...'.format(attribute, device), 'info')

		device_connection = connection_object.get_connection()
		device_output = device_connection.send_command(attribute_commands[device_information['os']][attribute])
		connection_object.close_connection(device_connection)

		log('Got {} attribute from {}'.format(attribute, device), 'info')
		log(device_output, 'info')