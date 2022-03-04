
import logging

class LoggerFactory:

    level = logging.INFO

    @staticmethod
    def init():
        logging.basicConfig(format='%(asctime)s - LoggerFactory - %(levelname)s - %(message)s', level=logging.INFO)

    @staticmethod
    def setLoggerLevel(loglevel):
        LoggerFactory.level = getattr(logging, loglevel, None)
        if not isinstance(LoggerFactory.level, int):
            raise ValueError('Invalid log level: %s' % loglevel)
        logging.info("Debug level set to %s", logging.getLevelName(LoggerFactory.level))


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
