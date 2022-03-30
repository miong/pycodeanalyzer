import configparser
import os
from typing import Dict, List, Tuple

from injector import singleton

from pycodeanalyzer.core.logging.loggerfactory import LoggerFactory


@singleton
class Configuration:
    """Configuration of pycodeanalyzer.

    This class allow to parse and use configuration with a INI format.
    """

    def __init__(self) -> None:
        self.logger = LoggerFactory.createLogger(__name__)
        self.config = configparser.ConfigParser()
        self.definition: Dict[str, List[Tuple[str, str]]] = {}

    def load(self, path: str) -> bool:
        """Load configuration file.

        Read and load the configuration from a INI config file.
        """
        try:
            self.logger.debug("Reding configuration file %s", path)
            if self.config.read(path) != [path]:
                self.logger.error("Fail to read configuration.")
                return False
            return True
        except configparser.Error:
            self.logger.error("Fail to read configuration.")
            return False

    def defineConfig(self, section: str, name: str, comment: str) -> None:
        """Define a configuration.

        This function allow to define a configuration. This is used for template generation.
        """
        if section not in self.definition.keys():
            self.definition[section] = []
        self.definition[section].append((name, comment))

    def get(self, section: str, name: str) -> str:
        """Get value from configuation"""

        try:
            return self.config.get(section, name)
        except configparser.Error:
            return None

    def generateTemplate(self, path: str) -> None:
        """Generate configuration template."""

        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w") as configFile:
            for section in self.definition.keys():
                configFile.write("[" + section + "]\n")
                for config in self.definition[section]:
                    configFile.write("# " + config[1] + "\n")
                    configFile.write("# " + config[0] + "= \n")
