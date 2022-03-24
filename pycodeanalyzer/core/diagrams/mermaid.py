from typing import Any, List, Tuple

from pycodeanalyzer.core.abstraction.objects import (
    AbstractClass,
    AbstractEnum,
    AbstractFunction,
    AbstractObject,
)


class ClassDiagramBuild:
    def __init__(self) -> None:
        self.reset()

    def reset(self) -> None:
        self.klasses: List[AbstractClass] = []
        self.enums: List[AbstractEnum] = []
        self.relations: List[Tuple[str, str]] = []
        self.parents: List[Tuple[str, str]] = []
        self.target: Any = None

    def createClass(
        self,
        target: AbstractClass,
        linkedClasses: List[AbstractClass],
        linkedEnums: List[AbstractEnum],
        linkedFunctions: List[AbstractFunction],
    ) -> None:
        self.target = target
        self.addClass(target)
        for klass in linkedClasses:
            self.addClass(klass)
            if target.isParent(klass):
                self.addInheritance(target, klass)
            else:
                self.addDependancy(target, klass)
        for enum in linkedEnums:
            self.addEnum(enum)
            self.addDependancy(target, enum)

    def createEnum(self, target: AbstractEnum) -> None:
        self.target = target
        self.addEnum(target)

    def build(self) -> str:
        res = "classDiagram\n"
        for klass in self.klasses:
            res += "class " + klass.name
            if not klass.origin:
                res += "\n<<External>> " + klass.name + "\n"
                continue
            res += " {\n"
            res += "<<Class>>\n"
            for member in klass.members:
                res += (
                    self.getVisibilityMark(member[2])
                    + " "
                    + (self.getTypeString(member[0]) + " " + member[1] + "\n")
                )
            for method in klass.methodes:
                paramstr = ""
                for param in method[2]:
                    paramstr += self.getTypeString(param[0]) + " " + param[1] + ", "
                res += (
                    self.getVisibilityMark(method[3])
                    + method[1]
                    + "("
                    + paramstr[:-2]
                    + ") "
                    + self.getTypeString(method[0])
                    + "\n"
                )
            res += "}\n"
            if klass != self.target:
                res += "link " + klass.name + ' "class££' + klass.getFullName() + '"\n'
        for enum in self.enums:
            res += "class " + enum.name
            if not enum.origin:
                res += "\n<<External>> " + enum.name + "\n"
                continue
            res += " {\n"
            res += "<<Enum>>\n"
            for value in enum.values:
                res += "+ " + value + "\n"
            res += "}\n"
            if enum != self.target:
                res += "link " + enum.name + ' "enum££' + enum.getFullName() + '"\n'
        for relation in self.parents:
            res += relation[0] + " --|> " + relation[1] + "\n"
        for relation in self.relations:
            res += relation[0] + " ..> " + relation[1] + "\n"
        return res

    def addInheritance(
        self, target: AbstractClass, linkedObject: AbstractObject
    ) -> None:
        relation = (target.name, linkedObject.name)
        if relation not in self.parents:
            self.parents.append(relation)

    def addDependancy(
        self, target: AbstractObject, linkedObject: AbstractObject
    ) -> None:
        relation = (target.name, linkedObject.name)
        if relation not in self.relations:
            self.relations.append(relation)

    def addClass(self, abstractClass: AbstractClass) -> None:
        if abstractClass not in self.klasses:
            self.klasses.append(abstractClass)

    def addEnum(self, abstractEnum: AbstractEnum) -> None:
        if abstractEnum not in self.enums:
            self.enums.append(abstractEnum)

    def getVisibilityMark(self, text: str) -> str:
        if text == "private":
            return "-"
        if text == "protected":
            return "#"
        return "+"

    def getTypeString(self, type: str) -> str:
        res = type
        if type.count("<") >= 2:
            # Mermaid does'nt support nested ~ so we do a workaround
            res = res.replace("<", "&lt;").replace(">", "&gt;")
        else:
            res = res.replace("<", "~").replace(">", "~")
        res = res.strip()
        return res
