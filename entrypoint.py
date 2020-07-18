import os
import subprocess
from argparse import ArgumentParser


class EntryPoint:
    def __init__(self):
        unit = str(subprocess.run(['uname', '-n'], stdout=subprocess.PIPE).stdout, 'utf-8').rstrip()
        print("Running on node: " + unit)

        selector = {
            'nibiru': self.keenetic_router,
            'oakaiomov-devtool': self.keenetic_router,
        }

        selector.get(unit, self.unknown)()

    @staticmethod
    def keenetic_router():
        path = os.path.dirname(__file__)

        argp = ArgumentParser(description="Automation entry point")

        argp.add_argument('-p', '--pid', help="PID file path")
        argp.add_argument('--service', help="Run a service", action='store_true')
        argp.add_argument('--status', help="Get a router status", action='store_true')

        argv = argp.parse_args()

        if argv.service:
            process = subprocess.Popen(['python3', '-m', 'keenetic', 'service'], cwd=path+"/routers/",
                                       stdout=subprocess.PIPE)
            print("Service started with pid '"+str(process.pid)+"'", end="")
            if argv.pid:
                open(argv.pid, 'w').write(str(process.pid))
                print(", pidfile:", argv.pid)
            else:
                print()
        elif argv.status:
            process = subprocess.Popen(['python3', '-m', 'keenetic', 'status'], cwd=path + "/routers/",
                                       stdout=subprocess.PIPE)
            print("Running to get status...")
            print(str(process.stdout.read(), encoding='ascii'))
        else:
            print("Execution ignored, use --service to start service, or --status to see status.")

    @staticmethod
    def unknown():
        print("Started on unknown node")


if __name__ == "__main__":
    EntryPoint()
