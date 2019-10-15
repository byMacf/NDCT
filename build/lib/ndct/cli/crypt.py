import click

from ast import literal_eval
from cryptography.fernet import Fernet
from ndct.core.crypt_tools import Crypt
from ndct.core.log import log

@click.command(short_help = 'Decrypt a file')
@click.option('-f', '--filename', help = 'Filename', required = True)
def decrypt(filename):
	'''
		Summary:
		Create a decrypted copy of a file.

		Takes: 
		filename:         		Name of decrypted file
	'''
	key = Crypt.generate_key()

	with open('../core/data' + filename + '.encrypted', 'rb') as encrypted_file:
		data = encrypted_file.read()

	fernet = Fernet(key)
	decrypted_data = literal_eval(fernet.decrypt(data).decode())

	with open('../core/data' + filename + '.decrypted', 'w') as decrypted_file:
		json.dump(decrypted_data, decrypted_file, indent=4)

	log('Generated decrypted file {}.decrypted'.format(filename), 'info')

@click.group(short_help = 'Crypt operations')
def crypt():
	pass

crypt.add_command(decrypt)