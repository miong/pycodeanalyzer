from typing import List

from pycodeanalyzer.core.abstraction.objects import AbstractObject
from pycodeanalyzer.core.logging.loggerfactory import LoggerFactory


class Analyzer:
    """Base class for language analyzer."""

    def __init__(self, name: str) -> None:
        self.logger = LoggerFactory.createLogger(name)

    def analyze(self, rootDir: str, path: str) -> List[AbstractObject]:
        self.logger.error("Use of abstract method : analyze from Analyzer class")
        raise NotImplementedError(
            "A subclass should be defined and implement this interface"
        )
