import time

from injector import inject, singleton

from pycodeanalyzer.core.analyzer.dependancy import DependancyAnalyser
from pycodeanalyzer.core.analyzer.identification import IdentityAnalyser
from pycodeanalyzer.core.diagrams.mermaid import ClassDiagramBuild
from pycodeanalyzer.core.filetree.filefetcher import FileFetcher
from pycodeanalyzer.core.languages.filedispatcher import FileDispatcher
from pycodeanalyzer.core.logging.loggerfactory import LoggerFactory
from pycodeanalyzer.core.utils.math import round_up
from pycodeanalyzer.ui.app import UiBrowseListener, UiStatListener, Application
from pycodeanalyzer.injection import injector

app = injector.get(Application)

class AnalysisStats:
    def __init__(self):
        self.nbFiles = 0
        self.nbClasses = 0
        self.nbEnums = 0
        self.nbFunctions = 0
        self.timeSpent = 0


@singleton
class Engine:
    @inject
    def __init__(
        self,
        fileFetcher: FileFetcher,
        fileDispatcher: FileDispatcher,
        identityAnalyser: IdentityAnalyser,
        dependancyAnalyser: DependancyAnalyser,
        uiStatListener: UiStatListener,
        uiBrowseListener: UiBrowseListener,
        classDiagramBuild: ClassDiagramBuild,
    ):
        self.fileFetcher = fileFetcher
        self.fileDispatcher = fileDispatcher
        self.identityAnalyser = identityAnalyser
        self.dependancyAnalyser = dependancyAnalyser
        self.uiStatListener = uiStatListener
        self.uiBrowseListener = uiBrowseListener
        self.files = []
        self.stats = AnalysisStats()
        self.classDiagramBuild = classDiagramBuild

    def run(self, args):
        app.run()
        time.sleep(2)
        self.logger = LoggerFactory.createLogger(__name__)
        start_time = time.time()
        self.logger.debug("Setting up analyzers")
        self.logger.info("Start analysis")
        self.logger.debug("Fetching files")
        # TODO allow multiple src dirs
        self.files = self.fileFetcher.fetch(args.path)
        if not self.files:
            self.logger.debug("No files to analyze, quitting.")
        self.logger.debug("Analysing fetched files")
        abstractObjects = self.fileDispatcher.dispatch(args.path, self.files)
        self.identityAnalyser.analyze(abstractObjects)
        self.logger.info("End analysis")
        end_time = time.time()
        self.recordStats(round_up(end_time - start_time, 2))

    def recordStats(self, duration):
        self.stats.nbFiles = len(self.files)
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

    def sendAnalysisStats(self):
        self.logger.debug("Stats sent to UI")
        self.uiStatListener.notifyStats(
            self.stats.nbFiles,
            self.stats.nbClasses,
            self.stats.nbEnums,
            self.stats.nbFunctions,
            self.stats.timeSpent,
        )

    def sendClasseNames(self):
        self.logger.debug("Class name tree sent to UI")
        self.uiBrowseListener.notifyClasseNames(self.identityAnalyser.getClasseTree())

    def sendClassData(self, className):
        klass = self.identityAnalyser.getClass(className)
        if not klass:
            self.logger.error("Unknow class requested : %s", className)
            return
        objects = self.dependancyAnalyser.analyze(
            self.identityAnalyser.getClasses(), self.identityAnalyser.getEnums(), klass
        )
        self.classDiagramBuild.reset()
        self.classDiagramBuild.create(objects[0], objects[1], objects[2], objects[3])
        mermaidDiag = self.classDiagramBuild.build()
        klassDesc = {}
        klassDesc["name"] = klass.name
        klassDesc["namespace"] = klass.namespace
        klassDesc["file"] = klass.origin
        klassDesc["parents"] = []
        for parent in klass.parents:
            klassDesc["parents"].append(parent[0])
        self.logger.debug("Class data sent to UI")
        self.uiBrowseListener.notifyClassData(klassDesc, mermaidDiag)
