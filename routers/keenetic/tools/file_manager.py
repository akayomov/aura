from .logger import Logger
import json
import time
import os


class FileManager:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not FileManager._instance:
            FileManager._instance = super(FileManager, cls).__new__(cls)
        return FileManager._instance

    def __init__(self, output):
        self.__logger = Logger("FileManager", output)
        self.__cache = {}
        self.__logger.log('Initialized')

    def get_config(self, file: str) -> (dict, list):
        path = os.path.abspath(os.path.join('/storage', file))
        self.__logger.log('Getting config file:', path)
        if os.path.exists(path) and os.path.isfile(path):
            modified = os.path.getmtime(path)
            if path in self.__cache and self.__cache[path][0] is modified:
                self.__logger.log('  returning cache, modified:', time.strftime("%Y-%m-%d at %H:%M:%S"))
                return self.__cache[path][1]
            else:
                self.__logger.log('  cache not found, reading from system')
                result = None
                err = None
                for iteration in range(1, 6):
                    self.__logger.log('    reading attempt:', iteration)
                    try:
                        result = json.loads(open(path, 'r', errors='strict').read())
                        err = None
                        break
                    except (IOError, ValueError) as e:
                        self.__logger.warnerr(e)
                if err is not None:
                    raise err
                return result
        else:
            self.__logger.log('  there is no such file...')
            return None

    def put_config(self, file: str, data: object):
        path = os.path.abspath(os.path.join('/storage', file))
        self.__logger.log('Putting config file:', path)
        err = None
        for iteration in range(1, 6):
            self.__logger.log('  storing attempt:', iteration)
            try:
                open(path, 'w', errors='strict').write(json.dumps(data, indent=4))
                err = None
                break
            except (IOError, ValueError) as e:
                self.__logger.warnerr(e)
        if err is not None:
            raise err
        modified = os.path.getmtime(path)
        self.__cache[path] = [modified, data]

    def get_status(self, timestamp: float, to_timestamp: float = None) -> object:
        self.__logger.log('Getting status for:', timestamp, 'to:', to_timestamp)
        # to_timestamp: None - means single status for specific stamp, -1 means list of all existing from timestamp
        result = {}
        dir_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data'))
        low_file_num = int(str(int(timestamp))[:-5])
        low_marker_num = int(str(int(timestamp))[-5:])
        for file in os.listdir(dir_path):
            self.__logger.log('  checking directory item:', file)
            file_path = os.path.abspath(os.path.join(dir_path, file))
            
            if os.path.isfile(file_path) and int(file.split('.')[0]) >= low_file_num and ((to_timestamp == -1) or
                    (to_timestamp is None and int(file.split('.')[0]) < low_file_num + 1) or
                    (int(file.split('.')[0]) < int(str(int(to_timestamp))[-5:]))):
                self.__logger.log('  matching the terms')
                for line in open(file_path, 'r', errors='strict'):
                    splitter = line.split("|")
                    self.__logger.log('    reading line:', splitter[0])
                    if (int(splitter[0]) >= low_marker_num) and ((to_timestamp == -1) or
                            (to_timestamp is None and int(splitter[0]) < low_file_num + 1) or
                            (int(splitter[0]) < int(str(int(to_timestamp))[-5:]))):
                        status = "|".join("\n".join(json.dumps(splitter[1]).split("$newline$")).split("$marker$"))
                        self.__logger.log('    matching the terms')
                        if to_timestamp is None:
                            result = status
                            break
                        else:
                            place = time.localtime(float(file.split('.')[0]+splitter[0]))
                            if str(place.tm_year) not in result:
                                result[str(place.tm_year)] = {}
                            if str(place.tm_mon) not in result[str(place.tm_year)]:
                                result[str(place.tm_year)][str(place.tm_mon)] = {}
                            if str(place.tm_mday) not in result[str(place.tm_year)][str(place.tm_mon)]:
                                result[str(place.tm_year)][str(place.tm_mon)][str(place.tm_mday)] = {}
                            if str(place.tm_hour) not in result[str(place.tm_year)][str(place.tm_mon)][str(place.tm_mday)]:
                                result[str(place.tm_year)][str(place.tm_mon)][str(place.tm_mday)][str(place.tm_hour)] = {}
                            if str(place.tm_min) not in result[str(place.tm_year)][str(place.tm_mon)][str(place.tm_mday)][str(place.tm_hour)]:
                                result[str(place.tm_year)][str(place.tm_mon)][str(place.tm_mday)][str(place.tm_hour)][str(place.tm_min)] = {}
                            result[str(place.tm_year)][str(place.tm_mon)][str(place.tm_mday)][str(place.tm_hour)][
                                str(place.tm_min)][str(place.tm_min)] = status
                if to_timestamp is None:
                    break
            break
        return result

    def put_status(self, timestamp: float, data: object):
        file = str(int(timestamp))[:-5] + '.aura'
        marker = str(int(timestamp))[-5:]
        path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data', file))
        self.__logger.log('Putting status file:', path, 'with marker:', marker)
        line = marker + "|" + "$marker$".join("$newline$".join(json.dumps(data).split("\n")).split("|")) + "\n"
        open(path, 'a', errors='strict').write(line)
