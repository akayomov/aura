from .providers.domashkanet import DomashkaISPParser
from .providers.crystal import CrystalISPParser
from .providers.nashnet import NashnetISPParser

from .features.redirect import RedirectChecker

from ..tools.router_access import RouterAccess
from ..tools.file_manager import FileManager
from ..tools.logger import Logger

import time
import os


class StatusCollector:
    def __init__(self, output=False):
        self.__logger = Logger("StatusCollector", output)
        self.__top = RouterAccess(output)
        self.__file = FileManager(output)
        self.__output = output
        self.__logger.log('Initialized', self)

    def collect(self, sections: list, current_time: float) -> dict:
        self.__logger.log('Status collect at \'', current_time, '\' for:', sections)
        self.__top.clear_cache()  # Clearing to get current response
        status = {
            "info": self.__info(current_time),
        }
        available_sections = {
            "system": self.__system,
            "internet": self.__internet,
            "provider": self.__provider,
            "tunnels": self.__tunnels,
            "devices": self.__devices,
            "features": self.__features,
        }
        for section in sections:
            status[section] = available_sections.get(section, lambda: {"unknown": True})()
        # noinspection PyTypeChecker
        status['info']['duration'] = str(round(time.time() - current_time, 2))
        self.__top.clear_cache()  # Clearing having clear state between statuses
        return status

    def __info(self, start_time) -> object:
        self.__logger.log('Collecting info')
        return {
            'node': self.__top.cli('uname -n'),
            'time': time.strftime("%Y-%m-%dT%H:%M:%S.000Z", time.localtime(start_time)),
        }

    def __system(self) -> object:
        self.__logger.log('Collecting system')
        result = {}

        status = self.__top.rci("/show/system")
        if status is not None:
            result['cpu'] = status['cpuload']
            result['ram'] = int(100 * int(status['memory'].split("/")[0]) / int(status['memory'].split("/")[1]))
            result['uptime'] = int(status['uptime'])

            ports = list(map(lambda l: " ".join(l.split()).split(" "), self.__top.cli("netstat -tulpn").split("\n")))
            while ports[0][0] != "Proto":
                ports.pop(0)
            ports.pop(0)
            ports = list(filter(lambda l: l[5] == "LISTEN", ports))
            ports = list(filter(lambda l: l[6] != "-", ports))

            result['ssh'] = len(list(filter(lambda l: l[6].split("/")[1] == "dropbear", ports))) > 0
            result['ftp'] = len(list(filter(lambda l: l[6].split("/")[1] == "pure-ftpd (SERV", ports))) > 0

            fstats = list(map(lambda line: " ".join(line.split()).split(" "), self.__top.cli("df -h").split("\n")))
            while fstats[0][0] != "Filesystem":
                fstats.pop(0)
            fstats.pop(0)

            hdd_line = list(filter(lambda l: l[5] == "/opt", fstats))
            result['hdd'] = int(hdd_line[0][4].split("%")[0]) if len(hdd_line) == 1 else 0

            tmp_line = list(filter(lambda l: l[5] == "/tmp", fstats))
            result['tmp'] = int(tmp_line[0][4].split("%")[0]) if len(tmp_line) == 1 else 0

            if len(tmp_line) == 1:
                backup_fs = "/dev/sda2" if hdd_line[0][0] == "/dev/sda1" else "/dev/sda1"
                bkp = list(filter(lambda line: line[0] == backup_fs, fstats))
                if len(bkp) == 1:
                    if os.listdir(bkp[0][5]) == ["install"]:
                        result['bkp'] = True if os.listdir(bkp[0][5] + "/install") == [
                            "core.firmware.tar.gz"] else False
                    else:
                        result['bkp'] = False
                else:
                    result['bkp'] = False
            else:
                result['bkp'] = False
        return result

    def __internet(self) -> object:
        self.__logger.log('Collecting internet')
        result = {}
        internet_status = self.__top.rci("/show/internet/status")
        interface_status = self.__top.rci("/show/interface/ISP")
        if internet_status is not None and interface_status is not None:
            result["ip"] = interface_status["address"]
            result["uptime"] = interface_status["uptime"]
            result["link"] = interface_status["link"] == "up"
            result["gateway"] = internet_status["gateway-accessible"]
            result["dns"] = internet_status["dns-accessible"]
            result["access"] = internet_status["internet"]
        return result

    def __provider(self) -> object:
        self.__logger.log('Collecting provider')
        provider = self.__file.get_config('provider.info')
        if provider is not None:
            case = {
                "domashkanet": DomashkaISPParser,
                "crystal": CrystalISPParser,
                "nashnet": NashnetISPParser,
            }
            current = case.get(provider['name'], lambda username, password: None)
            result = current(provider['login'], provider['password'], self.__output)
            if result is None:
                return {}
            else:
                return result.data
        else:
            return {}

    def __tunnels(self) -> list:
        self.__logger.log('Collecting tunnels')
        result = []

        tun_infos = self.__top.rci('/show/rc/interface/Wireguard0/wireguard/peer')
        tun_statuses = self.__top.rci('/show/interface/Wireguard0/wireguard/peer')

        for status in tun_statuses:
            result.append({
                "type": "wireguard",
                "name": list(filter(lambda t: t['key'] == status['public-key'], tun_infos))[0]['comment'],
                "online": status["online"],
            })
        return result

    def __devices(self) -> list:
        self.__logger.log('Collecting devices')
        result = []

        devices = self.__top.rci('/show/ip/hotspot/host')
        for device in devices:
            if device['active']:
                dev = {
                    'ip': device['ip'],
                    'mac': device['mac'],
                    'hostname': device['hostname'],
                }
                if 'speed' in device:
                    dev['connection'] = {
                        'type': 'wired',
                        'speed': int(device['speed']),
                    }
                elif 'mws' in device:
                    dev['connection'] = {
                        'type': 'wireless',
                        'mode': device['mws']['mode'],
                        'ht': device['mws']['ht'],
                        'gi': device['mws']['gi'],
                        'rssi': device['mws']['rssi'],
                    }
                else:
                    try:
                        dev['connection'] = {
                            'type': 'wireless',
                            'mode': device['mode'],
                            'ht': device['ht'],
                            'gi': device['gi'],
                            'rssi': device['rssi'],
                        }
                    except KeyError:
                        dev['connection'] = {
                            'type': 'unknown'
                        }
                result.append(dev)
        return result

    def __features(self) -> object:
        self.__logger.log('Collecting features')
        configuration = self.__file.get_config('features.config')
        if configuration is not None:
            result = {}
            case = {
                'redirect': RedirectChecker,
            }

            for config in configuration:
                checker = case.get(config['type'], lambda c, o: None)
                check = checker(config, self.__output)
                if check is None:
                    result[config['name']] = ''
                else:
                    result[config['name']] = check.data
            return result
        else:
            return {}
