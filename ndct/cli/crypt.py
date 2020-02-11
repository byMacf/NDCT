import click
import json

from ast import literal_eval
from cryptography.fernet import Fernet
from ndct.core.crypt import Crypt
from ndct.core.log import log

@click.command(short_help = 'Decrypt a file')
@click.option('-f', '--filename', type = click.Choice(['devices', 'deployments']), help = 'Filename', required = True)
def decrypt(filename):
	'''
		Summary:
		Create a decrypted copy of a file in JSON format.

		Takes: 
		filename: Name of decrypted file
	'''
	key = Crypt.get_key()

	with open('Documents/Python/NDCT/ndct/core/db/' + filename, 'rb') as encrypted_file:
		data = encrypted_file.read()

	fernet = Fernet(key)
	decrypted_data = literal_eval(fernet.decrypt(data).decode())

	with open('Documents/Python/NDCT/ndct/core/db/' + filename + '.decrypted', 'w') as decrypted_file:
		json.dump(decrypted_data, decrypted_file, indent=4)

	log('Generated decrypted file {}.decrypted'.format(filename), 'info')

@click.group(short_help = 'Crypt commands')
def crypt():
	pass

crypt.add_command(decrypt)