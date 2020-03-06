import os 

current_path = os.path.dirname(__file__)

KEY_PATH = current_path + '/db/key.key'
MODULE_PATH = os.path.dirname(current_path) + '/modules/'
CONFIG_PATH = current_path + '/configuration_files/'
METADATA_PATH = current_path + '/device_metadata/'
LOGGING_PATH = current_path + '/logs/'
DB_PATH = current_path + '/db/'