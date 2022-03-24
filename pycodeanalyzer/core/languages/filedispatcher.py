import pathlib
from typing import List, Tuple

from injector import inject, singleton

from pycodeanalyzer.core.abstraction.objects import (
    AbstractObject,
    compareAbstractObject,
)
from pycodeanalyzer.core.languages.analyzers.cppanalyzer import CppAnalyzer
from pycodeanalyzer.core.languages.analyzers.pythonanalyzer import PythonAnalyzer
from pycodeanalyzer.core.logging.loggerfactory import LoggerFactory
from pycodeanalyzer.ui.app import UiFileDispatcherListener


@singleton
class FileDispatcher:
    @inject
    def __init__(
        self,
        cppAnalyzer: CppAnalyzer,
        pythonAnalyzer: PythonAnalyzer,
        uiListener: UiFileDispatcherListener,
    ) -> None:
        self.logger = LoggerFactory.createLogger(__name__)
        self.cppAnalyzer = cppAnalyzer
        self.pythonAnalyzer = pythonAnalyzer
        self.uiListener = uiListener

    def dispatchRoots(self, roots: List[Tuple[str, List[str]]]) -> List[AbstractObject]:
        self.logger.debug("start file dispatching")
        abstractObjects: List[AbstractObject] = []
        for rootDir, files in roots:
            abstractObjects.extend(self.dispatch(rootDir, files))
        self.logger.debug("end file dispatching")
        self.sortObjects(abstractObjects)
        self.uiListener.notifyAnalysisEnd()
        return abstractObjects

    def dispatch(self, rootDir: str, files: List[str]) -> List[AbstractObject]:
        abstractObjects = []
        for file in files:
            extension = pathlib.Path(file).suffix
            if extension == ".h" or extension == ".hpp":
                self.uiListener.notifyAnalyzing(file)
                abstractObjects += self.cppAnalyzer.analyze(rootDir, file)
            if extension == ".py":
                self.uiListener.notifyAnalyzing(file)
                abstractObjects += self.pythonAnalyzer.analyze(rootDir, file)
        return abstractObjects

    def sortObjects(self, abstractObjects: List[AbstractObject]) -> None:
        abstractObjects.sort(key=compareAbstractObject)
