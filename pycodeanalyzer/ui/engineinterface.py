from injector import inject, singleton

from pycodeanalyzer.core.engine.engine import Engine


@singleton
class EngineCommands:
    @inject
    def __init__(self, engine: Engine):
        self.engine = engine

    def requestAnalysisStats(self):
        self.engine.sendAnalysisStats()

    def requestClasseNames(self):
        self.engine.sendClasseNames()

    def requestEnumNames(self):
        self.engine.sendEnumNames()

    def requestFunctionNames(self):
        self.engine.sendFunctionNames()

    def requestFileNames(self):
        self.engine.sendFileNames()

    def requestClassData(self, className):
        self.engine.sendClassData(className)

    def requestEnumData(self, enumName):
        self.engine.sendEnumData(enumName)

    def requestFunctionData(self, functionDef):
        self.engine.sendFunctionData(functionDef)

    def requestFileData(self, fileName):
        self.engine.sendFileData(fileName)
