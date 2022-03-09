from pycodeanalyzer.core.engine.engine import Engine

from injector import inject, singleton

@singleton
class EngineCommands:
    @inject
    def __init__(self, engine : Engine):
        self.engine = engine

    def requestAnalysisStats(self):
        self.engine.sendAnalysisStats()

    def requestClasseNames(self):
        self.engine.sendClasseNames()

    def requestClassData(self, className):
        self.engine.sendClassData(className)
