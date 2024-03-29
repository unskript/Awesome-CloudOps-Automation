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
from datetime import datetime
from unskript_utils import *
try:
     from envyaml import EnvYAML
except Exception as e:
     print("ERROR: Unable to find required yaml package to parse the config file")
     raise e


# This is a custom logger class to implement the following logic
# Any logger.info(...) & logger.error(...) message should be shown on the console
# Any logger.debug(...),  logger.warning(...)
# Message should be dumped to a log file that can be used to debug
# any issue.
class UctlLogger(logging.Logger):
    def __init__(self, name, level=logging.NOTSET):
        super().__init__(name, level)

        if not self.handlers:
            # Create a custom formatter
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

            # Create a console handler for INFO level
            console_handler = logging.StreamHandler()
            console_handler.setLevel(logging.INFO)
            console_handler.setFormatter(formatter)
            self.addHandler(console_handler)

            # Create File handler to dump all other level
            self.log_file_name = os.path.join(os.path.expanduser('~'), 'unskript_ctl.log')
            file_handler = logging.FileHandler(self.log_file_name)
            file_handler.setLevel(logging.DEBUG)
            file_handler.setFormatter(formatter)
            self.addHandler(file_handler)

            # Set Default logger level
            self.setLevel(logging.DEBUG)
            self.propagate = False

    def info(self, msg, *args, **kwargs):
        # Pass up the Info message to show the log to console
        super().info(msg, *args, **kwargs)

    def debug(self, msg, *args, **kwargs):
        # Dump to logfile
        self.dump_to_file(msg)

    def warning(self, msg, *args, **kwargs):
        # Warning to logfile
        self.dump_to_file(msg)

    def error(self, msg, *args, **kwargs):
        # Error to logfile
        self.dump_to_file(msg)
        super().info(msg, *args, **kwargs)

    def critical(self, msg, *args, **kwargs):
        # Critical msg to logfile and to console
        self.dump_to_file(msg)
        super().info(msg, *args, **kwargs)

    def dump_to_file(self, msg):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(self.log_file_name, 'a') as f:
            f.write(timestamp + ' : ' + str(msg) + '\n')

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
        logger = UctlLogger('UnskriptCtlLogger')
        # if not logger.handlers:
        #     logger.setLevel(logging.DEBUG)

        #     # Create a formatter for log messages
        #     formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

        #     # Create a file handler and set its format
        #     file_handler = logging.FileHandler(UnskriptFactory.log_file_name)
        #     file_handler.setLevel(logging.DEBUG)  # Set file logging level
        #     file_handler.setFormatter(formatter)

        #     # Add the file handler to the logger
        #     logger.addHandler(file_handler)
        #     logger.propagate = False

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
        c_data = {}
        for creds_json_file in creds_json_files:

            if is_creds_json_file_valid(creds_file=creds_json_file) is False:
                raise ValueError(f"Given Credential file {creds_json_file} is corrupt!")

            with open(creds_json_file, 'r', encoding='utf-8') as f:
                try:
                    c_data = json.load(f)
                except Exception as e:
                    # If creds file is corrupt, raise exception and bail out
                    self.logger.error(f"Exception Occurred while parsing credential file {creds_json_file}: {str(e)}")
                    raise ValueError(e)
                finally:
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
        self.logger.debug(f'{self.__class__.__name__} instance initialized')
        self._config = ConfigParserFactory()
        pass

    def run(self, **kwargs):
        pass

# This class implements an Abstract class for Executing Script
class ScriptsFactory(UnskriptFactory):
    def __init__(self):
        super().__init__()
        self.logger.debug(f'{self.__class__.__name__} instance initialized')
        self._config = ConfigParserFactory()
        pass

    def run(self, *args, **kwargs):
        pass

# This class implements an Abstract class for Notification that is used by Slack and Email
class NotificationFactory(UnskriptFactory):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.logger.debug(f'{self.__class__.__name__} instance initialized')
        self._config = ConfigParserFactory()
        pass

    def notify(self, **kwargs):
        pass

# This class implements the Database abstract class that is implemented by ZoDB and SQL
class DatabaseFactory(UnskriptFactory):
    def __init__(self):
        super().__init__()
        self.logger.debug(f'{self.__class__.__name__} instance initialized')
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
        self.logger.debug(f'{self.__class__.__name__} instance initialized')
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

    def get_info_action_params(self):
        return self._get('info', 'arguments')

    def get_info(self):
        return self.get_jobs().get('info',{})

    def get_email_fmt(self):
        notification_config = self.get_notification()
        email_config = notification_config.get('Email', {})
        email_fmt = email_config.get('email_fmt', {})
        return email_fmt

    def get_checks_section(self):
        # Get the checks_section from email_fmt
        checks_section = self.get_email_fmt().get('checks_section', {})
        return checks_section.get('priority', {})

    def get_info_section(self):
        # Get the info_section from email_fmt
        return self.get_email_fmt().get('info_section', [])

    def get_checks_priority(self)->dict:
        # This function reads the priority part of the config and converts it
        # into a dict with check_name as the key and priority as the value.
        # If the check is not found in the dict, its assigned priority P2.

        email_fmt = self.get_email_fmt()
        checks_section = email_fmt.get('checks_section', {})
        priority_config = checks_section.get('priority', {})

        checks_priority = {}

        # Check if the 'priority' configuration is properly set; if not, return None
        if not priority_config:
            return None

        # Explicitly fetch and map checks for each priority level using the constants
        for priority_level in [CHECK_PRIORITY_P0, CHECK_PRIORITY_P1, CHECK_PRIORITY_P2]:
            priority_checks = priority_config.get(priority_level, [])
            if priority_checks:
                for check_name in priority_checks:
                    checks_priority[check_name] = priority_level

        return checks_priority

