import traceback
import os


class Logger:
    def __init__(self, subtag="Main", direct_output=False):
        self.subtag = subtag
        self.direct = direct_output

    def __send(self, clr, p, m, a=None):
        os.system("logger -p {p} -t \"aura:{s}\" \"{m}\"".format(p=p, s=self.subtag, m=m))
        if a is not None:
            os.system("logger -p {p} -t \"aura:{s}\" \"{m}\"".format(p=p, s=self.subtag, m=a))
        if self.direct:
            try:
                print("\x1b[1;{clr}m{s} | {m}\x1b[0m".format(clr=clr, s=self.subtag, m=m))
                if a is not None:
                    print("\x1b[{clr}m{m}\x1b[0m".format(clr=clr, m=a))
            except IOError:
                os.system("logger -p 4 -t \"aura:Logger\" \"IO Error happened during output\"")

    def log(self, *args):
        message = " ".join(map(lambda x: str(x), args))
        self.__send(36, 6, message)

    def warn(self, *args):
        message = " ".join(map(lambda x: str(x), args))
        self.__send(33, 4, message)

    def warnerr(self, e: Exception):
        try:
            message = "Exception {}: <{}>".format(str(e.errno), e.strerror)
        except AttributeError:
            message = "Exception: <{}>".format(str(e))
        trace = "".join(traceback.format_exc())
        self.__send(33, 4, message, trace)

    def error(self, e: Exception):
        try:
            message = "Exception {}: <{}>".format(str(e.errno), e.strerror)
        except AttributeError:
            message = "Exception: <{}>".format(str(e))
        trace = "".join(traceback.format_exc())
        self.__send(31, 3, message, trace)
