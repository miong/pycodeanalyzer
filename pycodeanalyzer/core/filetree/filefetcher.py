import os
import pathlib
from typing import Dict, List

from injector import inject, singleton

from pycodeanalyzer.core.configuration.configuration import Configuration
from pycodeanalyzer.core.encoding.encodings import Encoding
from pycodeanalyzer.core.languages.extensions import languageExtensions
from pycodeanalyzer.core.logging.loggerfactory import LoggerFactory


@singleton
class FileFetcher:
    """File fetcher.

    Class allowing to fetch all supported file from a root directory.
    """

    @inject
    def __init__(self, configuration: Configuration) -> None:
        self.logger = LoggerFactory.createLogger(__name__)
        self.suported_extensions: List[str] = list(languageExtensions.keys())
        self.rejected_encoding = [
            "unknown-8bit",
            "binary",
        ]
        self.encoding = Encoding()
        self.configured = False
        self.configuration = configuration
        self.ignoredPatterns: List[str] = []
        self.languagesCount: Dict[str, int] = {}
        self.defineConfig()

    def reset(self) -> None:
        self.languagesCount = {}

    def isAnalyzed(self, fileabspath: str) -> bool:
        p = pathlib.Path(fileabspath)
        extension = p.suffix
        filename = p.stem

        encoding = self.encoding.getFileEncoding(fileabspath)

        ignored = False
        for pattern in self.ignoredPatterns:
            ignored = p.match(pattern)
            if ignored:
                self.logger.info("Ignore file due to excludes config : %s", fileabspath)
                break
        isAnalyzedValue = (
            encoding not in self.rejected_encoding
            and extension in self.suported_extensions
            and not filename.startswith(".")
            and not ignored
        )
        if isAnalyzedValue:
            language = None
            if extension in languageExtensions.keys():
                language = languageExtensions[extension]
            if language:
                if language in self.languagesCount.keys():
                    self.languagesCount[language] = self.languagesCount[language] + 1
                else:
                    self.languagesCount[language] = 1
        return isAnalyzedValue

    def fetch(self, rootDir: str) -> List[str]:
        if not self.configured:
            self.handleConfigation()
            self.configured = True
        list: List[str] = []
        rootabspath = os.path.abspath(rootDir)
        if not os.path.isdir(rootabspath):
            self.logger.error("There is no directory %s", rootabspath)
            return list
        self.logger.debug("start fetching files from : %s", rootabspath)
        for path, subdirs, files in os.walk(rootabspath):
            for file in files:
                fileabspath = os.path.join(rootabspath, path, file)
                filepath = os.path.join(path, file)
                if os.path.isfile(fileabspath) and self.isAnalyzed(fileabspath):
                    self.logger.debug("adding file for analysis : %s", filepath)
                    list.append(filepath)
        self.logger.debug("end fetching files")
        return list

    def defineConfig(self) -> None:
        self.configuration.defineConfig(
            "Analysis.Files",
            "excludes",
            "List of Glob expression (python) to exclude file. Used on file paths :"
            ' Example : ["**/not_parsed.h","/toto/titi/file.h", "**/*toto[1-9]*.not"]',
        )

    def handleConfigation(self) -> None:
        ignoredPatterns_val = self.configuration.getList("Analysis.Files", "excludes")
        self.ignoredPatterns = ignoredPatterns_val if ignoredPatterns_val else []
