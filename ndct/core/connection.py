from netmiko import Netmiko
from pythonping import ping
from ndct.core.device import Device
from ndct.core.log import log

class Connection(Device):
	def __init__(self, name, ip, username, password, os):
		'''
		Takes: 
		ip:                     IPv4 address of the device
		username:               Username to use for device connection
		password:               Password to use for device connection authentication
		os:                     Operating system of the device
		'''
		super().__init__(name, ip, username, password, os)

	def get_connection(self):
		'''
		Summary:
		Tests device connectivity then creates an SSH connection if successful.

		Returns:
		Connection object
		'''
		ping_result = ping(self.ip, count=1)

		if 'Request timed out' not in str(ping_result):
			log('{} reachable, getting connection...'.format(self.name), 'info')

			connection = Netmiko(
				self.ip,
				username=self.username,
				password=self.password,
				device_type=self.os
			)

			log('Connected to {}'.format(self.name), 'info')
			return connection
		else:
			log('{} not reachable'.format(self.name), 'info')
			return

	def close_connection(self, connection):
		'''
		Summary:
		Closes an SSH connection to a device.
		'''
		connection.disconnect()

		log('Disconnected from {}'.format(self.name), 'info')