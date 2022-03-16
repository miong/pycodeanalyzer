class ClassDiagramBuild:
    def __init__(self):
        self.reset()

    def reset(self):
        self.klasses = []
        self.enums = []
        self.relations = []
        self.parents = []

    def createClass(self, target, linkedClasses, linkedEnums, linkedFunctions):
        self.addClass(target)
        for klass in linkedClasses:
            self.addClass(klass)
            if target.isParent(klass):
                self.addInheritance(target, klass)
            else:
                self.addDependancy(target, klass)
        for enum in linkedEnums:
            self.addEnum(enum)
            self.addDependancy(target, klass)

    def createEnum(self, target):
        self.addEnum(target)

    def build(self):
        res = "classDiagram\n"
        for klass in self.klasses:
            res += "class " + klass.name
            if not klass.origin:
                res += "\n<<External>> "+klass.name+"\n"
                continue
            res += " {\n"
            res += "<<Class>>\n"
            for member in klass.members:
                res += self.getVisibilityMark(member[2]) +" "+ (
                    member[0].replace("<", "~").replace(">", "~").replace(" ", "")
                    + " "
                    + member[1]
                    + "\n"
                )
            for method in klass.methodes:
                paramstr = ""
                for param in method[2]:
                    paramstr += param[0] + " " + param[1] + ", "
                res += self.getVisibilityMark(method[3]) + method[1] + "(" + paramstr[:-2] + ") " + method[0] + "\n"
            res += "}\n"
            res += "link "+klass.name+" \"class££"+klass.getFullName()+"\"\n"
        for enum in self.enums:
            res += "class " + enum.name
            if not enum.origin:
                res += "\n<<External>> "+klass.name+"\n"
                continue
            res += " {\n"
            res += "<<Enum>>\n"
            for value in enum.values:
                res += "+ "+value+"\n"
            res += "}\n"
            res += "link "+enum.name+" \"enum££"+enum.getFullName()+"\"\n"
        for relation in self.parents:
            res += relation[0]+" --|> "+relation[1]+"\n"
        for relation in self.relations:
            res += relation[0]+" ..> "+relation[1]+"\n"
        print("----------------")
        print(res)
        return res

    def addInheritance(self, target, linkedObject):
        relation = (target.name, linkedObject.name)
        if relation not in self.parents:
            self.parents.append(relation)

    def addDependancy(self, target, linkedObject):
        relation = (target.name,linkedObject.name)
        if relation not in self.relations:
            self.relations.append(relation)

    def addClass(self, abstractClass):
        if abstractClass not in self.klasses:
            self.klasses.append(abstractClass)

    def addEnum(self, abstractEnum):
        if abstractEnum not in self.enums:
            self.enums.append(abstractEnum)

    def getVisibilityMark(self, text):
        if text == "private":
            return '-';
        if text == "protected":
            return '#';
        return '+';
