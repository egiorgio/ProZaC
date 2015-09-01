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
import threading
import logging
from logging.handlers import TimedRotatingFileHandler

import project_handler
import nova_handler
import readFile
import token_handler
import zabbix_handler
import ceilometer_handler
import configuration

def init_logger():
    """
    Method used to initialize the logging object
    """
    zcp_logger = logging.getLogger('ZCP')
    log_levels = {
            'DEBUG': logging.DEBUG, 'INFO': logging.INFO,
            'WARNING': logging.WARNING, 'ERROR': logging.ERROR,
            'CRITICAL': logging.CRITICAL
            }
    zcp_logHandler = TimedRotatingFileHandler(
                    conf_file.read_option('zcp_configs', 'log_file'),
                    when='D', interval=7, backupCount=4
                    )
    zcp_logHandler.setFormatter(
            logging.Formatter('%(asctime)-4s %(levelname)-4s %(message)s')
            )
    zcp_logger.addHandler(zcp_logHandler)
    zcp_logger.setLevel(
            log_levels[conf_file.read_option('zcp_configs', 'log_level')]
            )
    zcp_logger.info('********************************************************')
    zcp_logger.info('Prozac is starting')
    zcp_logger.info(
            'Loading configuration options from %s'%
            (conf_file.conf_file_name)
            )

def init_zcp(threads, configuration):
    zcp_logger = logging.getLogger('ZCP')
    # Creation of the Auth keystone-dedicated authentication class
    # Responsible for managing AAA related requests
    keystone_auth = token_handler.Auth(configuration)
    # Creation of the Zabbix Handler class
    # Responsible for the communication with Zabbix
    zabbix_hdl = zabbix_handler.ZabbixHandler(configuration, keystone_auth)
    # Creation of the Ceilometer Handler class
    # Responsible for the communication with OpenStack's Ceilometer,
    # polling for changes every N seconds
    ceilometer_hdl = ceilometer_handler.CeilometerHandler(configuration, keystone_auth)
    zcp_logger.info('Listeners have been initialized, ready for Zabbix first run')
    zabbix_hdl.first_run()
    # Creation of the Nova Handler class
    # Responsible for detecting the creation of new instances in OpenStack,
    # translated then to Hosts in Zabbix
    # nova_hdl = nova_handler.NovaEvents(
    #       conf_file.read_option('os_rabbitmq', 'rabbit_host'),
    #       conf_file.read_option('os_rabbitmq', 'rabbit_user'),
    #       conf_file.read_option('os_rabbitmq', 'rabbit_pass'), zabbix_hdl,
    #       ceilometer_hdl)
    nova_hdl = nova_handler.NovaEvents(configuration, zabbix_hdl, ceilometer_hdl)
    # Creation of the Project Handler class
    # Responsible for detecting the creation of new tenants in OpenStack,
    # translated then to HostGroups in Zabbix
    # project_hdl = project_handler.ProjectEvents(
    #       conf_file.read_option('os_rabbitmq', 'rabbit_host'),
    #       conf_file.read_option('os_rabbitmq', 'rabbit_user'),
    #       conf_file.read_option('os_rabbitmq', 'rabbit_pass'), zabbix_hdl)
    project_hdl = project_handler.ProjectEvents(configuration, zabbix_hdl)

    th1 = threading.Thread(target=project_hdl.keystone_listener)
    threads.append(th1)
    th2 = threading.Thread(target=nova_hdl.nova_listener)
    threads.append(th2)
    th3 = threading.Thread(target=ceilometer_hdl.run())
    threads.append(th3)
    [th.start() for th in threads]

if __name__ == '__main__':
    init_logger()
    threads = []
    configuration = configuration.Configuration()
    init_zcp(threads, configuration)
    # wait for all threads to complete
    [th.join() for th in threads]
    # this will never be printed, as daemon is killed by shell
    zcp_logger.info('Prozac terminated')

