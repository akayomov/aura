from .backend.handler import RequestsHandler
from .backend.static import StaticFilesHandler
from .backend.processor import RequestsProcessor

from .status.collector import StatusCollector
from .status.cli_designer import CLIDesigner

from .tools.file_manager import FileManager
from .tools.logger import Logger

import time
import sys

arguments = sys.argv[1:]
provide_output = None

if 'status' in arguments:
    sections = ['system', 'internet', 'tunnels', 'features', 'devices', 'provider']
    CLIDesigner(StatusCollector(False).collect(sections, time.time()))
    exit(0)
elif 'service' in arguments:
    provide_output = False
elif 'debug' in arguments:
    provide_output = True
else:
    Logger("Error", True).log("Unknown operation used. Exiting with error")
    exit(1)

if provide_output is not None:
    logger = Logger(direct_output=provide_output)
    logger.log("Starting AURA service loop:", arguments)

    manager = FileManager(provide_output)
    collector = StatusCollector(provide_output)
    handler = RequestsHandler(provide_output)
    StaticFilesHandler(provide_output)
    processor = RequestsProcessor(provide_output)
    handler.start_loop()

    DELAY = 60  # seconds

    min_status = 0
    MIN_TIMES = 1  # DELAY * MIN_TIMES = 60 seconds = 1 minute
    MIN_LIST = ['system', 'internet', 'tunnels']

    mid_status = 0
    MID_TIMES = 3  # DELAY * MID_TIMES = 180 seconds = 3 minute
    MID_LIST = ['features', 'devices']

    max_status = 0
    MAX_TIMES = 12  # DELAY * MAX_TIMES = 600 seconds = 12 minutes
    MAX_LIST = ['provider']

    last_collect = time.time()
    FULL_LIST = ['system', 'internet', 'tunnels', 'features', 'devices', 'provider']
    processor.update_status(collector.collect(FULL_LIST, last_collect))

    while True:
        try:
            current_time = time.time()
            if current_time >= last_collect + DELAY:
                last_collect = current_time
                min_status += 1
                mid_status += 1
                max_status += 1
                check_status = []
                if min_status >= MIN_TIMES:
                    check_status.extend(MIN_LIST)
                    min_status = 0
                if mid_status >= MID_TIMES:
                    check_status.extend(MID_LIST)
                    mid_status = 0
                if max_status >= MAX_TIMES:
                    check_status.extend(MAX_LIST)
                    max_status = 0
                status_update = collector.collect(check_status, current_time)
                processor.update_status(status_update)
                manager.put_status(current_time, status_update)
            time.sleep(0.5)
        except Exception as e:
            logger.error(e)
        except KeyboardInterrupt:
            logger.log('Loop finished by user\'s request')
            break
