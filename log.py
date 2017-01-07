import logging


class Logger:

    def __init__(self):
        logging.basicConfig(level=logging.DEBUG,
                            format='[%(levelname)s] (%(threadName)-10s) %(message)s',
                            )

    def debug(self, msg):
        logging.debug(msg)
