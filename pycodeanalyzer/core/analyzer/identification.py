import os
from typing import Any, Dict, List, Optional, cast

from pycodeanalyzer.core.abstraction.objects import (
    AbstractClass,
    AbstractClassClassifier,
    AbstractEnum,
    AbstractFunction,
    AbstractObject,
)


class IdentityAnalyser:
    """Identity analyzer

    This analyzer store all objects and allow to access them or the global trees.
    """

    def __init__(self) -> None:
        self.mapping: Dict[str, List[Any]] = {}
        self.mapping["Classes"] = []
        self.mapping["Enums"] = []
        self.mapping["Functions"] = []
        self.commonFilePath = "/"

    def analyze(self, objects: List[AbstractObject]) -> None:
        for object in objects:
            if object.type == "Class":
                self.mapping["Classes"].append(cast(AbstractClass, object))
            elif object.type == "Enum":
                self.mapping["Enums"].append(cast(AbstractEnum, object))
            elif object.type == "Function":
                self.mapping["Functions"].append(cast(AbstractFunction, object))
        self.analyzeClassifications()

    def analyzeClassifications(self) -> None:
        for klass in self.getClasses():
            if len(klass.methodes) == 0:
                klass.addClassifier(AbstractClassClassifier.Data)
            for parent in klass.parents:
                if "protobuf" in parent[0]:
                    klass.addClassifier(AbstractClassClassifier.Message)
                    break

    def getClasses(self) -> List[AbstractClass]:
        return self.mapping["Classes"]

    def getEnums(self) -> List[AbstractEnum]:
        return self.mapping["Enums"]

    def getFunctions(self) -> List[AbstractFunction]:
        return self.mapping["Functions"]

    def getClasseTree(self) -> Dict[str, Any]:
        tree: Dict[str, Any] = {}
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

    def getEnumTree(self) -> Dict[str, Any]:
        tree: Dict[str, Any] = {}
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

    def getFunctionTree(self) -> Dict[str, Any]:
        tree: Dict[str, Any] = {}
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

    def getFiles(self) -> List[str]:
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

    def getFileTree(self) -> Dict[str, Any]:
        files = self.getFiles()
        tree: Dict[str, Any] = {}
        if len(files) == 0:
            return tree
        self.commonFilePath = os.path.commonpath(files)
        if len(files) == 1:
            self.commonFilePath = os.path.abspath(
                os.path.join(self.commonFilePath, os.pardir)
            )
        currentTree = tree
        for file in files:
            currentTree = tree
            fileRelPath = file[len(self.commonFilePath) + 1 :]
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

    def getClass(self, classNamespacePath: str) -> Optional[AbstractClass]:
        for klass in self.getClasses():
            klassPath = klass.name
            if len(klass.namespace) > 0:
                klassPath = klass.namespace + "::" + klass.name
            if classNamespacePath == klassPath:
                return klass
        return None

    def getEnum(self, enumNamespacePath: str) -> Optional[AbstractEnum]:
        for enum in self.getEnums():
            enumPath = enum.name
            if len(enum.namespace) > 0:
                enumPath = enum.namespace + "::" + enum.name
            if enumNamespacePath == enumPath:
                return enum
        return None

    def getFunction(self, funcFullDef: str) -> Optional[AbstractFunction]:
        for func in self.getFunctions():
            if funcFullDef == func.getFullDef():
                return func
        return None

    def getObjectInFile(self, file: str) -> Dict[str, List[str]]:
        ret: Dict[str, List[str]] = {}
        if len(self.getClasses()) > 0:
            ret["classes"] = []
            for klass in self.getClasses():
                if klass.origin == file:
                    ret["classes"].append(klass.getFullName())
        if len(self.getEnums()) > 0:
            ret["enums"] = []
            for enum in self.getEnums():
                if enum.origin == file:
                    ret["enums"].append(enum.getFullName())
        if len(self.getFunctions()) > 0:
            ret["functions"] = []
            for func in self.getFunctions():
                if func.origin == file:
                    ret["functions"].append(func.getFullDef())
        return ret
