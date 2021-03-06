#!/usr/bin/python
"""
Class for requesting authentication tokens to Keystone
This class provides means to requests for authentication tokens to be used with OpenStack's Ceilometer, Nova and RabbitMQ
"""

__copyright__ = "Istituto Nazionale di Fisica Nucleare (INFN)"
__license__ = "Apache 2"

import urllib2
import json
import time, calendar
import logging

class Auth:
    def __init__(self, auth_host, public_port, admin_tenant, admin_user, admin_password):
        self.auth_host = auth_host
        self.public_port = public_port
        self.admin_tenant = admin_tenant
        self.admin_user = admin_user
        self.admin_password = admin_password
        
        self.logger = logging.getLogger('ZCP')
        self.logger.info("Keystone handler initialized")

    def getToken(self):
        """
        Requests and returns an authentication token to be used with OpenStack's Ceilometer, Nova and RabbitMQ
        :return: a tuple with
         - the Keystone token assigned to these credentials a
         - the expiration time (to avoid API REST calls at each Ceilometer or Project thread iteration)
        """
        auth_request = urllib2.Request("http://"+self.auth_host+":"+self.public_port+"/v2.0/tokens")
        auth_request.add_header('Content-Type', 'application/json;charset=utf8')
        auth_request.add_header('Accept', 'application/json')
        auth_data = {"auth": {"tenantName": self.admin_tenant, "passwordCredentials": {"username": self.admin_user, "password": self.admin_password}}}
        auth_request.add_data(json.dumps(auth_data))
        auth_response = urllib2.urlopen(auth_request)
        response_data = json.loads(auth_response.read())

        token_id = response_data['access']['token']['id']
        expiration_time = response_data['access']['token']['expires']
        self.logger.debug("Token expiration time:" + expiration_time)
        expiration_timestamp = calendar.timegm(time.strptime(expiration_time,"%Y-%m-%dT%H:%M:%SZ"))
        self.logger.debug("Expiration timestamp: " + str(expiration_timestamp))

        token = {'id': token_id, 'expires': expiration_timestamp}

        return token
