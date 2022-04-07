from typing import List

from pycodeanalyzer.core.abstraction.objects import AbstractObject
from pycodeanalyzer.core.languages.analyzer import Analyzer

# import kopyt


class KotlinAnalyzer(Analyzer):
    def __init__(self) -> None:
        super().__init__(__name__)

    def analyze(self, rootDir: str, path: str) -> List[AbstractObject]:
        abstractObjects: List[AbstractObject] = []
        self.logger.info("Analysing %s", path)
        return abstractObjects
