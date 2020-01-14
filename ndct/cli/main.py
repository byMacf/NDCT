import click

from ndct.cli import crypt
from ndct.cli import device
from ndct.cli import deployment
from ndct.cli import configuration
from ndct.core.banner import banner
from ndct.core.modules import get_modules

@click.group()
def main():
    '''
    Summary:
    Groups CLI commands to create the CLI menu.
    '''
    banner()
    get_modules()

main.add_command(crypt.crypt, name = 'crypt')
main.add_command(device.device, name = 'device')
main.add_command(deployment.deployment, name = 'deployment')
main.add_command(configuration.configuration, name = 'configuration')