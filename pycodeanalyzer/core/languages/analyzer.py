from typing import List

from pycodeanalyzer.core.abstraction.objects import AbstractObject
from pycodeanalyzer.core.logging.loggerfactory import LoggerFactory


class Analyzer:
    def __init__(self) -> None:
        self.logger = LoggerFactory.createLogger(__name__)

    def analyze(self, rootDir: str, path: str) -> List[AbstractObject]:
        self.logger.error("Use of abstract method : analyze from Analyzer class")
        return []
