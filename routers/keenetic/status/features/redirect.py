from ...tools.logger import Logger
from ...tools.router_access import RouterAccess


class RedirectChecker:
    def __init__(self, config, output):
        self.__logger = Logger("RedirectChecker", output)
        self.__logger.log("Checking redirect feature", config)
        self.__top = RouterAccess(output)
        self.config = config
        super(RedirectChecker, self).__init__()

        status = True

        try:
            if self.config['routing']['type'] == 'static':
                status = self.check_routing(self.config['routing']['list']) if status else False
            if self.config['vpn']['type'] == 'wireguard':
                status = self.check_wireguard(self.config['vpn']) if status else False
        except KeyError as e:
            self.__logger.warnerr(e)

        if status:
            self.data = 'on' if self.config['status'] else 'off'
        else:
            self.data = 'error'

    def check_routing(self, requirements) -> bool:
        table = self.__top.rci('/show/ip/route')
        result = True

        for requirement in requirements:
            if result:
                filtered = table
                for field in requirement:
                    filtered = list(filter(lambda i: i[field] == requirement[field], filtered))
                if len(filtered) == 0:
                    result = not self.config['status']
        return result

    def check_wireguard(self, config) -> bool:
        peers = self.__top.rci('/show/rc/interface/Wireguard0/wireguard/peer')
        peer = list(filter(lambda p: p['comment'] == config['peer'], peers))[0]
        result = True

        for requirement in config['subnets']:
            if result:
                occurred = False
                for subnet in peer['allow-ips']:
                    if subnet == requirement:
                        occurred = True
                result = False if occurred is not self.config['status'] else True
        return result
