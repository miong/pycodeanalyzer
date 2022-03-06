from injector import inject

from pycodeanalyzer.core.filetree.filefetcher import FileFetcher
from pycodeanalyzer.core.languages.filedispatcher import FileDispatcher
from pycodeanalyzer.core.logging.loggerfactory import LoggerFactory
from pycodeanalyzer.core.utils.math import round_up

import time

class Engine:

    @inject
    def __init__(self, fileFetcher : FileFetcher, fileDispatcher : FileDispatcher):
        self.fileFetcher = fileFetcher
        self.fileDispatcher = fileDispatcher

    def run(self, args):
        self.logger = LoggerFactory.createLogger(__name__)
        start_time = time.time()
        self.logger.debug("Setting up analyzers")
        self.logger.info("Start analysis")
        self.logger.debug("Fetching files")
        files = self.fileFetcher.fetch(args.path)
        self.logger.debug("Analysing fetched files")
        self.fileDispatcher.dispatch(files)
        self.logger.info("End analysis")
        end_time = time.time()
        self.logger.info("Analysis duration : %s seconds", str(round_up(end_time - start_time, 2)))
