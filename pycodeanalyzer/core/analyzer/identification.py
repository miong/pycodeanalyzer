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
                    if not element in currentTree.keys():
                        currentTree[element] = {}
                    currentTree = currentTree[element]
                else:
                    if not "__classes__" in currentTree.keys():
                        currentTree["__classes__"] = []
                    currentTree["__classes__"].append(element.replace("££", "::"))
        return tree

    def getClass(self, classNamespacePath):
        for klass in self.getClasses():
            klassPath = klass.name
            if len(klass.namespace) > 0:
                klassPath = klass.namespace + "::" + klass.name
            if classNamespacePath == klassPath:
                return klass
        return None
