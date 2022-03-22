import os
import pathlib
from typing import List

from injector import singleton

from pycodeanalyzer.core.encoding.encodings import Encoding
from pycodeanalyzer.core.logging.loggerfactory import LoggerFactory


@singleton
class FileFetcher:
    def __init__(self) -> None:
        self.logger = LoggerFactory.createLogger(__name__)
        self.suported_extensions = [
            ".h",
            ".hpp",
            ".py",
        ]
        self.rejected_encoding = [
            "unknown-8bit",
            "binary",
        ]
        self.encoding = Encoding()

    def isAnalyzed(self, fileabspath: str) -> bool:
        p = pathlib.Path(fileabspath)
        extension = p.suffix
        filename = p.stem

        encoding = self.encoding.getFileEncoding(fileabspath)

        return (
            encoding not in self.rejected_encoding
            and extension in self.suported_extensions
            and not filename.startswith(".")
        )

    def fetch(self, rootDir: str) -> List[str]:
        list: List[str] = []
        rootabspath = os.path.abspath(rootDir)
        if not os.path.isdir(rootabspath):
            self.logger.error("There is no directory %s", rootDir)
            return list
        self.logger.debug("start fetching files from : %s", rootDir)
        for path, subdirs, files in os.walk(rootabspath):
            for file in files:
                fileabspath = os.path.join(rootabspath, path, file)
                filepath = os.path.join(path, file)
                if os.path.isfile(fileabspath) and self.isAnalyzed(fileabspath):
                    self.logger.debug("adding file for analysis : %s", filepath)
                    list.append(filepath)
        self.logger.debug("end fetching files")
        return list
