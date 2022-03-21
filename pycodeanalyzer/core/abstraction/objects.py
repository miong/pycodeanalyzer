from __future__ import annotations

from typing import List, Tuple
import re


class AbstractObject:
    def __init__(self, name: str, origin: str) -> None:
        self.name = name
        self.type = "Object"
        self.origin = origin


class AbstractEnum(AbstractObject):
    def __init__(self, name: str, namespace: str, origin: str, values: List[str]):
        self.name = name
        self.namespace = namespace
        self.type = "Enum"
        self.values = values
        self.origin = origin

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
    def __init__(
        self,
        name: str,
        origin: str,
        returnType: str,
        parameters: List[Tuple[str, str]],
        namespace: str,
        doxygen: str,
    ) -> None:
        self.name = name
        self.namespace = namespace
        self.type = "Function"
        self.returnType = returnType
        self.origin = origin
        self.parameters = parameters
        self.doxygen = doxygen

    def print(self) -> None:
        print("Function : ", self.name)
        print("\tNamespace :", self.namespace)
        print("\tReturn :", self.returnType)
        print("\tParams :")
        for param in self.parameters:
            print("\t\t -", param[0], param[1])

    def getFullDef(self) -> str:
        ret: str = self.returnType + " " + self.namespace + "::" + self.name + "("
        for param in self.parameters:
            ret += param[0] + " " + param[1] + ", "
        ret = ret[:-2]
        ret += ")"
        return ret


class AbstractClass(AbstractObject):
    def __init__(self, name: str, namespace: str, origin: str) -> None:
        self.name = name
        self.namespace = namespace
        self.type = "Class"
        self.members: List[Tuple[str, str, str]] = []
        self.methodes: List[Tuple[str, str, List[Tuple[str, str]], str]] = []
        self.parents: List[Tuple[str, str, str]] = []
        self.origin = origin

    def addMember(self, type: str, name: str, visibility: str) -> None:
        self.members.append((type, name, visibility))

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
        if "<" in type:
            templateTypeList = self.__splitTypes(re.search('[^<]+<(.*)>', type).group(1))
            for templateType in templateTypeList:
                innerTypes = self.__getDependanceFromType(templateType)
                for dep in innerTypes:
                    if dep not in deps:
                        deps.append(self.__cleanLanguageArtifacts(dep))
            type = re.search('([^<]+).*>', type).group(1)
        deps.append(self.__cleanLanguageArtifacts(type))
        return deps

    def __splitTypes(self, decl):
        depth = 0;
        currentType = ""
        types = []
        for i in range (0, len(decl)):
            if decl[i] == '<':
                depth += 1
                currentType += decl[i]
            elif decl[i] == '>':
                depth -= 1
                currentType += decl[i]
            elif decl[i] == ',':
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
            .strip()
        )

    def removeNonObjectTypes(self, typeList: List[str]) -> List[str]:
        NonObjectTypes = [
            "void",
            "bool",
            "char",
            "unsigned char",
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
        ]
        cleaned_list = [
            x for x in typeList if x not in NonObjectTypes and "std::" not in x
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
