import pathlib

from injector import inject, singleton

from pycodeanalyzer.core.languages.analyzers.cppanalyzer import CppAnalyzer
from pycodeanalyzer.core.logging.loggerfactory import LoggerFactory
from pycodeanalyzer.ui.app import UiFileDispatcherListener


@singleton
class FileDispatcher:
    @inject
    def __init__(self, cppAnalyzer: CppAnalyzer, uiListener: UiFileDispatcherListener):
        self.logger = LoggerFactory.createLogger(__name__)
        self.cppAnalyzer = cppAnalyzer
        self.uiListener = uiListener

    def dispatchRoots(self, roots):
        self.logger.debug("start file dispatching")
        abstractObjects = []
        for rootDir, files in roots:
            abstractObjects.extend(self.dispatch(rootDir, files))
        self.logger.debug("end file dispatching")
        self.uiListener.notifyAnalysisEnd()
        return abstractObjects

    def dispatch(self, rootDir, files):
        abstractObjects = []
        for file in files:
            extension = pathlib.Path(file).suffix
            if extension == ".h" or extension == ".hpp":
                self.uiListener.notifyAnalyzing(file)
                abstractObjects += self.cppAnalyzer.analyze(rootDir, file)
        return abstractObjects
