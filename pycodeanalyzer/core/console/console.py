import argparse
from typing import Any

from pycodeanalyzer.core.engine.engine import Engine
from pycodeanalyzer.core.logging.loggerfactory import LoggerFactory


class Console:
    def _parseArgs(self) -> Any:
        parser = argparse.ArgumentParser()
        parser.prog = "pycodeanalyzer"
        parser.add_argument(
            "--log",
            default="INFO",
            required=False,
            help="Log level to be used",
            dest="loglevel",
        )
        parser.add_argument(
            "path", nargs="+", help="Path of a root directory to be analysed"
        )
        return parser.parse_args()

    def init(self) -> None:
        self.args = self._parseArgs()
        LoggerFactory.init()
        LoggerFactory.setLoggerLevel(self.args.loglevel)

    def run(self, engine: Engine) -> None:
        engine.run(self.args)
