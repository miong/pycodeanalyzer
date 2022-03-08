from injector import inject

from pycodeanalyzer.core.analyzer.identification import IdentityAnalyser
from pycodeanalyzer.core.filetree.filefetcher import FileFetcher
from pycodeanalyzer.core.languages.filedispatcher import FileDispatcher
from pycodeanalyzer.core.logging.loggerfactory import LoggerFactory
from pycodeanalyzer.core.utils.math import round_up

import time

class Engine:

    @inject
    def __init__(self, fileFetcher : FileFetcher, fileDispatcher : FileDispatcher, identityAnalyser : IdentityAnalyser):
        self.fileFetcher = fileFetcher
        self.fileDispatcher = fileDispatcher
        self.identityAnalyser = identityAnalyser
        self.files = []

    def run(self, args):
        self.logger = LoggerFactory.createLogger(__name__)
        start_time = time.time()
        self.logger.debug("Setting up analyzers")
        self.logger.info("Start analysis")
        self.logger.debug("Fetching files")
        #TODO allow multiple src dirs
        self.files = self.fileFetcher.fetch(args.path)
        if not self.files:
            self.logger.debug("No files to analyze, quitting.")
        self.logger.debug("Analysing fetched files")
        abstractObjects = self.fileDispatcher.dispatch(args.path, self.files)
        self.performAnalysis(abstractObjects)
        self.logger.info("End analysis")
        end_time = time.time()
        self.logger.info("Analysis duration : %s seconds", str(round_up(end_time - start_time, 2)))

    def performAnalysis(self, abstractObjects):
        self.identityAnalyser.analyze(abstractObjects)
        self.logger.info("Stats :")
        self.logger.info("Files found %d", len(self.files))
        self.logger.info("Classes found %d", len(self.identityAnalyser.getClasses()))
        self.logger.info("Enums found %d", len(self.identityAnalyser.getEnums()))

        for type in self.identityAnalyser.getClasses()[0].getLinkedTypes():
            print("linked to ", type)
            for klass in self.identityAnalyser.getClasses():
                print("trying", klass.name)
                if klass.name == type:
                    print("found as class in ", klass.origin)
