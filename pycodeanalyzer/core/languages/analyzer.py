from pycodeanalyzer.core.logging.loggerfactory import LoggerFactory

class Analyzer:

    def __init__(self):
        self.logger = LoggerFactory.createLogger(__name__)

    def analyze(self, path):
        self.logger.error("Use of abstract method : analyze from Analyzer class")