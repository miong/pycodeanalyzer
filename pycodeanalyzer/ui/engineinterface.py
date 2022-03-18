from injector import inject, singleton

from pycodeanalyzer.core.engine.engine import Engine


@singleton
class EngineCommands:
    @inject
    def __init__(self, engine: Engine) -> None:
        self.engine = engine

    def requestAnalysisStats(self) -> None:
        self.engine.sendAnalysisStats()

    def requestClasseNames(self) -> None:
        self.engine.sendClasseNames()

    def requestEnumNames(self) -> None:
        self.engine.sendEnumNames()

    def requestFunctionNames(self) -> None:
        self.engine.sendFunctionNames()

    def requestFileNames(self) -> None:
        self.engine.sendFileNames()

    def requestClassData(self, className: str) -> None:
        self.engine.sendClassData(className)

    def requestEnumData(self, enumName: str) -> None:
        self.engine.sendEnumData(enumName)

    def requestFunctionData(self, functionDef: str) -> None:
        self.engine.sendFunctionData(functionDef)

    def requestFileData(self, fileName: str) -> None:
        self.engine.sendFileData(fileName)

    def requestSearchData(self, token: str) -> None:
        self.engine.sendSearchResult(token)
