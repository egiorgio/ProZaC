"""
Class for reading the configuration file
Uses the ConfigParser lib to return the values present in the config file
"""

__authors__ = "Claudio Marques, David Palma, Luis Cordeiro"
__copyright__ = "Copyright (c) 2014 OneSource Consultoria Informatica, Lda"
__license__ = "Apache 2"

import ConfigParser
import os

class ReadConfFile:
    config = None
    def __init__(self, file = os.path.join(os.path.dirname(__file__), 'proxy.conf')):
        """
        Method to read from conf file specific options
        :param file:
        """
        self.conf_file_name = file
        self.config = ConfigParser.SafeConfigParser()
        self.config.readfp(open(file))

    def read_option(self, group, name):
        """
        :return:
        """
        value = self.config.get(group, name)
        return value
