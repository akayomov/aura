from requests.exceptions import HTTPError
from subprocess import getoutput
from .logger import Logger
import requests
import time


class RouterAccess:
    __logger = None
    __rci_cache = None
    __cli_cache = None

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'instance'):
            cls.instance = super(RouterAccess, cls).__new__(cls)
        return cls.instance

    def __init__(self, output=False):
        if self.__logger is None: self.__logger = Logger("RouterAccess", output)
        if self.__rci_cache is None: self.__rci_cache = {}
        if self.__cli_cache is None: self.__cli_cache = {}
        self.__logger.log('Initialized', self)

    def clear_cache(self):
        self.__rci_cache = {}
        self.__cli_cache = {}

    def rci(self, url: str):
        self.__logger.log('Request to RCI:', url)
        if url in self.__rci_cache:
            self.__logger.log('  found in cache')
            return self.__rci_cache[url]
        else:
            success = False
            response = None
            for iteration in range(1, 6):
                self.__logger.log('  attempting:', iteration)
                try:
                    time.sleep(1)  # Sleep to get some silence between requests
                    response = requests.get("http://localhost:79/rci" + url).json()
                    self.__rci_cache[url] = response
                    success = True
                    break
                except (ConnectionError, HTTPError, IOError) as e:
                    self.__logger.warnerr(e)
            if not success:
                raise Exception("Continuous error happened during request to router")
            return response

    def cli(self, command: str):
        self.__logger.log('Request to CLI:', command)
        if command in self.__cli_cache:
            self.__logger.log('  found in cache')
            return self.__cli_cache[command]
        else:
            success = False
            response = None
            for iteration in range(1, 6):
                self.__logger.log('  attempting:', iteration)
                try:
                    time.sleep(1)  # Sleep to get some silence between requests
                    response = getoutput(command)
                    self.__rci_cache[command] = response
                    success = True
                    break
                except (IOError, Exception) as e:
                    self.__logger.warnerr(e)
            if not success:
                raise Exception("Continuous error happened during request to router")
            return response
