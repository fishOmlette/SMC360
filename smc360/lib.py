"""
Core library for SMC360 - Social Media Data Connector.

This module provides the main SocialMediaConnector class for extracting,
parsing, and managing social media data.
"""

import os
import re
import json
import yaml
import logging
from halo import Halo
from datetime import datetime
from dotenv import load_dotenv
from importlib import import_module
from typing import Any, Dict, Optional


class SocialMediaConnector:
    """
    A class for parsing social media data and uploading it to an object storage and database.

    Attributes:
    ----
        - `config (dict)`: A dictionary containing the configuration information for the parser.

    Methods:
    ----
        - `__load_env_var()`: sets environment variables.
        - `run()`: Parses social media data and uploads it to an object storage and database.
    """

    def __init__(self, config_path):
        """
        Initializes a SocialMediaParser object with the given configuration.
        """

        # Set timestamp and logging
        curr_dir_path = os.path.dirname(config_path)
        log_path = os.path.join(curr_dir_path, "log")
        timestamp = os.environ['timestamp'] = str(datetime.now())
        if not os.path.exists(log_path):
            os.makedirs(log_path)
        logging.basicConfig(
            filename=os.path.join(log_path, timestamp.replace(':', '-')+".log"), 
            level=logging.INFO, 
            format='%(asctime)s - %(levelname)s - %(message)s'
            )
        self.logger = logging.getLogger(__name__)

        # Load configuration file and set environment variables
        with open(config_path, 'r') as f:
            self.config = yaml.safe_load(f)
        load_dotenv(dotenv_path=os.path.join(curr_dir_path, ".env"))
        self.__load_env_var(self.config)

    def __load_env_var(self, block):
        """
        Sets environment variables in the given configuration.

        Args:
        ----
            - `config (dict)`: A dictionary containing the configuration information.
            - `prefix (str)`: The prefix to use when setting environment variables. Defaults to 'config'.
        """

        for key, value in block.items():
            if isinstance(value, str) and bool(re.match(r'^\$\w+$', value)):
                env_var_name = value[1:]
                env_var_value = os.getenv(env_var_name)
                block[key] = env_var_value
            elif isinstance(value, dict):
                self.__load_env_var(block[key])
            elif isinstance(value, list):
                [self.__load_env_var(item) for item in value]

    def run(self):
        """
        Parses social media data and uploads it to an object storage and database.
        """

        # Load environment variables
        for service in ['platform', 'database', 'object_storage']:
            if service not in self.config:
                self.logger.critical(f"{service} not found in configuration.")
                exit(1)
            os.environ[service] = json.dumps(self.config[service])

        # Import necessary modules
        try:
            platform = import_module(f'smc360.services.platform.{self.config["platform"]["service_name"]}')
            object_storage = import_module(f'smc360.services.object_storage.{self.config["object_storage"]["service_name"]}')
            database = import_module(f'smc360.services.database.{self.config["database"]["service_name"]}')
        except ImportError as e:
            module_name = str(e).split("'")[1]
            self.logger.critical(f"module {module_name} is not supported.")
            exit(1)

        # Verify credentials
        for module in [platform, object_storage, database]:
            none_attrs = [attr_name for attr_name, attr_value in vars(module.credentials()).items() if attr_value is None]
            if none_attrs:
                self.logger.critical(f"{none_attrs} in {module.__name__} are None")
                exit(1)

        self.logger.info('Credentials validated')

        # Load additional configuration files from bucket
        file_store = object_storage.connection()
        try:
            input_configuration = yaml.safe_load(file_store.read_file(f"{self.config['platform']['service_name']}/input_configuration.yaml"))
            models_configuration = yaml.safe_load(file_store.read_file(f"{self.config['platform']['service_name']}/models_configuration.yaml"))
            self.logger.info(f"Configuration files extracted from {self.config['object_storage']['service_name']}")
        except Exception as e:
            self.logger.critical(str(e))
            exit(1)

        # Upload response to bucket
        spinner = Halo(text=f"Uploading {self.config['platform']['service_name']} data to {self.config['object_storage']['service_name']}: ", spinner='dots', placement='right', color='white')
        spinner.start()
        start_time = datetime.now()
        upload_response = platform.load_to_object_storage(object_storage)
        for input_key, input_value in input_configuration.items():
            if isinstance(input_value, dict):
                try:
                    method = getattr(upload_response, input_key)
                except Exception as e:
                    self.logger.error(str(e))
                    continue
                if callable(method):
                    method(input_value)
                self.logger.info(f"{input_key} extracted")
            else:
                setattr(upload_response, input_key, input_value)
                self.logger.info(f"{input_key} set to {input_value}")
        self.logger.info(f"Uploaded {self.config['platform']['service_name']} data to {self.config['object_storage']['service_name']}")
        elapsed_time, spinner.placement, spinner.text_color = (datetime.now() - start_time).total_seconds(), 'left', 'green'
        spinner.succeed(f"Uploaded {self.config['platform']['service_name']} data to {self.config['object_storage']['service_name']} [elapsed time: {elapsed_time:.2f}s]")

        # Parse response & build models
        spinner = Halo(text=f"Uploading {self.config['platform']['service_name']} data to {self.config['database']['service_name']}: ", spinner='dots', placement='right', color='white')
        spinner.start()
        start_time = datetime.now()
        parse_response = platform.load_to_database(database, object_storage)
        for model_key, model_value in models_configuration.items():
            if isinstance(model_value, dict):
                try:
                    method = getattr(parse_response, model_key)
                except Exception as e:
                    self.logger.error(str(e))
                    continue
                if callable(method):
                    method(model_value, model_key)
                self.logger.info(f"{model_key} model built")
            else:
                setattr(parse_response, model_key, model_value)
                self.logger.info(f"{model_key} set to {model_value}")
        self.logger.info(f"Uploaded {self.config['platform']['service_name']} data to {self.config['database']['service_name']}")
        elapsed_time, spinner.placement, spinner.text_color = (datetime.now() - start_time).total_seconds(), 'left', 'green'
        spinner.succeed(f"Uploaded {self.config['platform']['service_name']} data to {self.config['database']['service_name']} [elapsed time: {elapsed_time:.2f}s]")