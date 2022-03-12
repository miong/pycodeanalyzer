from flask import Flask, render_template
from flask_socketio import SocketIO
from flaskwebgui import FlaskUI
from flask_classful import FlaskView, route
import secrets
import threading
import os

from injector import inject, singleton

class UiLink:
    def __init__(self):
        self.socketio = None

    def setSocketIO(self, socketio):
        self.socketio = socketio

@singleton
class UiFileDispatcherListener(UiLink):
    def notifyAnalyzing(self, file):
        if self.socketio:
            self.socketio.emit('fileAnalyzedChange', { "file" : file })

    def notifyAnalysisEnd(self):
        if self.socketio:
            self.socketio.emit('analysisCompleted', {})

@singleton
class UiStatListener(UiLink):
    def notifyStats(self, nbFiles, nbClasses, nbEnums, nbFunctions, duration):
        if self.socketio:
            self.socketio.emit('statsChange', { "nbFiles" : nbFiles, "nbClasses" : nbClasses, "nbEnums" : nbEnums, "nbFunctions" : nbFunctions, "duration" : duration })

@singleton
class UiBrowseListener(UiLink):
    def notifyClasseNames(self, tree):
        if self.socketio:
            self.socketio.emit('classeNamesChange', { "tree" : tree })

    def notifyClassData(self, klass, mermaidDiag):
        if self.socketio:
            self.socketio.emit('classDataChange', { "class" : klass, "mermaidDiag" : mermaidDiag })

@singleton
class Application:

    @inject
    def __init__(self, uiFileDispatcherListener : UiFileDispatcherListener, uiStatListener : UiStatListener, uiBrowseListener : UiBrowseListener):
        templateDir = os.path.join(os.path.abspath(os.path.dirname(__file__)),"web/templates")
        staticDir = os.path.join(os.path.abspath(os.path.dirname(__file__)),"web/static")
        self.app = Flask("pycodeanalyzer", template_folder=templateDir, static_folder=staticDir)
        self.app.config['SECRET_KEY'] = secrets.token_urlsafe(16)
        self.app.use_reloader = True
        self.socketio = SocketIO(self.app, logger=False, engineio_logger=False)
        uiFileDispatcherListener.setSocketIO(self.socketio)
        uiStatListener.setSocketIO(self.socketio)
        uiStatListener.setSocketIO(self.socketio)
        uiBrowseListener.setSocketIO(self.socketio)
        FlaskHolder.register(self.app,route_base = '/')

    def run(self):
        threading.Thread(target=lambda: FlaskUI(self.app, socketio=self.socketio, start_server="flask-socketio").run()).start()



class FlaskHolder(FlaskView):

    @route("/")
    def loading(self):
        return render_template("loading.html")

    @route("/home")
    def home(self):
        return render_template("home.html")

    @route("/browse")
    def browse(self):
        return render_template("browse.html")