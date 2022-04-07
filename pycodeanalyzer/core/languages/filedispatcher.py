import pathlib
from typing import List, Tuple

from injector import inject, singleton

from pycodeanalyzer.core.abstraction.objects import (
    AbstractObject,
    compareAbstractObject,
)
from pycodeanalyzer.core.languages.analyzers.cppanalyzer import CppAnalyzer
from pycodeanalyzer.core.languages.analyzers.javaanalyzer import JavaAnalyzer
from pycodeanalyzer.core.languages.analyzers.kotlinanalyzer import KotlinAnalyzer
from pycodeanalyzer.core.languages.analyzers.pythonanalyzer import PythonAnalyzer
from pycodeanalyzer.core.languages.extensions import languageExtensions
from pycodeanalyzer.core.logging.loggerfactory import LoggerFactory
from pycodeanalyzer.ui.app import UiFileDispatcherListener


@singleton
class FileDispatcher:
    """File dispatcher.

    This class allow to dispatch fetched files to the correct language analyzer.
    """

    @inject
    def __init__(
        self,
        cppAnalyzer: CppAnalyzer,
        pythonAnalyzer: PythonAnalyzer,
        javaAnalyzer: JavaAnalyzer,
        kotlinAnalyzer: KotlinAnalyzer,
        uiListener: UiFileDispatcherListener,
    ) -> None:
        self.logger = LoggerFactory.createLogger(__name__)
        self.cppAnalyzer = cppAnalyzer
        self.pythonAnalyzer = pythonAnalyzer
        self.javaAnalyzer = javaAnalyzer
        self.kotlinAnalyzer = kotlinAnalyzer
        self.uiListener = uiListener

    def dispatchRoots(self, roots: List[Tuple[str, List[str]]]) -> List[AbstractObject]:
        self.logger.debug("start file dispatching")
        abstractObjects: List[AbstractObject] = []
        for rootDir, files in roots:
            abstractObjects.extend(self.dispatch(rootDir, files))
        self.logger.debug("end file dispatching")
        self.uiListener.notifyAnalysisEnd()
        return self.sortObjects(abstractObjects)

    def dispatch(self, rootDir: str, files: List[str]) -> List[AbstractObject]:
        abstractObjects = []
        for file in files:
            extension = pathlib.Path(file).suffix
            language = None
            if extension in languageExtensions.keys():
                language = languageExtensions[extension]
            if language == "CPP":
                self.uiListener.notifyAnalyzing(file)
                abstractObjects += self.cppAnalyzer.analyze(rootDir, file)
            if language == "PYTHON":
                self.uiListener.notifyAnalyzing(file)
                abstractObjects += self.pythonAnalyzer.analyze(rootDir, file)
            if language == "JAVA":
                self.uiListener.notifyAnalyzing(file)
                abstractObjects += self.javaAnalyzer.analyze(rootDir, file)
            if language == "KOTLIN":
                self.uiListener.notifyAnalyzing(file)
                abstractObjects += self.kotlinAnalyzer.analyze(rootDir, file)
        return abstractObjects

    def sortObjects(
        self, abstractObjects: List[AbstractObject]
    ) -> List[AbstractObject]:
        return sorted(abstractObjects, key=compareAbstractObject)
