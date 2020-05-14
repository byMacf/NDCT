import click

from ndct.cli import crypt
from ndct.cli import device
from ndct.cli import deployment
from ndct.cli import configuration
from ndct.core.banner import banner

@click.group()
def main():
    '''
    Summary:
    Network Device Configuration Tool.
    '''
    banner()

main.add_command(crypt.crypt, name = 'crypt')
main.add_command(device.device, name = 'device')
main.add_command(deployment.deployment, name = 'deployment')
main.add_command(configuration.configuration, name = 'configuration')