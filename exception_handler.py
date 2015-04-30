"""
Exception Handler
Collection of functions to handle HTTPError exceptions coming from Openstack Services or from Zabbix
"""

__copyright__ = "Istituto Nazionale di Fisica Nucleare (INFN)"
__license__ = "Apache 2"

import sys, traceback
import logging
logger = logging.getLogger('ZCP')

def handle_HTTPError_openstack(exception, caller):
    message = ""
    if exception.code == 401:
      message = "Unauthorized by Openstack."
    elif exception.code == 404:
      message = "Openstack resource not found."
    elif exception.code == 503:
      message = "Openstack service unavailable."
    else:
      message = "Unknown error."
    logger.warning("Error code %d: %s" % (code, message))

def handle_HTTPError_zabbix(exception, caller):
    message = ""
    if exception.code == 401:
      message = "Unauthorized by Zabbix."
    elif exception.code == 404:
      message = "Zabbix resource not found."
    elif exception.code == 503:
      message = "Zabbix service unavailable."
    else:
      message = "Unknown error."
    logger.warning("Error code %d: %s" % (code, message)) 
