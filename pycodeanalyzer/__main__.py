from pycodeanalyzer.core.logging.loggerfactory import LoggerFactory

def main():
    LoggerFactory.init()
    LoggerFactory.setLoggerLevel("DEBUG")
    logger = LoggerFactory.createLogger(__name__)
    logger.debug("Start")
    logger.debug("End")


if __name__ == "__main__":
    main()