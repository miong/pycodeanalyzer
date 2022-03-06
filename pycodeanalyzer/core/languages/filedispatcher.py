from injector import inject

from pycodeanalyzer.core.languages.analyzers.cppanalyzer import CppAnalyzer
from pycodeanalyzer.core.logging.loggerfactory import LoggerFactory


class FileDispatcher:

    @inject
    def __init__(self, cppAnalyzer : CppAnalyzer):
        self.logger = LoggerFactory.createLogger(__name__)

    def dispatch(self, files):
        self.logger.debug("start file dispatching")
        self.logger.debug("end file dispatching")