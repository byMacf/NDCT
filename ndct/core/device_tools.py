import os

from ndct.core.crypt_tools import Crypt
from ndct.core.log import log

device_list = []

class Device():
	def __init__(self, name, ip, user, password, os):
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
		self.user = user
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
		if os.path.isfile('data/devices.encrypted'):
			devices_temp_file = Crypt.get_encrypted_file_contents('data/devices.encrypted')
			for device in devices_temp_file:
				device_object = Device(
					device['name'], 
					device['ip'], 
					device['user'], 
					device['password'], 
					device['os']
				)
				device_list.append({device['name']: device_object})
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

		for device in device_list:
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
		for device in device_list:
			if device_name in device:
				device_information = device[device_name].all()

				return device_information

		return None

'''def device_decorator(get=False, save=False):
	def real_decorator(function):
		def wrapper():
			if get == True:
				if os.path.isfile('/data/devices.encrypted'):
					devices_temp_file = Crypt.get_encrypted_file_contents('/data/devices.encrypted')
					for device in devices_temp_file:
						device_object = Device(
							device['name'], 
							device['ip'], 
							device['user'], 
							device['password'], 
							device['os']
						)
						device_list.append({device['name']: device_object})
						log('Got devices from file', 'info')
				else:
					log('No devices to get from file', 'info')
			function()
			if save == True:
				devices_to_save = []

				for device in device_list:
					for device_name, device_object in device.items():
						devices_to_save.append(device_object.all())

				Crypt.create_encrypted_file('/data/devices', devices_to_save)

				log('Saved devices to file', 'info')
		return wrapper
	return real_decorator'''