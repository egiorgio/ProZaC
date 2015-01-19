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
    solved = False
    if exception.code == 401:
        logger.warning("401. Maybe keystone token expired. Trying to ask for a new one...")
        newToken = caller.keystone_auth.getToken()
        if newToken is not None:
            logger.warning("Got a new token from keystone.")
            caller.token = newToken
            solved = True
    elif exception.code == 404:
        logger.warning("Openstack resource not found.")
    elif exception.code == 503:
        logger.warning("Openstack service unavailable")
    else:
        logger.warning('Unknown error: %d' % exception.code)
    return solved

def handle_HTTPError_zabbix(exception, caller):
    solved = False
    if exception.code == 401:
        logger.warning("401. Maybe Zabbix token expired. Trying to ask for a new one...")
    elif exception.code == 404:
        logger.warning("Zabbix resource not found.")
    elif exception.code == 503:
        logger.warning("Zabbix service unavailable")
    else:
        logger.warning('Unknown error: %d' % exception.code)
    return solved
