import click
import sys

from ndct.core.deployment import Deployment, deployments
from ndct.core.device import Device, devices
from ndct.core.log import log
    
@click.command(short_help = 'Add a deployment')
@click.option('-n', '--name', help = 'Name', required = True)
@click.option('-t', '--targets', nargs = 0, help = 'Devices to deploy to', required = True)
@click.option('-a', '--action', type = click.Choice(['pull', 'push', 'custom']), help = 'Deployment action', required = True)
@click.argument('targets', nargs = -1)
def add(name, targets, action):
	'''
	Summary:
	Adds a deployment.

	Takes:
	name: Name of deployment
	targets: Devices to target with the deployment
	action: Action to perform custom|routes|config|deploy
	'''
	Deployment.get_deployments_from_file()
	for deployment in deployments:
		if name in deployment:
			log('Cannot add {}, deployment already exists'.format(name), 'info')
			sys.exit(1)
	deployment_object = Deployment(name, list(targets), action)
	deployments.append({name: deployment_object})
	log('Deployment {} with ID {} added successfully'.format(name, deployment_object.deployment_id), 'info')
	Deployment.save_deployments_to_file()

@click.command(short_help = 'Remove a deployment')
@click.option('-n', '--name', help = 'Name', required = True)
def remove(name):
	'''
	Summary:
	Removes a deployment.

	Takes:
	name: Name of deployment to remove
	'''
	Deployment.get_deployments_from_file()
	for deployment in deployments:
		if name in deployment:
			deployments.remove(deployment)
			log('Deployment {} removed successfully'.format(name), 'info')
			Deployment.save_deployments_to_file()
			return
	
	log('Deployment {} does not exist'.format(name), 'error')

@click.command(short_help = 'View a deployment')
@click.option('-n', '--name', help = 'Name', required = True)
def view(name):
	'''
	Summary:
	Prints attributes of a Deployment instance.
	
	Takes:
	name: Name of deployment to view information about
	'''
	Deployment.get_deployments_from_file()
	for deployment in deployments:
		if name in deployment:
			deployment_dict = deployment[name].all()
			log('Name: ' + str(deployment_dict['name']), 'info')
			log('Targets: ' + str(deployment_dict['targets']), 'info')
			log('Action: ' + str(deployment_dict['action']), 'info')
			log('ID: ' + str(deployment_dict['deployment_id']), 'info')
			log('Status: ' + str(deployment_dict['status']), 'info')
			return
	
	log('Deployment {} does not exist'.format(name), 'error')

@click.command(short_help = 'Run a deployment')
@click.option('-n', '--name', help = 'Name', required = True)
def run(name):
	'''
	Summary:
	Calls the run method on a Deployment object.

	Takes:
	name: Name of deployment to run
	'''
	Device.get_devices_from_file()
	Deployment.get_deployments_from_file()
	for deployment in deployments:
		if name in deployment:
			deployment[name].run()
			Deployment.save_deployments_to_file()
			return
	log('Deployment {} does not exist'.format(name), 'error')

@click.group(short_help = 'Deployment commands')
def deployment():
	pass

deployment.add_command(add)
deployment.add_command(remove)
deployment.add_command(view)
deployment.add_command(run)