import click
import sys

from ndct.core.device import Device, devices
from ndct.core.log import log

@click.command(short_help = 'Add a device')
@click.option('-n', '--name', help = 'Name', required = True)
@click.option('-i', '--ip', help = 'IP address', required = True)
@click.option('-u', '--username', help = 'Username to authenticate against', required = True)
@click.option('-p', '--password', help = 'Password to authenticate with', required = True)
@click.option('-o', '--os', type = click.Choice(['cisco_ios', 'juniper', 'cisco_nxos', 'cisco_asa']), help = 'Operating system', required = True)
def add(name, ip, username, password, os):
	'''
	Summary:
	Adds a device.
	'''
	Device.get_devices_from_file()
	for device in devices:
		if name in device:
			log('Cannot add {}, device already exists'.format(name), 'info')
			sys.exit(0)
	device_object = Device(name, ip, username, password, os)
	devices.append({name: device_object})
	log('Device {} added successfully'.format(name), 'info')
	Device.save_devices_to_file()
	#Expand this to add multiple devices at a time

@click.command(short_help = 'Remove a device')
@click.option('-n', '--name', help = 'Name', required = True)
def remove(name):
	'''
	Summary:
	Removes a device.
	'''
	Device.get_devices_from_file()
	for device in devices:
		if name in device:
			devices.remove(device)
			log('Device {} removed successfully'.format(name), 'info')
			Device.save_devices_to_file()
			return

	log('Device {} does not exist'.format(name), 'error')
	#Expand this to remove multiple devices at a time

@click.command(short_help = 'View a device')
@click.option('-n', '--name', help = 'Name', required = True)
def view(name):
	'''
	Summary:
	Prints attributes of a Device instance.
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
		log('Device {} does not exist'.format(name), 'error')

@click.group(short_help = 'Device operations')
def device():
	pass

device.add_command(add)
device.add_command(remove)
device.add_command(view)