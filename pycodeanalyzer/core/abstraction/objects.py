""" Object abstraction.

This modules containes all the abstraction for code object manipulated by pycodeanalyzer
"""

from __future__ import annotations

import re
from enum import IntEnum
from typing import Any, Dict, List, Tuple


class AbstractObjectLanguage(IntEnum):
    """Language of the code source

    Enum representing supported languages
    """

    Unknown = 0
    CPP = 1
    Python = 2
    Java = 3
    Kotlin = 4


class AbstractObject:
    """Base of all abstraction"""

    def __init__(self, name: str, origin: str) -> None:
        self.name = name
        self.type = "Object"
        self.origin: str = None if not origin else origin.replace("\\", "/")
        self.usingNS: List[str] = []
        self.objectLanguage: AbstractObjectLanguage = AbstractObjectLanguage.Unknown
        self.linkedGenericTypes: List[str] = None

    def addUsingNamespace(self, namespace: str) -> None:
        self.usingNS.append(namespace)


class AbstractEnum(AbstractObject):
    """Enum abstraction"""

    def __init__(
        self, name: str, namespace: str, origin: str, values: List[str]
    ) -> None:
        super().__init__(name, origin)
        self.namespace = namespace
        self.type = "Enum"
        self.values = values

    def getFullName(self) -> str:
        if len(self.namespace) <= 0:
            return self.name
        return self.namespace + "::" + self.name

    def print(self) -> None:
        print("Enum : ", self.name)
        print("\tValues : ")
        for value in self.values:
            print("\t\t * ", value)


class AbstractFunction(AbstractObject):
    """Function abstraction"""

    def __init__(
        self,
        name: str,
        origin: str,
        returnType: str,
        parameters: List[Tuple[str, str]],
        namespace: str,
        doxygen: str,
    ) -> None:
        super().__init__(name, origin)
        self.namespace = namespace
        self.type = "Function"
        self.returnType = returnType
        self.parameters = parameters
        self.doxygen = doxygen
        self.linkedGenericTypes: List[str] = []

    def addGenericType(self, genType: str) -> None:
        self.linkedGenericTypes.append(genType)

    def print(self) -> None:
        print("Function : ", self.name)
        print("\tNamespace :", self.namespace)
        print("\tReturn :", self.returnType)
        print("\tParams :")
        for param in self.parameters:
            print("\t\t -", param[0], param[1])

    def getFullDef(self) -> str:
        ret: str = self.returnType + " " + self.namespace + "::" + self.name + "("
        if len(self.parameters) > 0:
            for param in self.parameters:
                ret += param[0] + " " + param[1] + ", "
            ret = ret[:-2]
        ret += ")"
        return ret


class AbstractClassClassifier(IntEnum):
    """Classifier for class objects

    Enum representing additionnal data
    """

    NoClassifier = 0
    External = 1
    Generic = 2
    Message = 3
    Data = 4


class AbstractClass(AbstractObject):
    """Class abstraction"""

    NonObjectTypes: Dict[AbstractObjectLanguage, List[str]] = {
        AbstractObjectLanguage.Unknown: [],
        AbstractObjectLanguage.CPP: [
            "void",
            "bool",
            "unsigned",
            "char",
            "unsigned char",
            "short",
            "unsigned short",
            "int",
            "unsigned int",
            "long",
            "unsigned long",
            "long long",
            "unsigned long long",
            "float",
            "double",
            "int8_t",
            "int16_t",
            "int32_t",
            "int64_t",
            "uint8_t",
            "uint16_t",
            "uint32_t",
            "uint64_t",
            "int8",
            "int16",
            "int32",
            "int64",
            "uint8",
            "uint16",
            "uint32",
            "uint64",
            "size_t",
        ],
        AbstractObjectLanguage.Python: [
            "Any",
            "None",
            "List",
            "Tuple",
            "Dict",
            "str",
            "float",
            "int",
            "long",
            "bool",
        ],
        AbstractObjectLanguage.Java: [
            "void",
            "byte",
            "int",
            "short",
            "long",
            "float",
            "double",
            "boolean",
            "char",
            "String",
            "Object",
            "Integer",
            "Short",
            "Long",
            "Float",
            "Double",
            "Boolean",
            "Byte",
            "Char",
            "Void",
        ],
        AbstractObjectLanguage.Kotlin: [
            "KotlinAuto",
            "Unit",
            "Byte",
            "Short",
            "Int",
            "Long",
            "Float",
            "Double",
            "Boolean",
            "Char",
            "String",
            "Array",
            "Object",
            "Void",
        ],
    }

    def __init__(self, name: str, namespace: str, origin: str) -> None:
        super().__init__(name, origin)
        self.namespace = namespace
        self.type = "Class"
        self.members: List[Tuple[str, str, str]] = []
        self.methodes: List[Tuple[str, str, List[Tuple[str, str]], str]] = []
        self.parents: List[Tuple[str, str, str]] = []
        self.linkedGenericTypes: List[str] = []
        self.classifiers: List[AbstractClassClassifier] = []

    def addGenericType(self, genType: str) -> None:
        self.linkedGenericTypes.append(genType)

    def addMember(self, type: str, name: str, visibility: str) -> None:
        self.members.append((type, name, visibility))

    def hasMember(self, name: str) -> bool:
        for item in self.members:
            if item[1] == name:
                return True
        return False

    def addMethod(
        self,
        returnType: str,
        name: str,
        parameters: List[Tuple[str, str]],
        visibility: str,
    ) -> None:
        self.methodes.append((returnType, name, parameters, visibility))

    def addParent(self, completetype: str, name: str, visibility: str) -> None:
        self.parents.append((completetype, name, visibility))

    def addClassifier(self, classifier: AbstractClassClassifier) -> None:
        if classifier not in self.classifiers:
            self.classifiers.append(classifier)

    def getMainClassifier(self) -> str:
        if AbstractClassClassifier.External in self.classifiers:
            return "External"
        if AbstractClassClassifier.Generic in self.classifiers:
            return "Generic"
        if AbstractClassClassifier.Message in self.classifiers:
            return "Message"
        if AbstractClassClassifier.Data in self.classifiers:
            return "Data"
        return "Class"

    def getLinkedTypes(self) -> List[str]:
        types: List[str] = []
        for parent in self.parents:
            for type in self.__getDependanceFromType(parent[1]):
                if type not in types and self.__isPotentialClassName(type):
                    types.append(type)
            if parent[0] != parent[1]:
                for type in self.__getDependanceFromType(parent[0]):
                    if type not in types and self.__isPotentialClassName(type):
                        types.append(type)
        for method in self.methodes:
            for type in self.__getDependanceFromType(method[0]):
                if (
                    type not in types
                    and type != self.name
                    and self.__isPotentialClassName(type)
                ):
                    types.append(type)
            for param in method[2]:
                for type in self.__getDependanceFromType(param[0]):
                    if type not in types and self.__isPotentialClassName(type):
                        types.append(type)
        for member in self.members:
            for type in self.__getDependanceFromType(member[0]):
                if type not in types and self.__isPotentialClassName(type):
                    types.append(type)
        for genType in self.linkedGenericTypes:
            for type in self.__getDependanceFromType(genType):
                if type not in types and self.__isPotentialClassName(type):
                    types.append(type)
        types = self.__removeNonObjectTypes(types)
        return types

    def __isPotentialClassName(self, type: str) -> bool:
        if not type:
            return False
        if len(type) <= 0:
            return False
        if "(" in type:
            return False
        return True

    def __getDependanceFromType(self, type: str) -> List[str]:
        deps: List[str] = []
        if type.startswith("<anon-"):
            return deps
        if "<" in type:
            templateTypeList = self.__splitTypes(
                re.search("[^<]+<(.*)>", type).group(1)
            )
            for templateType in templateTypeList:
                innerTypes = self.__getDependanceFromType(templateType)
                for dep in innerTypes:
                    if dep not in deps:
                        deps.append(self.__cleanLanguageArtifacts(dep))
            type = re.search("([^<]+).*>", type).group(1)
        deps.append(self.__cleanLanguageArtifacts(type))
        return deps

    def __splitTypes(self, decl: Any) -> List[str]:
        depth = 0
        currentType = ""
        types: List[str] = []
        for i in range(0, len(decl)):
            if decl[i] == "<":
                depth += 1
                currentType += decl[i]
            elif decl[i] == ">":
                depth -= 1
                currentType += decl[i]
            elif decl[i] == ",":
                if depth == 0:
                    types.append(currentType)
                    currentType = ""
                else:
                    currentType += decl[i]
            else:
                currentType += decl[i]
        types.append(currentType)
        return types

    def getFullName(self) -> str:
        if len(self.namespace) <= 0:
            return self.name
        return self.namespace + "::" + self.name

    def __cleanLanguageArtifacts(self, type: str) -> str:
        # remove all languages artefact that are not needed to get the type we depends on
        return (
            type.replace("*", "")
            .replace("&", "")
            .replace("const", "")
            .replace("static", "")
            .replace("...", "")
            .replace("enum", "")
            .replace("struct", "")
            .replace("[", "")
            .replace("]", "")
            .replace("val", "")
            .replace("var", "")
            .replace("?", "")
            .replace("!!", "")
            .strip()
        )

    def __removeNonObjectTypes(self, typeList: List[str]) -> List[str]:
        cleaned_list = [
            x
            for x in typeList
            if x not in AbstractClass.NonObjectTypes[self.objectLanguage]
            and "std::" not in x
        ]
        return cleaned_list

    def isParent(self, klass: AbstractClass) -> bool:
        for tuple in self.parents:
            if tuple[0] == klass.name:
                return True
        return False

    def print(self) -> None:
        print("Class : ", self.name, " in namespace ", self.namespace)
        print("\tInherits : ")
        for tuple in self.parents:
            print("\t\t * {1} {0}".format(tuple[0], tuple[2]))
        print("\tMethods : ")
        for tuple in self.methodes:
            paramStr = ""
            for param in tuple[2]:
                paramStr = paramStr + param[0] + " " + param[1] + ", "
            paramStr = paramStr[:-2]
            print(
                "\t\t * {3} {0} {1} ({2})".format(
                    tuple[0], tuple[1], paramStr, tuple[3]
                )
            )
        print("\tMembers : ")
        for tuple in self.members:
            print("\t\t * {2} {0} {1}".format(tuple[0], tuple[1], tuple[2]))


def platformIndependantPathHash(path: str) -> str:
    return path.replace("\\", "/").replace("/", "").replace("_", "").replace(":", "")


def compareAbstractObject(obj: AbstractObject) -> Tuple[str, str, str]:
    """Comparison operator to sort AbstractObject and subclasses

    This allow to sort by type, origin and name
    """

    return (obj.type, platformIndependantPathHash(obj.origin), obj.name)
