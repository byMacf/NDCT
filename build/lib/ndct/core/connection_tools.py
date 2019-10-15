from netmiko import Netmiko
from ndct.core.device_tools import Device
from ndct.core.log import log

class Connection(Device):
    def __init__(self, name, ip, user, password, os):
        '''
	    Takes: 
        ip:                     IPv4 address of the device
        user:                   Username to use for device connection
        password:               Password to use for device connection authentication
        os:                     Operating system of the device
	    '''
        super().__init__(name, ip, user, password, os)

    def get_connection(self):
        '''
		Summary:
		Creates an SSH connection to a device.

        Returns:
        Connection object
	    '''
        connection = Netmiko(
		    self.ip,
		    username=self.user,
		    password=self.password,
		    device_type=self.os
        )

        log('Got connection to {}'.format(self.name), 'info')

        return connection

    def close_connection(self, connection):
        '''
		Summary:
		Closes an SSH connection to a device.
	    '''
        connection.disconnect()

        log('Closed connection to {}'.format(self.name), 'info')
