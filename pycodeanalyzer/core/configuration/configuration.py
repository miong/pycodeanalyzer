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
        self.logger.debug("Reding configuration file %s", path)
        if self.config.read(path) != [path]:
            self.logger.error("Fail to read configuration.")
            return False
        return True

    def defineConfig(self, section: str, name: str, comment: str) -> None:
        """Define a configuration.

        This function allow to define a configuration. This is used for template generation.
        """
        if section not in self.definition.keys():
            self.definition[section] = []
        self.definition[section].append((name, comment))

    def generateTemplate(self, path: str) -> None:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w") as configFile:
            for section in self.definition.keys():
                configFile.write("[" + section + "]")
                for config in self.definition[section]:
                    configFile.write("# " + config[1])
                    configFile.write("# " + config[0] + "= ")
