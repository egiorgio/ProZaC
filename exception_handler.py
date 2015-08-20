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
    logger.warning("Zabbix Error %d: %s" % (exception.code, exception.reason))

def handle_HTTPError_zabbix(exception, caller):
    logger.warning("Zabbix Error %d: %s" % (exception.code, exception.reason))

