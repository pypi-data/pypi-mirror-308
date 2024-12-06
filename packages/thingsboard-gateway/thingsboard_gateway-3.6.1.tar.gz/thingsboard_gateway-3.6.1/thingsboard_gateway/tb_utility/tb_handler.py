#     Copyright 2024. ThingsBoard
#
#     Licensed under the Apache License, Version 2.0 (the "License");
#     you may not use this file except in compliance with the License.
#     You may obtain a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#     Unless required by applicable law or agreed to in writing, software
#     distributed under the License is distributed on an "AS IS" BASIS,
#     WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#     See the License for the specific language governing permissions and
#     limitations under the License.

import logging
import logging.handlers
import os
import threading
from os import environ
from pathlib import Path
from queue import Queue, Empty
from sys import stdout
from time import time, sleep

from thingsboard_gateway.tb_utility.tb_logger import TbLogger, init_logger
from thingsboard_gateway.tb_utility.tb_utility import TBUtility

logging.setLoggerClass(TbLogger)

class TBLoggerHandler(logging.Handler):
    LOGGER_NAME_TO_ATTRIBUTE_NAME = {
        'service': 'SERVICE_LOGS',
        'extension': 'EXTENSION_LOGS',
        'tb_connection': 'CONNECTION_LOGS',
        'storage': 'STORAGE_LOGS',
    }

    def __init__(self, gateway):
        logging.setLoggerClass(TbLogger)
        self.current_log_level = 'INFO'
        super().__init__(logging.getLevelName(self.current_log_level))
        self.setLevel(logging.getLevelName('DEBUG'))
        self.__gateway = gateway
        self.activated = False

        self._max_message_count_batch = 20
        self._logs_queue = Queue(1000)

        self._send_logs_thread = threading.Thread(target=self._send_logs, name='Logs Sending Thread', daemon=True)

        self.setFormatter(logging.Formatter('%(asctime)s,%(msecs)03d - |%(levelname)s|<%(threadName)s> [%(filename)s] - %(module)s %(funcName)s - %(lineno)d - %(message)s'))
        self.loggers = {'service': None,
                        'extension': None,
                        'tb_connection': None,
                        'storage': None
                        }
        for logger in self.loggers:
            log = logging.getLogger(logger)
            log.addHandler(self.__gateway.main_handler)
            log.debug("Added remote handler to log %s", logger)
            self.loggers[logger] = log

    def get_logger(self, name):
        return self.loggers.get(name)

    def add_logger(self, name):
        log = logging.getLogger(name)
        if hasattr(self.__gateway, 'main_handler') and self.__gateway.main_handler not in log.handlers:
            log.addHandler(self.__gateway.main_handler)
            log.debug("Added main handler to log %s", name)
        self.loggers[name] = log

    def _send_logs(self):
        while self.activated and not self.__gateway.stopped:
            if not self._logs_queue.empty():
                logs_for_sending_list = []

                count = 1
                while count <= self._max_message_count_batch:
                    try:
                        if self.__gateway.tb_client is None or not self.__gateway.tb_client.is_connected():
                            sleep(1)
                            continue
                        log_msg = self._logs_queue.get(block=False)

                        logs_msg_size = TBUtility.get_data_size(log_msg)
                        if logs_msg_size > self.__gateway.get_max_payload_size_bytes():
                            print(f'Too big LOG message size to send ({logs_msg_size}). Skipping...')
                            continue

                        if TBUtility.get_data_size(logs_for_sending_list) + logs_msg_size > self.__gateway.get_max_payload_size_bytes():
                            self.__gateway.send_telemetry(logs_for_sending_list)
                            logs_for_sending_list = [log_msg]
                        else:
                            logs_for_sending_list.append(log_msg)

                        count += 1
                    except Empty:
                        break

                if logs_for_sending_list:
                    self.__gateway.send_telemetry(logs_for_sending_list)

            sleep(1)

    def activate(self, log_level=None):
        self.setLevel(logging.getLevelName(log_level or 'INFO'))
        self.current_log_level = log_level
        self.activated = True

        self._send_logs_thread = threading.Thread(target=self._send_logs, name='Logs Sending Thread', daemon=True)
        self._send_logs_thread.start()

    def handle(self, record):
        if self.activated and not self.__gateway.stopped:
            logger = self.loggers.get(record.name)
            if logger and hasattr(logger, 'connector_name'):
                name = logger.connector_name

                if name:
                    record = self.formatter.format(record)
                    try:
                        telemetry_key = self.LOGGER_NAME_TO_ATTRIBUTE_NAME[name]
                    except KeyError:
                        telemetry_key = name + '_LOGS'

                    log_msg = {'ts': int(time() * 1000), 'values': {telemetry_key: record}}

                    if telemetry_key in self.LOGGER_NAME_TO_ATTRIBUTE_NAME.values():
                        log_msg['values']['LOGS'] = record

                    self._logs_queue.put(log_msg)

    def deactivate(self):
        self.activated = False
        try:
            self._send_logs_thread.join()
        except Exception as e:
            log = TbLogger('service')
            log.debug("Exception while joining logs sending thread.", exc_info=e)

    @staticmethod
    def set_default_handler():
        logger_names = [
            'service',
            'storage',
            'extension',
            'tb_connection'
            ]
        logging.setLoggerClass(TbLogger)
        for logger_name in logger_names:
            logger = logging.getLogger(logger_name)
            handler = logging.StreamHandler(stdout)
            handler.setFormatter(logging.Formatter('[STREAM ONLY] %(asctime)s - %(levelname)s - [%(filename)s] - %(module)s - %(lineno)d - %(message)s'))
            logger.addHandler(handler)


class TimedRotatingFileHandler(logging.handlers.TimedRotatingFileHandler):
    def __init__(self, filename, when='h', interval=1, backupCount=0,
                 encoding=None, delay=False, utc=False):
        config_path = environ.get('TB_GW_LOGS_PATH')
        if config_path:
            filename = config_path + os.pathsep + filename.split(os.pathsep)[-1]

        if not Path(filename).exists():
            with open(filename, 'w'):
                pass

        super().__init__(filename, when=when, interval=interval, backupCount=backupCount,
                         encoding=encoding, delay=delay, utc=utc)
