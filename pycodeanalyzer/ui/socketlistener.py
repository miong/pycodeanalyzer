from injector import inject, singleton

from pycodeanalyzer.injection import injector
from pycodeanalyzer.ui.app import Application
from pycodeanalyzer.ui.engineinterface import EngineCommands

app = injector.get(Application)


@singleton
class SocketListner:
    @inject
    def __init__(self, engineCommands: EngineCommands):
        self.engineCommands = engineCommands

    def fetchStats(self):
        self.engineCommands.requestAnalysisStats()

    def fetchAnalysedClassNames(self):
        self.engineCommands.requestClasseNames()

    def fetchAnalysedEnumNames(self):
        self.engineCommands.requestEnumNames()

    def fetchAnalysedFunctionNames(self):
        self.engineCommands.requestFunctionNames()

    def fetchAnalysedFileNames(self):
        self.engineCommands.requestFileNames()

    def fetchClassData(self, className):
        self.engineCommands.requestClassData(className)

    def fetchEnumData(self, enumName):
        self.engineCommands.requestEnumData(enumName)

    def fetchFunctionData(self, functionDef):
        self.engineCommands.requestFunctionData(functionDef)

    def fetchFileData(self, fileName):
        self.engineCommands.requestFileData(fileName)

    def searchData(self, token):
        self.engineCommands.requestSearchData(token)


@app.socketio.on("fetchStats")
def fetchStats(json, methods=["GET", "POST"]):
    injector.get(SocketListner).fetchStats()


@app.socketio.on("fetchAnalysedClassNames")
def fetchAnalysedClassNames(json, methods=["GET", "POST"]):
    injector.get(SocketListner).fetchAnalysedClassNames()


@app.socketio.on("fetchAnalysedEnumNames")
def fetchAnalysedEnumNames(json, methods=["GET", "POST"]):
    injector.get(SocketListner).fetchAnalysedEnumNames()


@app.socketio.on("fetchAnalysedFunctionNames")
def fetchAnalysedFunctionNames(json, methods=["GET", "POST"]):
    injector.get(SocketListner).fetchAnalysedFunctionNames()


@app.socketio.on("fetchAnalysedFileNames")
def fetchAnalysedFileNames(json, methods=["GET", "POST"]):
    injector.get(SocketListner).fetchAnalysedFileNames()


@app.socketio.on("fetchClassData")
def fetchClassData(json, methods=["GET", "POST"]):
    injector.get(SocketListner).fetchClassData(json["className"])


@app.socketio.on("fetchEnumData")
def fetchEnumData(json, methods=["GET", "POST"]):
    injector.get(SocketListner).fetchEnumData(json["enumName"])


@app.socketio.on("fetchFunctionData")
def fetchFunctionData(json, methods=["GET", "POST"]):
    injector.get(SocketListner).fetchFunctionData(json["functionDef"])


@app.socketio.on("fetchFileData")
def fetchFileData(json, methods=["GET", "POST"]):
    injector.get(SocketListner).fetchFileData(json["fileName"])


@app.socketio.on("searchData")
def searchData(json, methods=["GET", "POST"]):
    injector.get(SocketListner).searchData(json["token"])
