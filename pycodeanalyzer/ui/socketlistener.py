
from pycodeanalyzer.injection import injector
from pycodeanalyzer.ui.engineinterface import EngineCommands
from pycodeanalyzer.ui.app import Application

from flask_socketio import SocketIO

from injector import inject, singleton

app = injector.get(Application)

@singleton
class SocketListner:
    @inject
    def __init__(self, engineCommands : EngineCommands):
        self.engineCommands = engineCommands

    def fetchStats(self):
        self.engineCommands.requestAnalysisStats()

    def fetchAnalysedClassNames(self):
        self.engineCommands.requestClasseNames()

    def fetchClassData(self, className):
        self.engineCommands.requestClassData(className)


@app.socketio.on('fetchStats')
def fetchStats(json, methods=['GET', 'POST']):
    injector.get(SocketListner).fetchStats()

@app.socketio.on('fetchAnalysedClassNames')
def fetchAnalysedClassNames(json, methods=['GET', 'POST']):
    injector.get(SocketListner).fetchAnalysedClassNames()

@app.socketio.on('fetchClassData')
def fetchClassData(json, methods=['GET', 'POST']):
    injector.get(SocketListner).fetchClassData(json["className"])

app.run()
