"""PlantUML diagram language

This module allow to create PlantUML class diagram from abstractions.
"""

from typing import List, Tuple

from pycodeanalyzer.core.abstraction.objects import (
    AbstractClass,
    AbstractEnum,
    AbstractFunction,
    AbstractObject,
)
from pycodeanalyzer.core.diagrams.iclassdiagrambuild import IClassDiagramBuild


class PlantUMLClassDiagramBuild(IClassDiagramBuild):
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
        res = "@startuml\n"
        for klass in self.klasses:
            res += "class " + klass.name
            res += " <<" + klass.getMainClassifier() + ">>\n"
            if not klass.origin:
                continue
            res += "{\n"
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
                    + self.__getTypeString(method[0])
                    + " "
                    + method[1]
                    + "("
                    + paramstr[:-2]
                    + ")\n"
                )
            res += "}\n"
        for enum in self.enums:
            res += "enum " + enum.name
            if not enum.origin:
                res += " <<External>>\n"
                continue
            res += " <<Enum>>\n"
            res += "{\n"
            for value in enum.values:
                res += value + "\n"
            res += "}\n"
        for relation in self.parents:
            res += relation[0] + " --|> " + relation[1] + "\n"
        for relation in self.relations:
            res += relation[0] + " ..|> " + relation[1] + "\n"
        res += "@enduml\n"
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
        res = res.strip()
        return res
