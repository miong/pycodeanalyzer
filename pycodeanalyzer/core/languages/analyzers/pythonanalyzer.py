import os
import re
from typing import Any, List, cast

import astroid
from astroid.nodes.node_classes import (
    AnnAssign,
    Assign,
    AssignAttr,
    Attribute,
    Const,
    Dict,
)
from astroid.nodes.node_classes import List as typeList
from astroid.nodes.node_classes import Name, Subscript, Tuple
from astroid.nodes.scoped_nodes import ClassDef, FunctionDef

from pycodeanalyzer.core.abstraction.objects import (
    AbstractClass,
    AbstractEnum,
    AbstractFunction,
    AbstractObject,
    AbstractObjectLanguage,
)
from pycodeanalyzer.core.languages.analyzer import Analyzer


class PythonAnalyzer(Analyzer):
    def __init__(self) -> None:
        super().__init__()

    def analyze(self, rootDir: str, path: str) -> List[AbstractObject]:
        abstractObjects: List[AbstractObject] = []
        abspath: str = os.path.join(rootDir, path)
        self.logger.info("Analysing %s", path)

        content: str = ""
        with open(abspath, "r") as srcFile:
            content = srcFile.read()

        if len(content) <= 0:
            return abstractObjects

        tree: Any = astroid.parse(content)
        for item in tree.body:
            if isinstance(item, ClassDef):
                self.handleClass(path, cast(ClassDef, item), abstractObjects)
            if isinstance(item, FunctionDef):
                # TODO handle free functions
                print("Found free funcion ", item.name)

        return abstractObjects

    def handleClass(
        self, path: str, item: ClassDef, abstractObjects: List[AbstractObject]
    ) -> None:
        # TODO handle enum !
        abstraction = AbstractClass(item.name, "", path)
        abstraction.language = AbstractObjectLanguage.Python
        for subItem in item.body:
            if isinstance(subItem, FunctionDef):
                funcname = subItem.name
                visibility = "public"
                if subItem.name == "__init__":
                    funcname = "Constructor"
                elif subItem.name.startswith("_"):
                    funcname = re.sub("^[ _]*", "", subItem.name)
                    visibility = "private"
                funargs = subItem.args
                params = []
                for i in range(0, len(funargs.args)):
                    paramName = funargs.args[i].name
                    if paramName == "self":
                        continue
                    paramType = "Any"
                    if funargs.annotations[i]:
                        paramType = self.handleTypeAnnotation(funargs.annotations[i])
                    params.append((paramType, paramName))
                # TODO return type
                abstraction.addMethod("None", funcname, params, visibility)
                self.handleMembers(subItem, abstraction)
        abstractObjects.append(abstraction)

    def handleMembers(self, func: Any, abstraction: AbstractClass) -> None:
        # TODO Handle private
        for item in func.body:
            if isinstance(item, Assign):
                for target in cast(Assign, item).targets:
                    if isinstance(target, AssignAttr):
                        attr = cast(AssignAttr, target)
                        if (
                            isinstance(attr.expr, Name)
                            and cast(Name, attr.expr).name == "self"
                        ):
                            abstraction.addMember(
                                self.deduceType(func, item), attr.attrname, "public"
                            )
            if isinstance(item, AnnAssign):
                if isinstance(item.target, AssignAttr):
                    attr = cast(AssignAttr, item.target)
                    if (
                        isinstance(attr.expr, Name)
                        and cast(Name, attr.expr).name == "self"
                    ):
                        abstraction.addMember(
                            self.handleTypeAnnotation(item.annotation),
                            attr.attrname,
                            "public",
                        )

    #TODO split this function cause too complex !
    def deduceType(self, func: Any, item: Assign) -> str:
        # TODO Handle non const affectation
        if isinstance(item.value, Const):
            return self.deduceConstType(item.value)
        if isinstance(item.value, Name):
            searchedName = item.value.name
            for i in range(0, len(func.args.args)):
                if func.args.args[i].name == searchedName:
                    if func.args.annotations[i]:
                        return self.handleTypeAnnotation(func.args.annotations[i])
                    if (
                        len(func.args.defaults) == len(func.args.args)
                        and func.args.defaults[i]
                    ):
                        return self.deduceConstType(func.args.defaults[i])
                    return "Any"
            return "Any"
        if isinstance(item.value, typeList):
            innerType = ""
            for elem in item.value.elts:
                if isinstance(elem, Const):
                    elemType = self.deduceConstType(elem)
                    if len(innerType) == 0:
                        innerType = elemType
                    elif innerType != elemType:
                        innerType = "Any"
                        break
            if len(innerType) == 0:
                innerType = "Any"
            return "List<" + innerType + ">"
        if isinstance(item.value, Tuple):
            innerType = ""
            for elem in item.value.elts:
                elemType = "Any"
                if isinstance(elem, Const):
                    elemType = self.deduceConstType(elem)
                innerType += elemType + ","
            return "Tuple<" + innerType[:-1] + ">"
        if isinstance(item.value, Dict):
            keyType = ""
            valueType = ""
            for dictKV in item.value.items:
                kvKeyType = "Any"
                if isinstance(dictKV[0], Const):
                    kvKeyType = self.deduceConstType(dictKV[0])
                    if len(keyType) == 0:
                        keyType = kvKeyType
                    elif keyType != kvKeyType:
                        keyType = "Any"
                kvValueType = "Any"
                if isinstance(dictKV[1], Const):
                    kvValueType = self.deduceConstType(dictKV[1])
                    if len(valueType) == 0:
                        valueType = kvValueType
                    elif valueType != kvValueType:
                        valueType = "Any"
            return "Dict<" + keyType + "," + valueType + ">"
        return "Any"

    def deduceConstType(self, item: Const) -> str:
        return type(item.value).__name__

    def handleTypeAnnotation(self, typeNope: Any) -> str:
        if isinstance(typeNope, Subscript):
            outter = typeNope.value.name
            inner = self.handleTypeAnnotation(typeNope.slice)
            return outter + "<" + inner + ">"
        elif isinstance(typeNope, Tuple):
            res = ""
            for inner in typeNope.elts:
                res += self.handleTypeAnnotation(inner) + ","
            res = res[:-1]
            return res
        elif isinstance(typeNope, Attribute):
            return typeNope.attrname
        else:
            return typeNope.name
