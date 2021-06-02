# This example shows how the logger can be set up to use a custom JSON format.
import logging
import json
import traceback
from datetime import datetime
import copy
import json_logging
import sys

class CustomJSONLog(logging.Formatter):
    """
    Customized logger
    """

    def get_exc_fields(self, record):
        if record.exc_info:
            exc_info = self.format_exception(record.exc_info)
        else:
            exc_info = record.exc_text
        return {'python.exc_info': exc_info}

    @classmethod
    def format_exception(cls, exc_info):
        return ''.join(traceback.format_exception(*exc_info)) if exc_info else ''

    def format(self, record):
        json_log_object = {
                           "level": record.levelname,
                           "message": record.getMessage(),
                           }

        if hasattr(record,'time'):
            json_log_object.update({'userTime':record.time})
        if hasattr(record,'user'):
            json_log_object.update({'function':record.user})
        if hasattr(record,'node'):
            json_log_object.update({'node':record.node})

        return json.dumps(json_log_object)


json_logging.ENABLE_JSON_LOGGING = True
json_logging.init_non_web(enable_json=True,custom_formatter=CustomJSONLog)

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.FileHandler('json.logs'))

with open('plaintext.logs') as f:
    content = f.readlines()
content = [x.strip() for x in content]
for c in content:
    ls = c.split()
    if (len(ls)>4):
      msg = c.split(']')[1]
      logger.warning(''.join(msg), extra={'time':ls[0], 'user':ls[2]}) 
      logger.error(''.join(msg), extra={'time':ls[0], 'user':ls[2]})
      logger.info(''.join(msg), extra={'time':ls[0], 'user':ls[2]})
      logger.debug(''.join(msg), extra={'time':ls[0], 'user':ls[2]})