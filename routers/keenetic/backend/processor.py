from ..tools.logger import Logger
from .handler import RequestsHandler
import json
import os


class RequestsProcessor:
    __logger = None
    __current_status = {}

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'instance'):
            cls.instance = super(RequestsProcessor, cls).__new__(cls)
        return cls.instance

    def __init__(self, output=False):
        self.__logger = Logger("RequestsProcessor", output)
        handler = RequestsHandler()
        handler.add("GET", '/config/status', self.__status)
        handler.add("GET", '/config/devices', self.__known_devices)
        handler.add("GET", '/config/routers', self.__routers_near)
        self.__logger.log('initialized')

    def update_status(self, status):
        for block in status:
            self.__current_status[block] = status[block]

    @staticmethod
    def __headers(intent, mime='application/json', status=200):
        intent.send_response(status)
        intent.send_header('Content-Type', mime)
        intent.end_headers()

    def __status(self, intent):
        self.__logger.log('__status')
        self.__headers(intent)
        intent.wfile.write(bytes(json.dumps(self.__current_status), encoding='utf-8'))

    def __known_devices(self, intent):
        self.__logger.log('__known_devices')
        path = os.path.abspath(os.path.join('/', 'storage', 'known.devices'))
        if os.path.exists(path):
            self.__headers(intent, status=200)
            intent.wfile.write(open(path, 'rb').read())
        else:
            self.__headers(intent, status=500)
            intent.wfile.write(bytes('[]', encoding='utf-8'))

    def __routers_near(self, intent):
        self.__logger.log('__routers_near')
        path = os.path.abspath(os.path.join('/', 'storage', 'routers.near'))
        if os.path.exists(path):
            self.__headers(intent, status=200)
            intent.wfile.write(open(path, 'rb').read())
        else:
            self.__headers(intent, status=500)
            intent.wfile.write(bytes('[]', encoding='utf-8'))
