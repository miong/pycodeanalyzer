import argparse
from injector import inject

from pycodeanalyzer.core.engine.engine import Engine
from pycodeanalyzer.core.logging.loggerfactory import LoggerFactory


class Console:

    def _parseArgs(self):
        parser = argparse.ArgumentParser()
        parser.add_argument('--log', default='INFO', required=False, help='Log level to be used', dest='loglevel')
        parser.add_argument("path", help='Path of the root directory to be analysed')
        return parser.parse_args()

    def init(self):
        self.args = self._parseArgs()
        LoggerFactory.init()
        LoggerFactory.setLoggerLevel(self.args.loglevel)

    def run(self, engine : Engine):
        engine.run(self.args)
