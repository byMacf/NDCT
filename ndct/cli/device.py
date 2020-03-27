import click
import sys
import os

from ndct.core.device import Device, devices
from ndct.core.log import log
from ndct.core.paths import DB_PATH

@click.command(short_help = 'Add a device')
@click.option('-n', '--name', help = 'Name', required = True)
@click.option('-i', '--ip', help = 'IP address', required = True)
@click.option('-u', '--username', help = 'Username to authenticate against', required = True)
@click.option('-p', '--password', help = 'Password to authenticate with', required = True)
@click.option('-o', '--os', type = click.Choice(['cisco_ios', 'juniper', 'vyos']), help = 'Operating system', required = True)
def add(name, ip, username, password, os):
	'''
	Summary:
	Adds a device.

	Takes: 
	name: Name of device
	ip: Management IP address of device
	username: Username to authenticate against
	password: Password to authenticate with
	os: Operating system of device cisco_ios|juniper|vyos
	'''
	Device.get_devices_from_file()
	for device in devices:
		if name in device:
			log('[{}] Device already exists'.format(name), 'info')
			sys.exit(1)
	device_object = Device(name, ip, username, password, os)
	devices.append({name: device_object})
	log('[{}] Device added successfully'.format(name), 'info')
	Device.save_devices_to_file()

@click.command(short_help = 'Add devices from a file')
@click.option('-f', '--filename', help = 'File to add devices from', required = True)
def add_from_file(filename):
	Device.get_devices_from_file()
	file_path = DB_PATH + filename
	if os.path.isfile(file_path):
		with open(file_path, 'r') as devices_file:
			all_lines = [line.strip() for line in devices_file.readlines()]
			for device_attribute in range(0, len(all_lines), 5):
				device_exists = False
				for device in devices:
					if all_lines[device_attribute] in device:
						log('[{}] Device already exists'.format(all_lines[device_attribute]), 'info')
						device_exists = True
				if device_exists == False:
					device_object = Device(all_lines[device_attribute], all_lines[device_attribute+1], all_lines[device_attribute+2], all_lines[device_attribute+3], all_lines[device_attribute+4])
					devices.append({all_lines[device_attribute]: device_object})
					log('[{}] Device added successfully'.format(all_lines[device_attribute]), 'info')
	Device.save_devices_to_file()

@click.command(short_help = 'Remove a device')
@click.option('-n', '--name', help = 'Name', required = True)
def remove(name):
	'''
	Summary:
	Removes a device.

	Takes:
	name: Name of device to remove
	'''
	Device.get_devices_from_file()
	for device in devices:
		if name in device:
			devices.remove(device)
			log('[{}] Device removed successfully'.format(name), 'info')
			Device.save_devices_to_file()
			return

	log('[{}] Device does not exist'.format(name), 'error')

@click.command(short_help = 'View a device')
@click.option('-n', '--name', help = 'Name', required = True)
def view(name):
	'''
	Summary:
	Prints attributes of a Device instance.

	Takes: 
	name: Name of device to view information about
	'''
	Device.get_devices_from_file()
	device_information = Device.get_device_information(name)
	if device_information != None:
		log('Name: ' + str(device_information['name']), 'info')
		log('IP: ' + str(device_information['ip']), 'info') 
		log('Username: ' + str(device_information['username']), 'info')
		log('Password: ' + str(device_information['password']), 'info')
		log('OS: ' + str(device_information['os']), 'info')
	else:
		log('[{}] Device does not exist'.format(name), 'error')

@click.group(short_help = 'Device commands')
def device():
	pass

device.add_command(add)
device.add_command(add_from_file)
device.add_command(remove)
device.add_command(view)