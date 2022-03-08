from pycodeanalyzer.core.languages.analyzers.cppanalyzer import CppAnalyzer
from pycodeanalyzer.core.logging.loggerfactory import LoggerFactory

from injector import inject
import pathlib

class FileDispatcher:

    @inject
    def __init__(self, cppAnalyzer : CppAnalyzer):
        self.logger = LoggerFactory.createLogger(__name__)
        self.cppAnalyzer = cppAnalyzer

    def dispatch(self, rootDir, files):
        abstractObjects = []
        self.logger.debug("start file dispatching")
        for file in files:
            extension = pathlib.Path(file).suffix
            if extension == ".h" or extension == ".hpp":
                abstractObjects += self.cppAnalyzer.analyze(rootDir, file)
        self.logger.debug("end file dispatching")
        return abstractObjects
