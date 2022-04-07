"""Socket listener module.

This module allow to listen to web socket used on Flask site side.
All received event will create a call to EngineCommands using a SocketListner.
"""

from typing import Any, Dict, List

from injector import inject, singleton

from pycodeanalyzer.injection import injector
from pycodeanalyzer.ui.app import Application
from pycodeanalyzer.ui.engineinterface import EngineCommands

app = injector.get(Application)


@singleton
class SocketListner:
    """Socket listener class.

    This class is responsible to call engine commands on web socket events
    """

    @inject
    def __init__(self, engineCommands: EngineCommands) -> None:
        self.engineCommands = engineCommands

    def fetchStats(self) -> None:
        self.engineCommands.requestAnalysisStats()

    def fetchAnalysedClassNames(self) -> None:
        self.engineCommands.requestClasseNames()

    def fetchAnalysedEnumNames(self) -> None:
        self.engineCommands.requestEnumNames()

    def fetchAnalysedFunctionNames(self) -> None:
        self.engineCommands.requestFunctionNames()

    def fetchAnalysedFileNames(self) -> None:
        self.engineCommands.requestFileNames()

    def fetchClassData(self, className: str) -> None:
        self.engineCommands.requestClassData(className)

    def fetchEnumData(self, enumName: str) -> None:
        self.engineCommands.requestEnumData(enumName)

    def fetchFunctionData(self, functionDef: str) -> None:
        self.engineCommands.requestFunctionData(functionDef)

    def fetchFileData(self, fileName: str) -> None:
        self.engineCommands.requestFileData(fileName)

    def searchData(self, token: str) -> None:
        self.engineCommands.requestSearchData(token)

    def changeUsedByUse(self, activated: bool) -> None:
        self.engineCommands.setUsedByActivation(activated)

    def requestUsedByUse(self) -> None:
        self.engineCommands.requestUsedByUse()


@app.socketio.on("fetchStats")
def fetchStats(json: Dict["str", Any], methods: List[str] = ["GET", "POST"]) -> None:
    injector.get(SocketListner).fetchStats()


@app.socketio.on("fetchAnalysedClassNames")
def fetchAnalysedClassNames(
    json: Dict["str", Any], methods: List[str] = ["GET", "POST"]
) -> None:
    injector.get(SocketListner).fetchAnalysedClassNames()


@app.socketio.on("fetchAnalysedEnumNames")
def fetchAnalysedEnumNames(
    json: Dict["str", Any], methods: List[str] = ["GET", "POST"]
) -> None:
    injector.get(SocketListner).fetchAnalysedEnumNames()


@app.socketio.on("fetchAnalysedFunctionNames")
def fetchAnalysedFunctionNames(
    json: Dict["str", Any], methods: List[str] = ["GET", "POST"]
) -> None:
    injector.get(SocketListner).fetchAnalysedFunctionNames()


@app.socketio.on("fetchAnalysedFileNames")
def fetchAnalysedFileNames(
    json: Dict["str", Any], methods: List[str] = ["GET", "POST"]
) -> None:
    injector.get(SocketListner).fetchAnalysedFileNames()


@app.socketio.on("fetchClassData")
def fetchClassData(
    json: Dict["str", Any], methods: List[str] = ["GET", "POST"]
) -> None:
    injector.get(SocketListner).fetchClassData(json["className"])


@app.socketio.on("fetchEnumData")
def fetchEnumData(json: Dict["str", Any], methods: List[str] = ["GET", "POST"]) -> None:
    injector.get(SocketListner).fetchEnumData(json["enumName"])


@app.socketio.on("fetchFunctionData")
def fetchFunctionData(
    json: Dict["str", Any], methods: List[str] = ["GET", "POST"]
) -> None:
    injector.get(SocketListner).fetchFunctionData(json["functionDef"])


@app.socketio.on("fetchFileData")
def fetchFileData(json: Dict["str", Any], methods: List[str] = ["GET", "POST"]) -> None:
    injector.get(SocketListner).fetchFileData(json["fileName"])


@app.socketio.on("searchData")
def searchData(json: Dict["str", Any], methods: List[str] = ["GET", "POST"]) -> None:
    injector.get(SocketListner).searchData(json["token"])


@app.socketio.on("changeUsedByUse")
def changeUsedByUse(
    json: Dict["str", Any], methods: List[str] = ["GET", "POST"]
) -> None:
    injector.get(SocketListner).changeUsedByUse(json["activated"])


@app.socketio.on("requestUsedByUse")
def requestUsedByUse(
    json: Dict["str", Any], methods: List[str] = ["GET", "POST"]
) -> None:
    injector.get(SocketListner).requestUsedByUse()
