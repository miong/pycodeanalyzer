import re
from threading import Thread


class SearchAnalyser:
    def searchInAllFiles(self, token, files):
        self.results = []
        self.threads = []
        for file in files:
            thread = Thread(target=self.seachInFileThreaded, args=(token, file))
            self.threads.append(thread)
            thread.start()
        for thread in self.threads:
            thread.join()
        return self.results

    def seachInFile(self, token, filePath):
        res = []
        with open(filePath, "r") as file:
            enumeration = dict((i, j) for i, j in enumerate(file))
            for linenb, line in enumeration.items():
                if re.search(token.lower(), line.lower()):
                    context = ""
                    for i in range(-3, 3):
                        if linenb + i >= 0 and linenb + i < len(enumeration):
                            context += enumeration[linenb + i]
                    res.append((filePath, context))
        return res

    def seachInFileThreaded(self, token, filePath):
        self.results.extend(self.seachInFile(token, filePath))
