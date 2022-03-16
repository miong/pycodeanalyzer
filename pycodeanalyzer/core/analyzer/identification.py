import os


class IdentityAnalyser:
    def __init__(self):
        self.mapping = {}
        self.mapping["Classes"] = []
        self.mapping["Enums"] = []
        self.mapping["Functions"] = []

    def analyze(self, objects):
        for object in objects:
            if object.type == "Class":
                self.mapping["Classes"].append(object)
            elif object.type == "Enum":
                self.mapping["Enums"].append(object)
            elif object.type == "Function":
                self.mapping["Functions"].append(object)

    def getClasses(self):
        return self.mapping["Classes"]

    def getEnums(self):
        return self.mapping["Enums"]

    def getFunctions(self):
        return self.mapping["Functions"]

    def getClasseTree(self):
        tree = {}
        currentTree = None
        for klass in self.getClasses():
            klassName = klass.name.replace("::", "££")
            klassPath = klass.namespace + "::" + klassName
            pathElements = klassPath.split("::")
            currentTree = tree
            for element in pathElements:
                if len(element) == 0:
                    continue
                if pathElements.index(element) < len(pathElements) - 1:
                    if element not in currentTree.keys():
                        currentTree[element] = {}
                    currentTree = currentTree[element]
                else:
                    if "__classes__" not in currentTree.keys():
                        currentTree["__classes__"] = []
                    currentTree["__classes__"].append(element.replace("££", "::"))
        return tree

    def getEnumTree(self):
        tree = {}
        currentTree = None
        for enum in self.getEnums():
            enumName = enum.name.replace("::", "££")
            enumPath = enum.namespace + "::" + enumName
            pathElements = enumPath.split("::")
            currentTree = tree
            for element in pathElements:
                if len(element) == 0:
                    continue
                if pathElements.index(element) < len(pathElements) - 1:
                    if element not in currentTree.keys():
                        currentTree[element] = {}
                    currentTree = currentTree[element]
                else:
                    if "__enums__" not in currentTree.keys():
                        currentTree["__enums__"] = []
                    currentTree["__enums__"].append(element.replace("££", "::"))
        return tree

    def getFunctionTree(self):
        tree = {}
        currentTree = None
        for func in self.getFunctions():
            funcName = func.name.replace("::", "££")
            funcPath = func.namespace + "::" + funcName
            pathElements = funcPath.split("::")
            currentTree = tree
            for element in pathElements:
                if len(element) == 0:
                    continue
                if pathElements.index(element) < len(pathElements) - 1:
                    if element not in currentTree.keys():
                        currentTree[element] = {}
                    currentTree = currentTree[element]
                else:
                    if "__functions__" not in currentTree.keys():
                        currentTree["__functions__"] = []
                    elementValue = element.replace("££", "::")
                    data = {}
                    data["name"] = elementValue
                    data["fullDef"] = func.getFullDef()
                    currentTree["__functions__"].append(data)
        return tree

    def getFiles(self):
        files = []
        for item in self.getClasses():
            if item.origin not in files:
                files.append(item.origin)
        for item in self.getEnums():
            if item.origin not in files:
                files.append(item.origin)
        for item in self.getFunctions():
            if item.origin not in files:
                files.append(item.origin)
        return files

    def getFileTree(self):
        files = self.getFiles()
        tree = {}
        self.commonFilePath = os.path.commonpath(files)
        self.singleFile = len(files) == 1
        if self.singleFile:
            self.commonFilePath = os.path.abspath(
                os.path.join(self.commonFilePath, os.pardir)
            )
        currentTree = tree
        for file in files:
            currentTree = tree
            fileRelPath = file[len(self.commonFilePath)+1:]
            elements = fileRelPath.split("/")
            for element in elements:
                if fileRelPath.index(element) < len(fileRelPath) - 1 - len(element):
                    if element not in currentTree.keys():
                        currentTree[element] = {}
                    currentTree = currentTree[element]
                else:
                    if "__files__" not in currentTree.keys():
                        currentTree["__files__"] = []
                    currentTree["__files__"].append(element)
        return tree

    def getClass(self, classNamespacePath):
        for klass in self.getClasses():
            klassPath = klass.name
            if len(klass.namespace) > 0:
                klassPath = klass.namespace + "::" + klass.name
            if classNamespacePath == klassPath:
                return klass
        return None

    def getEnum(self, enumNamespacePath):
        for enum in self.getEnums():
            enumPath = enum.name
            if len(enum.namespace) > 0:
                enumPath = enum.namespace + "::" + enum.name
            if enumNamespacePath == enumPath:
                return enum
        return None

    def getFunction(self, funcFullDef):
        for func in self.getFunctions():
            if funcFullDef == func.getFullDef():
                return func
        return None

    def getObjectInFile(self, file):
        ret = {}
        if len(self.getClasses()) > 0:
            ret["classes"] = []
            for item in self.getClasses():
                if item.origin == file:
                    ret["classes"].append(item.getFullName())
        if len(self.getEnums()) > 0:
            ret["enums"] = []
            for item in self.getEnums():
                if item.origin == file:
                    ret["enums"].append(item.getFullName())
        if len(self.getFunctions()) > 0:
            ret["functions"] = []
            for item in self.getFunctions():
                if item.origin == file:
                    ret["functions"].append(item.getFullDef())
        return ret
