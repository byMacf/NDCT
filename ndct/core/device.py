import os

from ndct.core.crypt import Crypt
from ndct.core.log import log

devices = []

class Device():
	def __init__(self, name, ip, username, password, os):
		'''
		Takes: 
		name:					Device name 
		ip:                     IPv4 address of the device
		user:                   Username to use for device connection
		password:               Password to use for device connection authentication
		os:                     Operating system of the device
		'''
		self.name = name
		self.ip = ip
		self.username = username
		self.password = password
		self.os = os

	def all(self):
		'''
		Summary:
		Gets the contents of a Device instance.

		Returns:
		Device instance contents in dictionairy form.
		'''
		return self.__dict__

	@staticmethod
	def get_devices_from_file():
		'''
		Summary:
		Gets device data from an encrypted file.
		'''
		if os.path.isfile('Documents/Python/NDCT/ndct/core/db/devices'):
			devices_temp_file = Crypt.get_encrypted_file_contents('devices')
			for device in devices_temp_file:
				device_object = Device(
					device['name'], 
					device['ip'], 
					device['username'], 
					device['password'], 
					device['os']
				)
				devices.append({device['name']: device_object})
			log('Got devices from file', 'info')
		else:
			log('No devices to get from file', 'info')

	@staticmethod
	def save_devices_to_file():
		'''
		Summary:
		Saves device data to an encrypted file.
		'''
		devices_to_save = []

		for device in devices:
			for device_name, device_object in device.items():
				devices_to_save.append(device_object.all())

		Crypt.create_encrypted_file('devices', devices_to_save)

		log('Saved devices to file', 'info')

	@staticmethod
	def get_device_information(device_name):
		'''
		Summary:
		Gets the contents of a Device instance.

		Returns:
		Device instance contents in dictionairy form.
		'''
		for device in devices:
			if device_name in device:
				device_information = device[device_name].all() 
				return device_information

		return None
