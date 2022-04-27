import argparse
from typing import Any

from pycodeanalyzer.core.engine.engine import Engine
from pycodeanalyzer.core.logging.loggerfactory import LoggerFactory


class Console:
    """Console interface.

    This class is the interface allowing to run the engine using the command line.
    It parse arguments, initialize logging facilities and start the engine.
    """

    def _parseArgs(self) -> Any:
        parser = argparse.ArgumentParser()
        parser.prog = "pycodeanalyzer"
        parser.add_argument(
            "--config",
            default=None,
            required=False,
            help="Configuration file to be used",
            dest="configfile",
        )
        parser.add_argument(
            "--create-config",
            default=None,
            required=False,
            help="Create a configuration file template. Should be used alone.",
            dest="templatefile",
        )
        parser.add_argument(
            "--log",
            default="INFO",
            choices=["CRITICAL", "ERROR", "WARNING", "INFO", "DEBUG"],
            required=False,
            help="Log level to be used",
            dest="loglevel",
        )
        parser.add_argument(
            "--exportDiagrams",
            default=None,
            required=False,
            help="Export all class diagrams to the path specified",
            dest="exportPath",
        )
        parser.add_argument(
            "--exportFormat",
            default="mermaid",
            required=False,
            choices=["mermaid", "plantuml"],
            help="Format to be used for exported class diagrams",
            dest="exportFormat",
        )
        parser.add_argument(
            "--dumpobj",
            required=False,
            help="Serialize objets found, mainly for test purpose",
            dest="dumpobj",
            action="store_true",
        )
        parser.add_argument(
            "--no-ui",
            required=False,
            help="Discard UI,  mainly for test purpose",
            dest="no_ui",
            action="store_true",
        )
        parser.add_argument(
            "path", nargs="*", help="Path of a root directory to be analysed"
        )
        return parser.parse_args()

    def init(self) -> None:
        """Initialize the console.

        This need to be called before run.
        """

        self.args = self._parseArgs()
        LoggerFactory.init()
        LoggerFactory.setLoggerLevel(self.args.loglevel)

    def run(self, engine: Engine) -> None:
        """Start the engine.

        Start the engine with all the parsed arguments.
        """
        engine.run(self.args)
