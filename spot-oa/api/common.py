import json
import logging
import os

# Load configuration
CONFIG_FILE = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'config/config.json')
with open(CONFIG_FILE) as config_file:
    CONFIG = json.load(config_file)

# Enable logging, this will also direct built-in DXL log messages.
# See - https://docs.python.org/2/howto/logging-cookbook.html
log_formatter = logging.Formatter('%(asctime)s %(name)s - %(levelname)s - %(message)s')

console_handler = logging.StreamHandler()
console_handler.setFormatter(log_formatter)

logger = logging.getLogger('apache.spot.oa.api')
logger.addHandler(console_handler)
logger.setLevel(logging.INFO)
