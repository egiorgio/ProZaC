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
        self.zabbix_admin_user = self.parser.get(zabbix_configs, zabbix_admin_user)
        """
        TODO
        """

