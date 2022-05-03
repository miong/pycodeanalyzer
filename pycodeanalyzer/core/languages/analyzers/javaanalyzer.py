from typing import Any, List, Union

import javalang

from pycodeanalyzer.core.abstraction.objects import (
    AbstractClass,
    AbstractEnum,
    AbstractObject,
    AbstractObjectLanguage,
)
from pycodeanalyzer.core.languages.analyzer import Analyzer


class JavaAnalyzer(Analyzer):
    def __init__(self) -> None:
        super().__init__(__name__)
        self.globalImports: List[str] = []

    def analyze(self, rootDir: str, path: str) -> List[AbstractObject]:
        abstractObjects: List[AbstractObject] = []
        self.logger.info("Analysing %s", path)
        content: str = ""
        with open(path, "r") as srcFile:
            content = srcFile.read()
        try:
            tree = javalang.parse.parse(content)
        except javalang.parser.JavaParserBaseException:
            self.logger.error("Can't parse %s", path)
            return abstractObjects

        # Handle imports
        self.globalImports = []
        for item in tree.imports:
            importNS = item.path.replace(".", "::")
            if not item.wildcard:
                importNS = importNS[: importNS.rindex("::")]
            self.globalImports.append(importNS)

        # handle package
        currentNS = ""
        if tree.package:
            currentNS = tree.package.name.replace(".", "::")

        # handle types
        for item in tree.types:
            if isinstance(item, javalang.tree.ClassDeclaration) or isinstance(
                item, javalang.tree.InterfaceDeclaration
            ):
                self.handleClass(abstractObjects, path, currentNS, item)
            elif isinstance(item, javalang.tree.EnumDeclaration):
                self.handleEnum(abstractObjects, path, currentNS, item)
        return abstractObjects

    def handleClass(
        self,
        abstractObjects: List[AbstractObject],
        path: str,
        currentNS: str,
        klass: Union[
            javalang.tree.ClassDeclaration, javalang.tree.InterfaceDeclaration
        ],
    ) -> None:
        abstraction = AbstractClass(klass.name, currentNS, path)
        for ns in self.globalImports:
            abstraction.addUsingNamespace(ns)
        if klass.type_parameters:
            for genType in klass.type_parameters:
                abstraction.addGenericType(str(genType.name).strip())
        if klass.extends:
            self.handleParent(klass.extends, abstraction)
        if isinstance(klass, javalang.tree.ClassDeclaration):
            if klass.implements:
                for item in klass.implements:
                    self.handleParent(item, abstraction)
        for item in klass.body:
            if isinstance(item, javalang.tree.ClassDeclaration):
                self.handleClass(
                    abstractObjects, path, currentNS + "::" + klass.name, item
                )
            elif isinstance(item, javalang.tree.EnumDeclaration):
                self.handleEnum(
                    abstractObjects, path, currentNS + "::" + klass.name, item
                )
            elif isinstance(item, javalang.tree.FieldDeclaration) or isinstance(
                item, javalang.tree.ConstantDeclaration
            ):
                type = self.deduceType(item.type)
                visibility = self.deduceVisibility(item)
                for decl in item.declarators:
                    name = decl.name
                    abstraction.addMember(type, name, visibility)
            elif isinstance(item, javalang.tree.MethodDeclaration):
                rtype = "void"
                if item.return_type:
                    rtype = self.deduceType(item.return_type)
                visibility = self.deduceVisibility(item)
                params = []
                for param in item.parameters:
                    paramName = param.name
                    paramType = self.deduceType(param.type)
                    params.append((paramType, paramName))
                abstraction.addMethod(rtype, item.name, params, visibility)
                if item.type_parameters:
                    for genType in item.type_parameters:
                        abstraction.addGenericType(str(genType.name).strip())
            elif isinstance(item, javalang.tree.ConstructorDeclaration):
                visibility = self.deduceVisibility(item)
                params = []
                for param in item.parameters:
                    paramName = param.name
                    paramType = self.deduceType(param.type)
                    params.append((paramType, paramName))
                abstraction.addMethod(klass.name, item.name, params, visibility)
        abstraction.objectLanguage = AbstractObjectLanguage.Java
        abstractObjects.append(abstraction)

    def handleEnum(
        self,
        abstractObjects: List[AbstractObject],
        path: str,
        currentNS: str,
        enum: javalang.tree.EnumDeclaration,
    ) -> None:
        values: List[str] = []
        for item in enum.body.constants:
            values.append(item.name)
        abstraction = AbstractEnum(enum.name, currentNS, path, values)
        abstraction.objectLanguage = AbstractObjectLanguage.Java
        abstractObjects.append(abstraction)

    def handleParent(self, item: Any, klass: AbstractClass) -> None:
        parentName = item.name
        subtype = item.sub_type
        while subtype:
            parentName = parentName + "::" + subtype.name
            subtype = subtype.sub_type
        parentSimpleName = parentName
        if "::" in parentName:
            parentSimpleName = parentName[parentName.rindex("::") + 2 :]
        klass.addParent(parentName, parentSimpleName, "public")

    def deduceVisibility(self, item: Any) -> str:
        visibility = "public"
        if "private" in item.modifiers:
            visibility = "private"
        if "protected" in item.modifiers:
            visibility = "protected"
        return visibility

    def deduceType(self, item: Any) -> str:
        typeName = item.name
        dimention = item.dimensions
        if not isinstance(item, javalang.tree.BasicType):
            subtype = item.sub_type
            while subtype:
                typeName = typeName + "::" + subtype.name
                dimention = subtype.dimensions
                subtype = subtype.sub_type
        if dimention:
            for i in range(0, len(dimention)):
                typeName = typeName + "[]"
        return typeName
