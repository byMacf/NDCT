import logging
import sys

from datetime import datetime

def log(log_message, level):
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

        file_handler = logging.FileHandler('Documents/Python/NDCT/ndct/core/logs/log_' + datetime.now().strftime("%Y-%m-%d_%H:%M:%S") + '.log')
        #Make this absolute path
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(formatter)

        stream_handler = logging.StreamHandler(sys.stdout)
        stream_handler.setFormatter(formatter)

        logger.addHandler(file_handler)
        logger.addHandler(stream_handler)

    log_message_types[level](log_message)
