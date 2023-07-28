import logging
import os
import datetime


class Logger:
    __instance = None

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            print("Logger new")
            cls.__instance = super().__new__(cls, *args, **kwargs)
            cls.__instance = logging.getLogger("my-logger")
            cls.__instance.setLevel(logging.DEBUG)
            formatter = logging.Formatter("%(asctime)s \t [%(levelname)s | %(filename)s:%(lineno)s] > %(message)s")

            now = datetime.datetime.now()
            dirname = "./log"

            if not os.path.isdir(dirname):
                os.mkdir(dirname)
            fileHandler = logging.FileHandler(dirname + "/log_" + now.strftime("%Y-%m-%d") + ".log")

            streamHandler = logging.StreamHandler()

            fileHandler.setFormatter(formatter)
            streamHandler.setFormatter(formatter)

            cls.__instance.addHandler(fileHandler)
            cls.__instance.addHandler(streamHandler)

        return cls.__instance
