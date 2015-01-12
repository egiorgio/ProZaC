
"""
Exception Handler

Collection of functions to handle HTTPError exceptions coming from Openstack Services or from Zabbix
"""

__authors__ = "Daniele Belfiore, Andrea Valentini Albanelli, Matteo Pergolesi"
__copyright__ = "None"
__license__ = "Apache 2"
__contact__ = "None"
__date__ = "16/10/2014"

__version__ = "1.0"

import sys, traceback
import logging

def handle_HTTPError_openstack(exception, caller):
        solved = False
        if exception.code == 401:
          logging.warning("401. Maybe keystone token expired. Trying to ask for a new one...") 
          newToken = caller.keystone_auth.getToken()
          if newToken is not None:
            logging.warning("Got a new token from keystone.")
            caller.token = newToken
            solved = True
        elif exception.code == 404:
          logging.warning("Openstack resource not found.")
        elif exception.code == 503:
          logging.warning("Openstack service unavailable")
        else:
          logging.warning('Unknown error: %d' % exception.code)
        return solved

def handle_HTTPError_zabbix(exception, caller):
        solved = False
        if exception.code == 401:
          logging.warning("401. Maybe Zabbix token expired. Trying to ask for a new one...")
          #TODO Get a new token from Zabbix
          #newToken = self.keystone_auth.getToken()
          #if newToken is not None:
          #  print "Got a new token."
          #  self.token = newToken
          #  solved = True
        elif exception.code == 404:
          logging.warning("Zabbix resource not found.")
        elif exception.code == 503:
          logging.warning("Zabbix service unavailable")
        else:
           logging.warning('Unknown error: %d' % exception.code)
        return solved
