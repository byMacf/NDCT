import uuid
import os

from multiprocessing import Process
from ndct.core.configuration import Configuration
from ndct.core.crypt import Crypt
from ndct.core.log import log
from ndct.core.paths import DB_PATH

deployments = []

class Deployment:
	def __init__(self, name, targets, action, deployment_id=str(uuid.uuid4()), status='Not started'):
		'''
		Takes: 
        name: Deployment name
        targets: Target devices
        action: Action of deployment
		deployment_id: Unique identifier of deployment
		status: Deployment status
		attribute: Deployment attribute - for 'get' action deployments
		'''
		self.name = name
		self.targets = targets
		self.action = action
		self.deployment_id = deployment_id
		self.status = status 

	def all(self):
		'''
		Summary:
		Gets the contents of a Deployment instance.

		Returns:
		Deployment instance contents in dictionairy form
		'''
		return self.__dict__

	def run(self):
		'''
		Summary:
		Runs a deployment.
		'''
		log('[{}] Running deployment'.format(self.name), 'info')

		self.status = 'In progress'
		log('[{}] Updated deployment status to In progress'.format(self.name), 'info')

		if self.action == 'get':
			device_processes = [Process(target=Configuration.get_configuration, args=(target_device,)) for target_device in self.targets]
		elif self.action == 'deploy_generated':
			device_processes = [Process(target=Configuration.deploy_generated_configuration, args=(target_device,)) for target_device in self.targets]
		elif self.action == 'deploy_custom':
			device_processes = [Process(target=Configuration.deploy_custom_configuration, args=(target_device,)) for target_device in self.targets]

		for _process in device_processes:
			_process.start()

		for _process in device_processes:
			_process.join()

		self.status = 'Completed'
		log('[{}] Updated deployment status to Completed'.format(self.name), 'info')

		log('[{}] Deployment completed'.format(self.name), 'info')

	@staticmethod
	def get_deployments_from_file():
		'''
		Summary:
		Gets deployment data from an encrypted file and creates an object stored in the deployments list.
		'''
		if os.path.isfile(DB_PATH + 'deployments'):
			deployments_temp_file = Crypt.get_encrypted_file_contents('deployments')
			for deployment in deployments_temp_file:
				deployment_object = Deployment(
					deployment['name'], 
					deployment['targets'], 
					deployment['action'], 
					deployment_id=deployment['deployment_id'],
					status=deployment['status'],
				)
				deployments.append({deployment['name']: deployment_object})

			log('Got deployments from file', 'info')
		else:
			log('No deployments to get from file', 'info')

	@staticmethod
	def save_deployments_to_file():
		'''
		Summary:
		Saves deployment data to an encrypted file.
		'''
		deployments_to_save = []

		for deployment in deployments:
			for deployment_name, deployment_object in deployment.items():
				deployments_to_save.append(deployment_object.all())

		Crypt.create_encrypted_file('deployments', deployments_to_save)

		log('Saved deployments to file', 'info')
