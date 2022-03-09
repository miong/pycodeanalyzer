
import logging
from functools import partial

class LoggerFactory:

    level = logging.INFO
    defaultLogger = None

    @staticmethod
    def init():
        logging.basicConfig(format='%(asctime)s - LoggerFactory - %(levelname)s - %(message)s', level=logging.INFO)
        LoggerFactory.defaultLogger = LoggerFactory.createLogger("DefaultLogger")
        logging.root = LoggerFactory.defaultLogger
        # Setting log level for known used packages
        logging.getLogger('werkzeug').setLevel(logging.WARNING)


    @staticmethod
    def setLoggerLevel(loglevel):
        LoggerFactory.level = getattr(logging, loglevel, None)
        if not isinstance(LoggerFactory.level, int):
            raise ValueError('Invalid log level: %s' % loglevel)
        logging.debug("Debug level set to %s", logging.getLevelName(LoggerFactory.level))
        logging.root.setLevel(LoggerFactory.level)


    @staticmethod
    def createLogger(name):
        logger = logging.getLogger(name)
        logger.setLevel(LoggerFactory.level)
        ch = logging.StreamHandler()
        ch.setLevel(LoggerFactory.level)
        ch.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
        logger.addHandler(ch)
        logger.propagate = 0
        return logger
