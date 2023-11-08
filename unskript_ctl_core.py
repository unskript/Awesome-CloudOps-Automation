#!/usr/bin/env python
#
# Copyright (c) 2023 unSkript.com
# All rights reserved.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE
#
#
import logging
from abc import ABC, abstractmethod, abstractproperty


class Logger:
    def __init__(self, log_filename, log_level=logging.INFO):
        self.log_filename = log_filename
        self.log_level = log_level 
        self.logger = self.setup()
    
    def setup(self):
        logger = logging.getLogger(__name__)
        logger.setLevel(self.log_level)
        formatter = logging.Formatter('%(asctime)s - %(name) - %(levelname)s - %(message)s')
        
        file_handler = logging.FileHandler(self.log_filename)
        file_handler.setFormatter(formatter)

        logger.addHandler(file_handler)
        
        return logger 
    
    def log(self, message):
        if not message:
            return
        self.logger.log(self.log_level, message)

class CtlCore(ABC):
    def __init__(self):
        self.logger = Logger("unskript_ctl.log")
    
    def configParser(self):
        pass 

    def auditManager(self):
        pass


class ConfigParser(CtlCore):
    pass 


class ConfigParserImpl(ConfigParser):
    pass 


class DisplayManager(CtlCore):
    pass 

class DisplayManagerImpl(DisplayManager):
    pass 


class Notification(CtlCore):
    pass

class NotificationImpl(Notification):
    pass 

  