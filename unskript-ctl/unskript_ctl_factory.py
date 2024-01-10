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
import os
import yaml
import logging 
import json
import glob

from abc import ABC, abstractmethod 
from unskript_utils import *
try:
     from envyaml import EnvYAML
except Exception as e:
     print("ERROR: Unable to find required yaml package to parse the config file")
     raise e


# This is the Base class, Abstract class that shall be used by all the other
# classes that are implemented. This class is implemented as a Singleton class
# which means, the Child that inherits this class, will have a single copy in
# memory. This saves Memory footprint! This class also implements a Logger
# that is being used by individual child class. This class generates
# unskript_ctl.log in the same directory, from where the unskript-ctl.sh is 
# called. 
class UnskriptFactory(ABC):
    _instance = None 
    log_file_name = os.path.join(os.path.expanduser('~'), 'unskript_ctl.log')
    
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls)
            if os.path.exists(os.path.dirname(cls.log_file_name)) is False:
                os.makedirs(os.path.dirname(cls.log_file_name))
            cls._instance.logger = cls._configure_logger()
        return cls._instance 
    

    @staticmethod
    def _configure_logger():
        logger = logging.getLogger('UnskriptCtlLogger')
        if not logger.handlers:
            logger.setLevel(logging.DEBUG)
            
            # Create a formatter for log messages
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            
            # Create a file handler and set its format
            file_handler = logging.FileHandler(UnskriptFactory.log_file_name)
            file_handler.setLevel(logging.DEBUG)  # Set file logging level
            file_handler.setFormatter(formatter)
            
            # Add the file handler to the logger
            logger.addHandler(file_handler)
            logger.propagate = False
        
        return logger
    
    def __init__(self):
        self.uglobals = UnskriptGlobals()
        self.update_credentials_to_uglobal()
        pass

    def update_credentials_to_uglobal(self):
        mapping = {} 
        home = os.path.expanduser('~')
        creds_json_files = []
        for dirpath, dirname, filenames in os.walk(home):
            if 'credential-save' in dirname:
                pattern = os.path.join(dirpath, dirname[-1]) + '/*.json'
                creds_json_files.extend(glob.glob(pattern, recursive=True))
                break
        self.creds_json_files = creds_json_files
        for creds_json_file in creds_json_files:
            with open(creds_json_file, 'r', encoding='utf-8') as f:
                c_data = json.load(f)
                if c_data.get('metadata').get('connectorData') == '{}':
                    continue 
                mapping[c_data.get('metadata').get('type')] = {"name": c_data.get('metadata').get('name'), 
                                                            "id": c_data.get('id')}
        self.uglobals['default_credentials'] = mapping

    def _banner(self, msg: str):
        print('\033[4m\x1B[1;20;42m' + msg + '\x1B[0m\033[0m')
    
    def _error(self, msg: str):
        print('\x1B[1;20;41m' + msg + '\x1B[0m')


# This class implements an Abstract class for All Checks
class ChecksFactory(UnskriptFactory):
    def __init__(self):
        super().__init__()
        self.logger.info(f'{self.__class__.__name__} instance initialized')
        self._config = ConfigParserFactory()
        pass 

    def run(self, **kwargs):
        pass 

# This class implements an Abstract class for Executing Script
class ScriptsFactory(UnskriptFactory):
    def __init__(self):
        super().__init__()
        self.logger.info(f'{self.__class__.__name__} instance initialized')
        self._config = ConfigParserFactory()
        pass

    def run(self, *args, **kwargs):
        pass

# This class implements an Abstract class for Notification that is used by Slack and Email
class NotificationFactory(UnskriptFactory):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.logger.info(f'{self.__class__.__name__} instance initialized')
        self._config = ConfigParserFactory()
        pass

    def notify(self, **kwargs):
        pass 

# This class implements the Database abstract class that is implemented by ZoDB and SQL
class DatabaseFactory(UnskriptFactory):
    def __init__(self):
        super().__init__()
        self.logger.info(f'{self.__class__.__name__} instance initialized')
        pass

    @abstractmethod
    def create(self, **kwargs):
        pass

    @abstractmethod
    def read(self, **kwargs):
        pass 

    @abstractmethod
    def update(self, **kwargs):
        pass

    @abstractmethod
    def delete(self, **kwargs):
        pass 


# This class implements the Config parser that is being used by the UnskriptFactory 
# This class looks the the unskript_ctl_config.yaml in known directories, parses it
# and saves it as a local class specific variable. 
class ConfigParserFactory(UnskriptFactory):
    CONFIG_FILE_NAME = "unskript_ctl_config.yaml"
    DEFAULT_DIRS = ["/etc/unskript", "/opt/unskript", "/tmp", "./config", "./"]
    
    def __init__(self):
        super().__init__()
        self.logger.info(f'{self.__class__.__name__} instance initialized')
        self.yaml_content = self.load_config_file()
        if not self.yaml_content:
            raise FileNotFoundError(f"{self.CONFIG_FILE_NAME} not found or empty!")

    def load_config_file(self):
        for directory in self.DEFAULT_DIRS:
            conf_file = os.path.join(directory, self.CONFIG_FILE_NAME)
            if os.path.exists(conf_file):
                yaml_content = EnvYAML(conf_file, strict=False)
                return yaml_content
        return {}  # Return an empty dictionary if file not found or empty

    def _get(self, key, sub_key=None):
        if self.yaml_content:
            value = self.yaml_content.get(key)
            if sub_key:
                value = value.get(sub_key) if value else None
            return value if value is not None else {}
        return {}
    
    def get_schedule(self):
        return self._get('scheduler')[0]

    def get_jobs(self):
        return self._get('jobs')[0]

    def get_checks(self):
        return self.get_jobs().get('checks')
    

    def get_notification(self):
        return self._get('notification')

    def get_credentials(self):
        # FIXME: Not implemented 
        pass 

    def get_global(self):
        return self._get('global')
    
    def get_checks_params(self):
        return self._get('checks', 'arguments')