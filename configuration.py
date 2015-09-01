#!/usr/bin/env python                                                           
"""                                                                             
Proxy for integration of resources between OpenStack's Ceilometer and Zabbix    
                                                                                
This proxy periodically checks for changes in Ceilometer's resources reporting  
them to Zabbix. It is also integrated OpenStack's Nova and RabbitMQ for         
reflecting changes in Projects/Tenants and Instances                            
"""                                                                             
########################   NOTICE   ########################                    
# ProZaC is a fork of ZabbixCeilometer-Proxy (aka ZCP),    #                    
# which is Copyright of OneSource Consultoria Informatica  #                    
# (http://www.onesource.pt).                               #                    
# For further information about ZCP, check its github:     #                    
# https://github.com/clmarques/ZabbixCeilometer-Proxy      #                    
############################################################                    
                                                                                
__copyright__ = 'Istituto Nazionale di Fisica Nucleare (INFN)'                  
__license__ = 'Apache 2'

import sys                                                                      
import getopt
import ConfigParser                                                             
import os
import logging

class Configuration:
    def __init__(self, filename):
        """                                                                     
        Method to create a Configuration type Object

        It reads configuration for ProZaC in configuration file.
        ex. prozac.conf

        :param filename: The name of the configuration file (assuming
        it resides int the same path of the executable).
        """
        self.file_path = os.path.join(os.path.dirname(__file__), filename)
        self.parser = ConfigParser.SafeConfigParser()
        self.parser.readfp(open(file_path))
        
        self.zabbix_admin_username = readfp.get('zabbix', 'admin_username')
        self.zabbix_admin_password = readfp.get('zabbix', 'admin_password')
        self.zabbix_host = readfp.get('zabbix', 'host')
        self.zabbix_port = readfp.get('zabbix', 'port')
        self.zabbix_protocol = readfp.get('zabbix', 'protocol')

        self.rpc_keystone_type = readfp.get('rpc', 'keystone_type')
        self.rpc_keystone_host = readfp.get('rpc', 'keystone_host')
        self.rpc_keystone_username = readfp.get('rpc', 'keystone_username')
        self.rpc_keystone_password = readfp.get('rpc', 'keystone_password')
        self.rpc_nova_type = readfp.get('rpc', 'nova_type')             
        self.rpc_nova_host = readfp.get('rpc', 'nova_host')             
        self.rpc_nova_username = readfp.get('rpc', 'nova_username')     
        self.rpc_nova_password = readfp.get('rpc', 'nova_password')

        self.ceilometer_api_host = readfp.get('ceilometer', 'api_host')
        self.ceilometer_api_port = readfp.get('ceilometer', 'api_port')

        self.keystone_admin_username = readfp.get('keystone', 'admin_username')
        self.keystone_admin_password = readfp.get('keystone', 'admin_password') 
        self.keystone_admin_tenant = readfp.get('keystone', 'admin_tenant')
        self.keystone_host = readfp.get('keystone', 'host')
        self.keystone_admin_port = readfp.get('keystone', 'admin_port')
        self.keystone_public_port = readfp.get('keystone', 'public_port')
        self.keystone_nova_compute_port = readfp.get('keystone', 'nova_compute_port')

        self.prozac_polling_interval = readfp.get('prozac', 'polling_interval')
        self.prozac_zabbix_template_name = readfp.get(
                                            'prozac', 'zabbix_template_name')
        self.prozac_zabbix_proxy_name = readfp.get(
                                            'prozac', 'zabbix_proxy_name')
        self.prozac_log_file = readfp.get('prozac', 'log_file')
        self.prozac_log_level = readfp.get('prozac', 'log_level')

