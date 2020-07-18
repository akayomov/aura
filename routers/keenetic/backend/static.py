from ..tools.logger import Logger
from .handler import RequestsHandler
import os


class StaticFilesHandler:
    def __init__(self, output):
        self.__logger = Logger("StaticFilesHandler", output)
        handler = RequestsHandler()
        handler.add("GET", '/', self.__index)
        handler.add("GET", '/favicon.ico', self.__favicon)
        self.__logger.log('initialized')

    @staticmethod
    def __headers(mime, intent):
        intent.send_response(200)
        intent.send_header('Content-Type', mime)
        intent.end_headers()

    def __index(self, intent):
        self.__logger.log('__index')
        self.__headers('text/html', intent)
        path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'frontend', 'build', 'index.html'))
        intent.wfile.write(open(path, 'rb').read())

    def __favicon(self, intent):
        self.__logger.log('__favicon')
        self.__headers('image/x-icon', intent)
        path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'frontend', 'resources', 'favicon.ico'))
        intent.wfile.write(open(path, 'rb').read())
