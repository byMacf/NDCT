import click

from ndct.core.deployment import Deployment, deployments
from ndct.core.log import log
    
@click.command(short_help = 'Add a deployment')
@click.option('-n', '--name', help = 'Name', required = True)
@click.option('-t', '--targets', help = 'Devices to deploy to', required = True)
@click.option('-a', '--action', type = click.Choice(['collect', 'push', 'get']), help = 'Deployment action', required = True)
@click.option('-att', '--attribute', type = click.Choice(['bgp', 'ospf', 'eigrp', 'interfaces', 'routes']), help = 'Attribute to get from device(s)')
def add(name, targets, action, attribute):
	'''
	Summary:
	Adds a deployment.
	'''
	Deployment.get_deployments_from_file()
	if attribute:
		deployment_object = Deployment(name, targets, action, attribute=attribute)
		deployments.append({name: deployment_object})
	else:
		deployment_object = Deployment(name, targets, action)
		deployments.append({name: deployment_object})
	log('Deployment {} with ID {} added successfully'.format(name, deployment_object.deployment_id), 'info')
	Deployment.save_deployments_to_file()

@click.command(short_help = 'Remove a deployment')
@click.option('-n', '--name', help = 'Name', required = True)
def remove(name):
	'''
	Summary:
	Removes a deployment.
	'''
	Deployment.get_deployments_from_file()
	for deployment in deployments:
		if name in deployment:
			deployments.remove(deployment)
			log('Deployment {} removed successfully'.format(name))
			Deployment.save_deployments_to_file()
			return
	
	log('Deployment {} does not exist'.format(name), 'error')

@click.command(short_help = 'View a deployment')
@click.option('-n', '--name', help = 'Name', required = True)
def view(name):
	'''
	Summary:
	Prints attributes of a Deployment instance.
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
			if deployment_dict['attribute'] != None:
				log('Attribute: ' + str(deployment_dict['attribute']), 'info')
			return
	
	log('Deployment {} does not exist'.format(name), 'error')

@click.command(short_help = 'Run a deployment')
@click.option('-n', '--name', help = 'Name', required = True)
def run(name):
	'''
	Summary:
	Calls the run method on a Deployment object.
	'''
	Deployment.get_deployments_from_file()
	for deployment in deployments:
		if name in deployment:
			deployment[name].run()
			Deployment.save_deployments_to_file()
			return
	log('Deployment {} does not exist'.format(name), 'error')

@click.group(short_help = 'Deployment operations')
def deployment():
	pass

deployment.add_command(add)
deployment.add_command(remove)
deployment.add_command(view)
deployment.add_command(run)