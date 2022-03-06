from pycodeanalyzer.core.logging.loggerfactory import LoggerFactory


class FileFetcher:

    def __init__(self):
        self.logger = LoggerFactory.createLogger(__name__)

    def fetch(self, rootDir):
        self.logger.debug("start fetching files from : %s", rootDir)
        self.logger.debug("end fetching files")