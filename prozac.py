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

import project_events
import nova_events
import auth
import zabbix_handler
import ceilometer_handler
import configuration

def init_logger():
    """
    Method used to initialize the logging object
    """
    prozac_logger = logging.getLogger('prozac')
    log_levels = {
            'DEBUG': logging.DEBUG, 'INFO': logging.INFO,
            'WARNING': logging.WARNING, 'ERROR': logging.ERROR,
            'CRITICAL': logging.CRITICAL
            }
    prozac_logHandler = TimedRotatingFileHandler(
                    configuration.prozac_log_file,
                    when='D', interval=7, backupCount=4
                    )
    prozac_logHandler.setFormatter(
            logging.Formatter('%(asctime)-4s %(levelname)-4s %(message)s')
            )
    prozac_logger.addHandler(prozac_logHandler)
    prozac_logger.setLevel(
            log_levels[configuration.prozac_log_level]
            )
    prozac_logger.info('********************************************************')
    prozac_logger.info('ProZaC is starting')
    prozac_logger.info(
            'Loading configuration options from %s'%
            (configuration.file_path)
            )

def init_prozac(threads, configuration):
    prozac_logger = logging.getLogger('prozac')
    
    keystone_auth = token_handler.Auth(configuration)
    zabbix_hdl = zabbix_handler.ZabbixHandler(configuration, keystone_auth)
    ceilometer_hdl = ceilometer_handler.CeilometerHandler(configuration, keystone_auth)
    prozac_logger.info('Listeners have been initialized, ready for Zabbix first run')
    zabbix_hdl.first_run()
    nova_hdl = nova_handler.NovaEvents(configuration, zabbix_hdl, ceilometer_hdl)
    project_hdl = project_handler.ProjectEvents(configuration, zabbix_hdl)

    th1 = threading.Thread(target=project_hdl.keystone_listener)
    threads.append(th1)
    th2 = threading.Thread(target=nova_hdl.nova_listener)
    threads.append(th2)
    th3 = threading.Thread(target=ceilometer_hdl.run())
    threads.append(th3)
    [th.start() for th in threads]

if __name__ == '__main__':
    threads = []
    configuration = configuration.Configuration()
    init_logger(configuration)
    init_prozac(threads, configuration)
    # wait for all threads to complete
    [th.join() for th in threads]
    # this will never be printed, as daemon is killed by shell
    prozac_logger.info('Prozac terminated')

