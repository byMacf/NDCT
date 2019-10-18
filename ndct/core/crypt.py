import base64
import os
import hashlib
import json

from getpass import getpass
from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

class Crypt:
	@staticmethod
	def generate_key():
		'''
			Summary:
			Generate a key used for symmetric encryption, using the hash of a user entered password for the salt.

			Returns:
			Encryption key

			Encryption type: 128-bit AES
		'''
		password = getpass(prompt='Encryption key password: ')
		password_bytes = password.encode()
		salt = hashlib.md5(password_bytes).digest()
		kdf = PBKDF2HMAC(
			algorithm=hashes.SHA256(),
			length=32,
			salt=salt,
			iterations=100000,
			backend=default_backend()
		)
		key = base64.urlsafe_b64encode(kdf.derive(password_bytes))

		return key
		#Update this to store the key after it's entered once & delete the key on script end

	@staticmethod
	def create_encrypted_file(filename, data):
		'''
			Summary:
			Create an encrypted file from data that is passed to the function.

			Takes: 
			filename:         		Name of encrypted file
			data:					Data to encrypt
		'''
		key = Crypt.generate_key()
		
		fernet = Fernet(key)
		encrypted_data = fernet.encrypt(str(data).encode())
		
		with open('db/' + filename + '.encrypted', 'wb') as encrypted_file:
			encrypted_file.write(encrypted_data)

	@staticmethod
	def get_encrypted_file_contents(filename):
		'''
			Summary:
			Get the contents of an encrypted file to enable use of the stored data.

			Takes: 
			filename:         		Name of file to get decrypted contents of

			Returns:
			Decrypted file contents 
		'''
		key = Crypt.generate_key()

		with open('db/' + filename + '.encrypted', 'rb') as encrypted_file:
			data = encrypted_file.read()

		fernet = Fernet(key)
		temp_data = fernet.decrypt(data).decode()
		temp_data_list = literal_eval(temp_data)

		return temp_data_list