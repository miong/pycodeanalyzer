import re
from threading import Thread
from typing import Dict, List, Tuple


class SearchAnalyser:
    """Search analyser

    This class allow to search tokens with context in each parsed source file.
    """

    def searchInAllFiles(self, token: str, files: List[str]) -> List[Tuple[str, str]]:
        self.results: List[Tuple[str, str]] = []
        self.threads: List[Thread] = []
        for file in files:
            thread = Thread(target=self.__seachInFileThreaded, args=(token, file))
            self.threads.append(thread)
            thread.start()
        for thread in self.threads:
            thread.join()
        return self.results

    def seachInFile(self, token: str, filePath: str) -> List[Tuple[str, str]]:
        res: List[Tuple[str, str]] = []
        with open(filePath, "r") as file:
            text = file.read().splitlines()
            enumeration: Dict[int, str] = dict(
                (i, j + "\n") for i, j in enumerate(text)
            )
            for linenb, line in enumeration.items():
                if re.search(token.lower(), line.lower()):
                    context = ""
                    for i in range(-3, 3):
                        if linenb + i >= 0 and linenb + i < len(enumeration):
                            context += enumeration[linenb + i]
                    res.append((filePath, context))
        return res

    def __seachInFileThreaded(self, token: str, filePath: str) -> None:
        self.results.extend(self.seachInFile(token, filePath))
