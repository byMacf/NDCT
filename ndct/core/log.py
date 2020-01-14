import logging
import sys

from datetime import datetime
from ndct.core.paths import LOGGING_PATH

def log(log_message, level):
    '''
	Summary:
	Logs information to logfile at the specified level.

    Takes:
    log_message: Information to log
    level: Level of which to log the information at
	'''
    logger = logging.getLogger('ndct-logger')

    log_message_types = {
        'debug': logger.debug,
        'info': logger.info,
        'warning': logger.warning,
        'error': logger.error,
        'critical': logger.critical
    }
    
    if not logger.handlers:
        logger.setLevel(logging.DEBUG)

        formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(message)s')

        file_handler = logging.FileHandler(LOGGING_PATH + 'log_' + datetime.now().strftime("%Y-%m-%d_%H:%M:%S") + '.log')
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(formatter)

        stream_handler = logging.StreamHandler(sys.stdout)
        stream_handler.setFormatter(formatter)

        logger.addHandler(file_handler)
        logger.addHandler(stream_handler)

    log_message_types[level](log_message)
