import os
import logging
from datetime import datetime

"""
Config for the log-module
the basicConfig handles the console log
the file_handler handles the log file
usage example:

import logging
import logger as logger

logger = logging.getLogger(__name__)

logger.critical('my message')
logger.warning('my warning message)
logger.info('my info message')

"""
#checks if a directory for the logfiles exists
if not os.path.isdir('logs'):
    os.mkdir('logs')

#logging for the console
logging.basicConfig(
    level=logging.INFO,
    format='%(name)-4s %(levelname)-4s %(message)s',
    datefmt='%Y-%m-%d %H:%M'
)
#logging for log file
file_handler = logging.FileHandler('logs'+ os.path.sep + 'zigbee_log'+datetime.now().strftime('%Y-%m-%d')+'.log', mode='a')
file_handler.setLevel(logging.ERROR)
formatter = logging.Formatter('%(asctime)s %(name)-12s %(levelname)-8s %(message)s', datefmt='%Y-%m-%d %H:%M')
file_handler.setFormatter(formatter)
#add filehandler to the root logger
logging.getLogger('').addHandler(file_handler)