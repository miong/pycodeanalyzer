import time
from typing import Any, Dict, List, Tuple

import jsonpickle
from injector import inject, singleton

from pycodeanalyzer.core.analyzer.dependancy import DependancyAnalyser
from pycodeanalyzer.core.analyzer.identification import IdentityAnalyser
from pycodeanalyzer.core.analyzer.search import SearchAnalyser
from pycodeanalyzer.core.diagrams.mermaid import ClassDiagramBuild
from pycodeanalyzer.core.filetree.filefetcher import FileFetcher
from pycodeanalyzer.core.languages.filedispatcher import FileDispatcher
from pycodeanalyzer.core.logging.loggerfactory import LoggerFactory
from pycodeanalyzer.core.utils.math import round_up
from pycodeanalyzer.injection import injector
from pycodeanalyzer.ui.app import Application, UiBrowseListener, UiStatListener

app = injector.get(Application)


class AnalysisStats:
    def __init__(self) -> None:
        self.nbFiles = 0
        self.nbClasses = 0
        self.nbEnums = 0
        self.nbFunctions = 0
        self.timeSpent = 0.0


@singleton
class Engine:
    @inject
    def __init__(
        self,
        fileFetcher: FileFetcher,
        fileDispatcher: FileDispatcher,
        identityAnalyser: IdentityAnalyser,
        dependancyAnalyser: DependancyAnalyser,
        searchAnalyser: SearchAnalyser,
        uiStatListener: UiStatListener,
        uiBrowseListener: UiBrowseListener,
        classDiagramBuild: ClassDiagramBuild,
    ) -> None:
        self.fileFetcher = fileFetcher
        self.fileDispatcher = fileDispatcher
        self.identityAnalyser = identityAnalyser
        self.dependancyAnalyser = dependancyAnalyser
        self.searchAnalyser = searchAnalyser
        self.uiStatListener = uiStatListener
        self.uiBrowseListener = uiBrowseListener
        self.classDiagramBuild = classDiagramBuild
        self.roots: List[Tuple[str, List[str]]] = []
        self.nbFiles = 0
        self.stats = AnalysisStats()

    def reset(self) -> None:
        self.roots = []
        self.nbFiles = 0
        self.stats = AnalysisStats()

    def run(self, args: Any) -> None:
        self.reset()
        if not args.no_ui:
            app.run()
        time.sleep(2)
        self.logger = LoggerFactory.createLogger(__name__)
        start_time = time.time()
        self.logger.debug("Setting up analyzers")
        self.logger.info("Start analysis")
        self.logger.debug("Fetching files")
        for path in args.path:
            files = self.fileFetcher.fetch(path)
            self.nbFiles += len(files)
            self.roots.append((path, files))
        if self.nbFiles == 0:
            self.logger.debug("No files to analyze, quitting.")
        else:
            self.logger.debug("Analysing fetched files")
            abstractObjects = self.fileDispatcher.dispatchRoots(self.roots)
            self.identityAnalyser.analyze(abstractObjects)
            self.logger.info("End analysis")
        end_time = time.time()
        self.recordStats(round_up(end_time - start_time, 2))
        if args.dumpobj:
            jsonpickle.set_preferred_backend("simplejson")
            jsonpickle.set_encoder_options("simplejson", sort_keys=True, indent=4)
            with open("dumpobj.json", "w") as file:
                file.write(jsonpickle.encode(abstractObjects))

    def recordStats(self, duration: float) -> None:
        self.stats.nbFiles = self.nbFiles
        self.stats.nbClasses = len(self.identityAnalyser.getClasses())
        self.stats.nbEnums = len(self.identityAnalyser.getEnums())
        self.stats.nbFunctions = len(self.identityAnalyser.getFunctions())
        self.stats.timeSpent = duration

        self.logger.info("Stats :")
        self.logger.info("Files found %d", self.stats.nbFiles)
        self.logger.info("Classes found %d", self.stats.nbClasses)
        self.logger.info("Enums found %d", self.stats.nbEnums)
        self.logger.info("Functions found %d", self.stats.nbFunctions)
        self.logger.info("Analysis duration : %s seconds", str(self.stats.timeSpent))

    def sendAnalysisStats(self) -> None:
        self.logger.debug("Stats sent to UI")
        self.uiStatListener.notifyStats(
            self.stats.nbFiles,
            self.stats.nbClasses,
            self.stats.nbEnums,
            self.stats.nbFunctions,
            self.stats.timeSpent,
        )

    def sendClasseNames(self) -> None:
        self.logger.debug("Class name tree sent to UI")
        self.uiBrowseListener.notifyClasseNames(self.identityAnalyser.getClasseTree())

    def sendEnumNames(self) -> None:
        self.logger.debug("Enum name tree sent to UI")
        self.uiBrowseListener.notifyEnumNames(self.identityAnalyser.getEnumTree())

    def sendFunctionNames(self) -> None:
        self.logger.debug("Function name tree sent to UI")
        self.uiBrowseListener.notifyFunctionNames(
            self.identityAnalyser.getFunctionTree()
        )

    def sendFileNames(self) -> None:
        self.logger.debug("File name tree sent to UI")
        self.uiBrowseListener.notifyFileNames(self.identityAnalyser.getFileTree())

    def sendClassData(self, className: str) -> None:
        klass = self.identityAnalyser.getClass(className)
        if not klass:
            self.logger.error("Unknow class requested : %s", className)
            return
        objects = self.dependancyAnalyser.analyze(
            self.identityAnalyser.getClasses(), self.identityAnalyser.getEnums(), klass
        )
        self.classDiagramBuild.reset()
        self.classDiagramBuild.createClass(
            objects[0], objects[1], objects[2], objects[3]
        )
        mermaidDiag = self.classDiagramBuild.build()
        klassDesc: Dict[str, Any] = {}
        klassDesc["name"] = klass.name
        klassDesc["namespace"] = klass.namespace
        klassDesc["file"] = klass.origin
        klassDesc["parents"] = []
        for parent in klass.parents:
            klassDesc["parents"].append(parent[0])
        self.logger.debug("Class data sent to UI")
        self.uiBrowseListener.notifyClassData(klassDesc, mermaidDiag)

    def sendEnumData(self, enumName: str) -> None:
        enum = self.identityAnalyser.getEnum(enumName)
        if not enum:
            self.logger.error("Unknow enum requested : %s", enumName)
            return
        self.classDiagramBuild.reset()
        self.classDiagramBuild.createEnum(enum)
        mermaidDiag = self.classDiagramBuild.build()
        enumDesc = {}
        enumDesc["name"] = enum.name
        enumDesc["namespace"] = enum.namespace
        enumDesc["file"] = enum.origin
        self.logger.debug("Enum data sent to UI")
        self.uiBrowseListener.notifyEnumData(enumDesc, mermaidDiag)

    def sendFunctionData(self, functionDef: str) -> None:
        func = self.identityAnalyser.getFunction(functionDef)
        if not func:
            self.logger.error("Unknow function requested : %s", functionDef)
            return
        functionDesc: Dict[str, Any] = {}
        functionDesc["name"] = func.name
        functionDesc["namespace"] = func.namespace
        functionDesc["file"] = func.origin
        functionDesc["rtype"] = func.returnType
        params = {}
        for param in func.parameters:
            params[param[1]] = param[0]
        functionDesc["params"] = params
        functionDesc["doxygen"] = func.doxygen
        self.logger.debug("Function data sent to UI")
        self.uiBrowseListener.notifyFunctionData(functionDesc)

    def sendFileData(self, fileName: str) -> None:
        filePath = fileName
        if "::" in fileName or "/" not in fileName:
            filePath = (
                self.identityAnalyser.commonFilePath + "/" + fileName.replace("::", "/")
            )
        if "::" not in fileName:
            fileName = fileName.replace(
                self.identityAnalyser.commonFilePath + "/", ""
            ).replace("/", "::")
        fileDesc: Dict[str, Any] = {}
        fileDesc["name"] = fileName
        fileDesc["path"] = filePath
        fileDesc["objects"] = self.identityAnalyser.getObjectInFile(filePath)
        fileDesc["content"] = open(filePath, mode="r").read()
        self.logger.debug("File data sent to UI")
        self.uiBrowseListener.notifyFileData(fileDesc)

    def sendSearchResult(self, token: str) -> None:
        searchRes = self.searchAnalyser.searchInAllFiles(
            token, self.identityAnalyser.getFiles()
        )
        self.uiBrowseListener.notifySearchResult(searchRes)
