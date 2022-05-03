"""Mermaid.js diagram language

This module allow to create mermaid.js class diagram from abstractions.
"""

from typing import Dict, List, Tuple

from pycodeanalyzer.core.abstraction.objects import (
    AbstractClass,
    AbstractEnum,
    AbstractFunction,
    AbstractObject,
)
from pycodeanalyzer.core.diagrams.iclassdiagrambuild import IClassDiagramBuild


class PieCharBuild:
    """Mermaid.js pie char builder"""

    def __init__(self) -> None:
        self.reset()

    def reset(self) -> None:
        self.categories: Dict[str, int] = {}

    def addValue(self, label: str, value: int) -> None:
        self.categories[label] = value

    def build(self, title: str) -> str:
        res = "pie title " + title + "\n"
        for label, value in self.categories.items():
            res += '"' + label + '" : ' + str(value) + "\n"
        return res


class ClassDiagramBuild(IClassDiagramBuild):
    """Mermaid.js class diagram builder"""

    def __init__(self) -> None:
        super().__init__(__name__)
        self.reset()

    def reset(self) -> None:
        self.klasses: List[AbstractClass] = []
        self.enums: List[AbstractEnum] = []
        self.relations: List[Tuple[str, str]] = []
        self.parents: List[Tuple[str, str]] = []
        self.target: AbstractObject = None

    def createClass(
        self,
        target: AbstractClass,
        linkedClasses: List[AbstractClass],
        linkedEnums: List[AbstractEnum],
        linkedFunctions: List[AbstractFunction],
    ) -> None:
        self.target = target
        self.__addClass(target)
        for klass in linkedClasses:
            self.__addClass(klass)
            if target.isParent(klass):
                self.__addInheritance(target, klass)
            else:
                self.__addDependancy(target, klass)
        for enum in linkedEnums:
            self.__addEnum(enum)
            self.__addDependancy(target, enum)

    def createEnum(self, target: AbstractEnum) -> None:
        self.target = target
        self.__addEnum(target)

    def build(self) -> str:
        res = "classDiagram\n"
        for klass in self.klasses:
            res += "class " + klass.name
            if not klass.origin:
                res += "\n<<" + klass.getMainClassifier() + ">> " + klass.name + "\n"
                continue
            res += " {\n"
            res += "<<" + klass.getMainClassifier() + ">>\n"
            for member in klass.members:
                res += (
                    self.__getVisibilityMark(member[2])
                    + " "
                    + (self.__getTypeString(member[0]) + " " + member[1] + "\n")
                )
            for method in klass.methodes:
                paramstr = ""
                for param in method[2]:
                    paramstr += self.__getTypeString(param[0]) + " " + param[1] + ", "
                res += (
                    self.__getVisibilityMark(method[3])
                    + method[1]
                    + "("
                    + paramstr[:-2]
                    + ") "
                    + self.__getTypeString(method[0])
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

    def __addInheritance(
        self, target: AbstractClass, linkedObject: AbstractObject
    ) -> None:
        relation = (target.name, linkedObject.name)
        if relation not in self.parents:
            self.parents.append(relation)

    def __addDependancy(
        self, target: AbstractObject, linkedObject: AbstractObject
    ) -> None:
        relation = (target.name, linkedObject.name)
        if relation not in self.relations:
            self.relations.append(relation)

    def __addClass(self, abstractClass: AbstractClass) -> None:
        if abstractClass not in self.klasses:
            self.klasses.append(abstractClass)

    def __addEnum(self, abstractEnum: AbstractEnum) -> None:
        if abstractEnum not in self.enums:
            self.enums.append(abstractEnum)

    def __getVisibilityMark(self, text: str) -> str:
        if text == "private":
            return "-"
        if text == "protected":
            return "#"
        return "+"

    def __getTypeString(self, type: str) -> str:
        res = type
        if type.count("<") >= 2:
            # Mermaid does'nt support nested ~ so we do a workaround
            res = res.replace("<", "&lt;").replace(">", "&gt;")
        else:
            res = res.replace("<", "~").replace(">", "~")
        res = res.replace("(", "&#40").replace(")", "&#41")
        res = res.strip()
        return res
