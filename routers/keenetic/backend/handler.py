from http.server import HTTPServer, SimpleHTTPRequestHandler
from typing import Any

from ..tools.logger import Logger
from threading import Thread


class RequestsHandler:
    __logger = None
    __server = None
    __loop = None
    __get_handlers = None
    __post_handlers = None
    __initialized = None

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'instance'):
            cls.instance = super(RequestsHandler, cls).__new__(cls)
        return cls.instance

    def __init__(self, output=False):
        if self.__logger is None: self.__logger = Logger("RequestsHandler", output)
        if self.__get_handlers is None: self.__get_handlers = {}
        if self.__post_handlers is None: self.__post_handlers = {}
        if self.__initialized is None:
            self.__initialized = True
            self.__logger.log("Initialized", self)

    def start_loop(self):
        if self.__server is None: self.__server = HTTPServer(('0.0.0.0', 8000), SubRH)
        if self.__loop is None:
            self.__loop = Thread(target=self.__server.serve_forever)
            self.__loop.daemon = True
            self.__loop.start()
        self.__logger.log("Loop Started")

    def add(self, method, url, handler):
        self.__logger.log("Add request handler to:", method, url)
        {
            "GET": self.__get_handlers,
            "POST": self.__post_handlers,
        }.get(method.upper(), {})[url] = handler

    def solve_request(self, method: str, handler):
        self.__logger.log("Solving:", method, handler.path)
        handlers = {
            "GET": self.__get_handlers,
            "POST": self.__post_handlers,
        }.get(method.upper(), {})
        if handler.path in handlers:
            handlers[handler.path](handler)
        else:
            handler.send_response(404)
            handler.end_headers()
            error_body = bytes("Can't resolve execution for path: "+method.upper()+" "+handler.path, encoding='utf-8')
            handler.wfile.write(error_body)


class SubRH(SimpleHTTPRequestHandler):
    def do_GET(self) -> None:
        self.server_version = "Custom HTTP Handler"
        self.sys_version = "{AURA}"
        RequestsHandler().solve_request("GET", self)

    def do_POST(self) -> None:
        self.server_version = "Custom HTTP Handler"
        self.sys_version = "{AURA}"
        RequestsHandler().solve_request("POST", self)

    def do_PUT(self) -> None:
        self.server_version = "Custom HTTP Handler"
        self.sys_version = "{AURA}"
        RequestsHandler().solve_request("PUT", self)

    def do_PATCH(self) -> None:
        self.server_version = "Custom HTTP Handler"
        self.sys_version = "{AURA}"
        RequestsHandler().solve_request("PATCH", self)

    def do_DELETE(self) -> None:
        self.server_version = "Custom HTTP Handler"
        self.sys_version = "{AURA}"
        RequestsHandler().solve_request("DELETE", self)

    def log_message(self, format: str, *args: Any) -> None:
        pass
