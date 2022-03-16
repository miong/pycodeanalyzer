import re


class SearchAnalyser:
    def seachInFile(self, token, filePath):
        with open(filePath, "r") as file:
            for line in file:
                if re.search(sys.argv[1], line):
                    print(line)
