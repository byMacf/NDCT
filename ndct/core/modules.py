import os

from ndct.core.paths import MODULE_PATH
from ndct.core.log import log

def get_modules():
    '''
	Summary:
	Gets all modules that are installed and sends them to stdout.
	'''
    log('Getting modules...', 'info')
    module_list = os.listdir(MODULE_PATH)[1:]
    for module in module_list:
        log('Got module "{}"'.format(module), 'info')