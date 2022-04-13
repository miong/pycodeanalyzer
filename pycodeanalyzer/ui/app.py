"""App module.

This module define all the class related to UI.
"""

import os
import secrets
import threading
from typing import Any, Dict, List, Tuple

from flask import Flask, render_template
from flask_classful import FlaskView, route
from flask_socketio import SocketIO
from flaskwebgui import FlaskUI
from injector import inject, singleton


class UiLink:
    """Base of UI communation using web sockets"""

    def __init__(self) -> None:
        self.socketio: SocketIO = None

    def setSocketIO(self, socketio: SocketIO) -> None:
        self.socketio = socketio


@singleton
class UiFileDispatcherListener(UiLink):
    def notifyAnalyzing(self, file: str) -> None:
        if self.socketio:
            self.socketio.emit("fileAnalyzedChange", {"file": file})

    def notifyAnalysisEnd(self) -> None:
        if self.socketio:
            self.socketio.emit("analysisCompleted", {})


@singleton
class UiStatListener(UiLink):
    def notifyStats(
        self,
        nbFiles: int,
        nbClasses: int,
        nbEnums: int,
        nbFunctions: int,
        languagePie: str,
        duration: float,
    ) -> None:
        if self.socketio:
            self.socketio.emit(
                "statsChange",
                {
                    "nbFiles": nbFiles,
                    "nbClasses": nbClasses,
                    "nbEnums": nbEnums,
                    "nbFunctions": nbFunctions,
                    "languagePie": languagePie,
                    "duration": duration,
                },
            )


@singleton
class UiBrowseListener(UiLink):
    def notifyClasseNames(self, tree: Dict[str, Any]) -> None:
        if self.socketio:
            self.socketio.emit("classeNamesChange", {"tree": tree})

    def notifyEnumNames(self, tree: Dict[str, Any]) -> None:
        if self.socketio:
            self.socketio.emit("enumNamesChange", {"tree": tree})

    def notifyFunctionNames(self, tree: Dict[str, Any]) -> None:
        if self.socketio:
            self.socketio.emit("functionNamesChange", {"tree": tree})

    def notifyFileNames(self, tree: Dict[str, Any]) -> None:
        if self.socketio:
            self.socketio.emit("fileNamesChange", {"tree": tree})

    def notifyClassData(self, klass: Dict[str, Any], mermaidDiag: str) -> None:
        if self.socketio:
            self.socketio.emit(
                "classDataChange", {"class": klass, "mermaidDiag": mermaidDiag}
            )

    def notifyEnumData(self, enum: Dict[str, Any], mermaidDiag: str) -> None:
        if self.socketio:
            self.socketio.emit(
                "enumDataChange", {"enum": enum, "mermaidDiag": mermaidDiag}
            )

    def notifyFunctionData(self, function: Dict[str, Any]) -> None:
        if self.socketio:
            self.socketio.emit("functionDataChange", {"function": function})

    def notifyFileData(self, file: Dict[str, Any]) -> None:
        if self.socketio:
            self.socketio.emit("fileDataChange", {"file": file})

    def notifySearchResult(self, searchRes: List[Tuple[str, str]]) -> None:
        if self.socketio:
            self.socketio.emit("searchResult", {"res": searchRes})

    def notifyUsedByUse(self, activated: bool) -> None:
        if self.socketio:
            self.socketio.emit("usedByUseChange", {"activated": activated})


@singleton
class Application:
    @inject
    def __init__(
        self,
        uiFileDispatcherListener: UiFileDispatcherListener,
        uiStatListener: UiStatListener,
        uiBrowseListener: UiBrowseListener,
    ) -> None:
        templateDir = os.path.join(
            os.path.abspath(os.path.dirname(__file__)), "web/templates"
        )
        staticDir = os.path.join(
            os.path.abspath(os.path.dirname(__file__)), "web/static"
        )
        self.app = Flask(
            "pycodeanalyzer", template_folder=templateDir, static_folder=staticDir
        )
        self.app.config["SECRET_KEY"] = secrets.token_urlsafe(16)
        self.app.use_reloader = True
        self.socketio = SocketIO(self.app, logger=False, engineio_logger=False)
        self.ui: FlaskUI = None
        uiFileDispatcherListener.setSocketIO(self.socketio)
        uiStatListener.setSocketIO(self.socketio)
        uiStatListener.setSocketIO(self.socketio)
        uiBrowseListener.setSocketIO(self.socketio)
        FlaskHolder.register(self.app, route_base="/")

    def run(self) -> None:
        self.ui = FlaskUI(
            self.app, socketio=self.socketio, start_server="flask-socketio"
        )
        threading.Thread(target=lambda: self.ui.run()).start()

    def quit(self) -> None:
        if self.ui:
            self.ui.idle_interval = 0


class FlaskHolder(FlaskView):
    @route("/")
    def loading(self) -> str:
        return render_template("loading.html")

    @route("/home")
    def home(self) -> str:
        return render_template("home.html")

    @route("/browse")
    @route("/browse/classes")
    @route("/browse/enums")
    @route("/browse/functions")
    @route("/browse/files")
    @route("/browse/search")
    def browse(self) -> str:
        return render_template("browse.html")
