import re
from typing import Any, List, Tuple, Union

import kopyt

from pycodeanalyzer.core.abstraction.objects import (
    AbstractClass,
    AbstractEnum,
    AbstractFunction,
    AbstractObject,
    AbstractObjectLanguage,
)
from pycodeanalyzer.core.languages.analyzer import Analyzer


class KotlinAnalyzer(Analyzer):
    def __init__(self) -> None:
        super().__init__(__name__)
        self.globalImports: List[str] = []

    def analyze(self, rootDir: str, path: str) -> List[AbstractObject]:
        abstractObjects: List[AbstractObject] = []
        self.logger.info("Analysing %s", path)
        parsed: Any = None
        with open(path) as file:
            parser = kopyt.Parser(file.read())
            try:
                parsed = parser.parse()
            except kopyt.exception.ParserException:
                self.logger.error("Error parsing %s, will be ommitted.", path)
                return abstractObjects

        # Handle imports
        self.globalImports = []
        for item in parsed.imports:
            importNS = item.name.replace(".", "::")
            if not item.wildcard:
                importNS = importNS[: importNS.rindex("::")]
            self.globalImports.append(importNS)

        # handle package
        currentNS = ""
        if parsed.package:
            currentNS = parsed.package.name.replace(".", "::")

        # handle types
        for item in parsed.declarations:
            if isinstance(item, kopyt.node.EnumDeclaration):
                self.handleEnum(abstractObjects, path, currentNS, item)
            elif isinstance(item, kopyt.node.ClassDeclaration) or isinstance(
                item, kopyt.node.InterfaceDeclaration
            ):
                self.handleClass(abstractObjects, path, currentNS, item)
            elif isinstance(item, kopyt.node.FunctionDeclaration):
                self.handleFunction(abstractObjects, path, currentNS, item)
        return abstractObjects

    def handleClass(
        self,
        abstractObjects: List[AbstractObject],
        path: str,
        currentNS: str,
        klass: Union[kopyt.node.ClassDeclaration, kopyt.node.InterfaceDeclaration],
    ) -> None:
        abstraction = AbstractClass(klass.name, currentNS, path)

        for ns in self.globalImports:
            abstraction.addUsingNamespace(ns)

        self.handleParent(abstraction, klass.supertypes)
        if klass.constructor:
            self.handleConstuctor(abstraction, klass.constructor, True)
        if klass.generics:
            for genType in klass.generics:
                abstraction.addGenericType(str(genType).strip())
        if klass.body:
            for item in klass.body.members:
                if isinstance(item, kopyt.node.ClassDeclaration):
                    self.handleClass(
                        abstractObjects, path, currentNS + "::" + klass.name, item
                    )
                elif isinstance(item, kopyt.node.CompanionObject) and item.body:
                    for subitem in item.body.members:
                        if isinstance(subitem, kopyt.node.PropertyDeclaration):
                            self.handleProperty(abstraction, subitem, True)
                        elif isinstance(item, kopyt.node.FunctionDeclaration):
                            self.handleMethod(abstraction, item, True)
                        else:
                            self.logger.error(
                                "Unhandled companion object member type %s", type(item)
                            )
                elif isinstance(item, kopyt.node.SecondaryConstructor):
                    self.handleConstuctor(abstraction, item, False)
                elif isinstance(item, kopyt.node.PropertyDeclaration):
                    self.handleProperty(abstraction, item, False)
                elif isinstance(item, kopyt.node.FunctionDeclaration):
                    self.handleMethod(abstraction, item, False)
                elif isinstance(item, kopyt.node.ObjectDeclaration) and item.body:
                    for subitem in item.body.members:
                        if isinstance(subitem, kopyt.node.PropertyDeclaration):
                            self.handleProperty(abstraction, subitem, True)
                        elif isinstance(item, kopyt.node.FunctionDeclaration):
                            self.handleMethod(abstraction, item, True)
                        else:
                            self.logger.error(
                                "Unhandled object member type %s", type(item)
                            )
                elif isinstance(item, kopyt.node.AnonymousInitializer):
                    # Nothing to be done
                    pass
                else:
                    self.logger.error("Unhandled member type %s", type(item))
        abstraction.objectLanguage = AbstractObjectLanguage.Kotlin
        abstractObjects.append(abstraction)

    def handleParent(
        self,
        abstraction: AbstractClass,
        item: kopyt.node.DelegationSpecifiers,
    ) -> None:
        for supertype in item:
            if isinstance(supertype, kopyt.node.AnnotatedDelegationSpecifier):
                if isinstance(supertype.delegate, kopyt.node.UserType):
                    for elem in supertype.delegate.sequence:
                        abstraction.addParent(str(elem), elem.name, "public")
                elif isinstance(supertype.delegate, kopyt.node.ConstructorInvocation):
                    for elem in supertype.delegate.invoker.sequence:
                        abstraction.addParent(str(elem), elem.name, "public")
                else:
                    self.logger.error(
                        "Unhandled supertype delegation type %s",
                        type(supertype.delegate),
                    )
            else:
                self.logger.error(
                    "Unhandled supertype type %s",
                    type(supertype),
                )

    def handleConstuctor(
        self,
        abstraction: AbstractClass,
        item: Union[kopyt.node.PrimaryConstructor, kopyt.node.SecondaryConstructor],
        isPrimary: bool,
    ) -> None:
        constructorVisibility = self.deduceVisibility(item)
        constructorParams: List[Tuple[str, str]] = []
        for param in item.parameters:
            paramVisibility = self.deduceVisibility(param)
            paramName = param.name
            paramType = self.deduceType(str(param.type))
            constructorParams.append((paramType, paramName))
            if isPrimary and param.mutability:
                paramType = self.deduceType(
                    str(param.mutability) + " " + str(param.type)
                )
                abstraction.addMember(paramType, paramName, paramVisibility)
        abstraction.addMethod(
            abstraction.name, "constructor", constructorParams, constructorVisibility
        )

    def handleProperty(
        self,
        abstraction: AbstractClass,
        item: kopyt.node.PropertyDeclaration,
        isStatic: bool,
    ) -> None:
        visibility = self.deduceVisibility(item)
        if isinstance(item.declaration, kopyt.node.MultiVariableDeclaration):
            for decl in item.declaration:
                name = item.declaration.name
                type = item.declaration.type
                if not type:
                    type = self.deduceTypeFromExpression(str(item.value))
                type = str(item.mutability) + " " + self.deduceType(str(type))
                if isStatic:
                    type = "static " + type
                abstraction.addMember(type, name, visibility)
        else:
            name = item.declaration.name
            type = item.declaration.type
            if not type:
                type = self.deduceTypeFromExpression(str(item.value))
            type = str(item.mutability) + " " + self.deduceType(str(type))
            if isStatic:
                type = "static " + type
            abstraction.addMember(type, name, visibility)

    def handleMethod(
        self,
        abstraction: AbstractClass,
        item: kopyt.node.FunctionDeclaration,
        isStatic: bool,
    ) -> None:
        visibility = self.deduceVisibility(item)
        rtype = "Unit"
        if item.type:
            rtype = self.deduceType(str(item.type))
        params: List[Tuple[str, str]] = []
        for param in item.parameters:
            paramType = self.deduceType(str(param.type))
            paramName = str(param.name)
            params.append((paramType, paramName))
        abstraction.addMethod(rtype, item.name, params, visibility)
        if item.generics:
            for genType in item.generics:
                abstraction.addGenericType(str(genType).strip())

    def handleEnum(
        self,
        abstractObjects: List[AbstractObject],
        path: str,
        currentNS: str,
        enum: kopyt.node.EnumDeclaration,
    ) -> None:
        values: List[str] = []
        for item in enum.body.entries:
            values.append(item.name)
        abstraction = AbstractEnum(enum.name, currentNS, path, values)
        abstraction.objectLanguage = AbstractObjectLanguage.Kotlin
        abstractObjects.append(abstraction)

    def handleFunction(
        self,
        abstractObjects: List[AbstractObject],
        path: str,
        currentNS: str,
        function: kopyt.node.FunctionDeclaration,
    ) -> None:
        rtype = "KotlinTypeNotFound"
        if function.type:
            rtype = self.deduceType(str(function.type))
        params: List[Tuple[str, str]] = []
        for param in function.parameters:
            paramType = self.deduceType(str(param.type))
            paramName = str(param.name)
            params.append((paramType, paramName))
        doxygen = ""
        abstraction = AbstractFunction(
            str(function.name),
            path,
            rtype,
            params,
            currentNS,
            doxygen,
        )
        if function.generics:
            for genType in function.generics:
                abstraction.addGenericType(str(genType).strip())
        abstraction.objectLanguage = AbstractObjectLanguage.Kotlin
        abstractObjects.append(abstraction)

    def deduceVisibility(self, item: Any) -> str:
        visibility = "public"
        if "private" in item.modifiers:
            visibility = "private"
        if "protected" in item.modifiers:
            visibility = "protected"
        return visibility

    def deduceTypeFromExpression(self, expression: str) -> str:
        if "{" in expression:
            expression = expression[: expression.index("{")]
        expression = expression.strip()

        if expression.startswith('"'):
            return "String"
        elif re.match("^ *object *:", expression):
            index = expression.index(":") + 1
            return self.deduceType(expression[index:])
        elif re.match("[-+]?\\d+.{0,1}\\d*[fF]$", expression):
            return "Float"
        elif re.match("[-+]?\\d+L$", expression):
            return "Long"
        elif re.match("[-+]?\\d+$", expression):
            return "Int"
        elif re.match("[-+]?\\d+.{0,1}\\d*$", expression):
            return "Double"
        elif "<" in expression and expression[-1] == ">":
            return self.deduceType(expression)
        elif "(" in expression and expression[-1] == ")":
            return self.deduceType(expression[: expression.rindex("(")])
        elif "." in expression:
            return self.deduceType(expression[: expression.rindex(".")])
        return "KotlinAuto"

    def deduceType(self, type: str) -> str:
        return type.replace(".", "::").replace(" ", "").strip()
