import os

from ndct.core.log import log
from ndct.modules import *

MODULE_PATH = 'Documents/Python/NDCT/ndct/modules'

def get_modules():
    log('Getting modules...', 'info')
    module_list = os.listdir(MODULE_PATH)[1:]
    for module in module_list:
        log('Got module "{}"'.format(module), 'info')