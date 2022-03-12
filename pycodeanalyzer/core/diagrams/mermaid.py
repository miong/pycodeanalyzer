class ClassDiagramBuild:
    def __init__(self):
        self.reset()

    def reset(self):
        self.klasses = []
        self.relation = []

    def create(self, target, linkedClasses, linkedEnums, linkedFunctions):
        self.addClass(target)
        for klass in linkedClasses:
            self.addClass(klass)

    def build(self):
        res = "classDiagram\n"
        for klass in self.klasses:
            res += "class " + klass.name + " {\n"
            res += "<<class>>\n"
            for member in klass.members:
                res += (
                    member[0].replace("<", "~").replace(">", "~").replace(" ", "")
                    + " "
                    + member[1]
                    + "\n"
                )
            for method in klass.methodes:
                paramstr = ""
                for param in method[2]:
                    paramstr += param[0] + " " + param[1] + ", "
                res += method[1] + "(" + paramstr[:-2] + ") " + method[0] + "\n"
            res += "}\n"
        print(res)
        return res

    def addClass(self, abstractClass):
        if abstractClass not in self.klasses:
            self.klasses.append(abstractClass)

    def printGraph(self):
        print("TODO")
