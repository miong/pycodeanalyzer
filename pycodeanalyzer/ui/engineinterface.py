from injector import inject, singleton

from pycodeanalyzer.core.engine.engine import Engine
from pycodeanalyzer.core.logging.loggerfactory import LoggerFactory


@singleton
class EngineCommands:
    """Engine commands

    This class represent all the request that could be made to the engine once an analysis have been done.
    """

    @inject
    def __init__(self, engine: Engine) -> None:
        self.engine = engine
        self.logger = LoggerFactory.createLogger(__name__)

    def requestAnalysisStats(self) -> None:
        self.logger.info("Received analysis stats request")
        self.engine.sendAnalysisStats()
        self.logger.info("Anwser sent to UI")

    def requestClasseNames(self) -> None:
        self.logger.info("Received class names request")
        self.engine.sendClasseNames()
        self.logger.info("Anwser sent to UI")

    def requestEnumNames(self) -> None:
        self.logger.info("Received enum names request")
        self.engine.sendEnumNames()
        self.logger.info("Anwser sent to UI")

    def requestFunctionNames(self) -> None:
        self.logger.info("Received function names request")
        self.engine.sendFunctionNames()
        self.logger.info("Anwser sent to UI")

    def requestFileNames(self) -> None:
        self.logger.info("Received file names request")
        self.engine.sendFileNames()
        self.logger.info("Anwser sent to UI")

    def requestClassData(self, className: str) -> None:
        self.logger.info("Received class data request for %s", className)
        self.engine.sendClassData(className)
        self.logger.info("Anwser sent to UI")

    def requestEnumData(self, enumName: str) -> None:
        self.logger.info("Received enum data request for %s", enumName)
        self.engine.sendEnumData(enumName)
        self.logger.info("Anwser sent to UI")

    def requestFunctionData(self, functionDef: str) -> None:
        self.logger.info("Received function data request for %s", functionDef)
        self.engine.sendFunctionData(functionDef)
        self.logger.info("Anwser sent to UI")

    def requestFileData(self, fileName: str) -> None:
        self.logger.info("Received file data request for %s", fileName)
        self.engine.sendFileData(fileName)
        self.logger.info("Anwser sent to UI")

    def requestSearchData(self, token: str) -> None:
        self.logger.info("Received search request for %s", token)
        self.engine.sendSearchResult(token)
        self.logger.info("Anwser sent to UI")

    def setUsedByActivation(self, activated: bool) -> None:
        self.logger.info("Received use by activation %s", activated)
        self.engine.setUsedByActivation(activated)
        self.logger.info("Request traited")

    def requestUsedByUse(self) -> None:
        self.logger.info("Received use by request")
        self.engine.requestUsedByUse()
        self.logger.info("Anwser sent to UI")
