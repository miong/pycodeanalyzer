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
    ImportFrom,
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
    """Python Analyzer.

    Handle Python code using astroid
    """

    def __init__(self) -> None:
        super().__init__(__name__)
        self.globalImports: List[str] = []

    def analyze(self, rootDir: str, path: str) -> List[AbstractObject]:
        abstractObjects: List[AbstractObject] = []
        self.logger.info("Analysing %s", path)

        content: str = ""
        with open(path, "r") as srcFile:
            content = srcFile.read()

        if len(content) <= 0:
            return abstractObjects

        namespace = self.deduceNamespace(path, rootDir)
        tree: Any = astroid.parse(content)
        self.globalImports = self.getImportsNameSpace(tree.body)
        for item in tree.body:
            if isinstance(item, ClassDef):
                if (
                    len(item.bases) == 1
                    and isinstance(item.bases[0], Name)
                    and self.isEnumType(item.bases[0].name)
                ):
                    self.handleEnum(
                        path, namespace, cast(ClassDef, item), abstractObjects
                    )
                else:
                    self.handleClass(
                        path, namespace, cast(ClassDef, item), abstractObjects
                    )
            if isinstance(item, FunctionDef):
                self.handleFunction(
                    path, namespace, cast(FunctionDef, item), abstractObjects
                )

        return abstractObjects

    def handleEnum(
        self,
        path: str,
        namespace: str,
        item: ClassDef,
        abstractObjects: List[AbstractObject],
    ) -> None:
        values: List[str] = []
        for subItem in item.body:
            if isinstance(subItem, Assign):
                values.append(subItem.targets[0].name)
        abstraction = AbstractEnum(item.name, namespace, path, values)
        abstraction.objectLanguage = AbstractObjectLanguage.Python
        abstractObjects.append(abstraction)

    def handleClass(
        self,
        path: str,
        namespace: str,
        item: ClassDef,
        abstractObjects: List[AbstractObject],
    ) -> None:
        abstraction = AbstractClass(item.name, namespace, path)
        for ns in self.globalImports:
            abstraction.addUsingNamespace(ns)
        for parents in item.bases:
            parentName = "unamed_function"
            if isinstance(parents, Name):
                parentName = self.deduceTypeFromTypeName(parents)
            elif isinstance(parents, Attribute):
                parentName = (
                    self.deduceNamespaceFromAttribute(parents) + "::" + parents.attrname
                )
            abstraction.addParent(parentName, parentName, "public")
        abstraction.objectLanguage = AbstractObjectLanguage.Python
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
                rtype = "Any"
                if subItem.returns:
                    rtype = self.deduceReturnType(subItem.returns)
                abstraction.addMethod(rtype, funcname, params, visibility)
                self.handleMembers(subItem, abstraction)
        abstractObjects.append(abstraction)

    def isEnumType(self, type: str) -> bool:
        return (
            type == "Enum"
            or type == "IntEnum"
            or type == "StrEnum"
            or type == "Flag"
            or type == "IntFlag"
        )

    def handleFunction(
        self,
        path: str,
        namespace: str,
        item: FunctionDef,
        abstractObjects: List[AbstractObject],
    ) -> None:
        funcname = item.name
        if item.name.startswith("_"):
            funcname = re.sub("^[ _]*", "", item.name)
        funargs = item.args
        params = []
        for i in range(0, len(funargs.args)):
            paramName = funargs.args[i].name
            if paramName == "self":
                continue
            paramType = "Any"
            if funargs.annotations[i]:
                paramType = self.handleTypeAnnotation(funargs.annotations[i])
            params.append((paramType, paramName))
        rtype = "Any"
        if item.returns:
            rtype = self.deduceReturnType(item.returns)
        doxygen = '"""No comments in file"""'
        if item.doc_node:
            doxygen = '"""' + item.doc_node.value + '"""'
        abstraction = AbstractFunction(
            funcname, path, rtype, params, namespace, doxygen
        )
        abstraction.objectLanguage = AbstractObjectLanguage.Python
        abstractObjects.append(abstraction)

    def handleMembers(self, func: Any, abstraction: AbstractClass) -> None:
        for item in func.body:
            if isinstance(item, Assign):
                for target in cast(Assign, item).targets:
                    if isinstance(target, AssignAttr):
                        attr = cast(AssignAttr, target)
                        if (
                            isinstance(attr.expr, Name)
                            and cast(Name, attr.expr).name == "self"
                        ):
                            name = attr.attrname
                            visibility = "public"
                            if name.startswith("_"):
                                name = re.sub("^[ _]*", "", name)
                                visibility = "private"
                            if not abstraction.hasMember(name):
                                abstraction.addMember(
                                    self.deduceType(func, item), name, visibility
                                )
            if isinstance(item, AnnAssign):
                if isinstance(item.target, AssignAttr):
                    attr = cast(AssignAttr, item.target)
                    if (
                        isinstance(attr.expr, Name)
                        and cast(Name, attr.expr).name == "self"
                    ):
                        name = attr.attrname
                        visibility = "public"
                        if name.startswith("_"):
                            name = re.sub("^[ _]*", "", name)
                            visibility = "private"
                        abstraction.addMember(
                            self.handleTypeAnnotation(item.annotation),
                            name,
                            visibility,
                        )

    def deduceType(self, func: FunctionDef, item: Assign) -> str:
        # TODO Handle non const affectation
        if isinstance(item.value, Const):
            return self.deduceTypeFromConst(item.value)
        if isinstance(item.value, Name):
            return self.deduceTypeFromName(func, item.value)
        if isinstance(item.value, typeList):
            return self.deduceTypeFromList(item.value)
        if isinstance(item.value, Tuple):
            return self.deduceTypeFromTuple(item.value)
        if isinstance(item.value, Dict):
            return self.deduceTypeFromDict(item.value)
        if isinstance(item.value, Subscript):
            return self.handleTypeAnnotation(item.value)
        # TODO handle function call returns and IfExp if possible
        return "Any"

    def deduceReturnType(self, returnItem: Any) -> str:
        if isinstance(returnItem, Const):
            return self.deduceTypeFromConst(returnItem)
        if isinstance(returnItem, Name):
            return self.deduceTypeFromTypeName(returnItem)
        if isinstance(returnItem, Subscript):
            return self.handleTypeAnnotation(returnItem)
        if isinstance(returnItem, Attribute):
            return self.handleTypeAnnotation(returnItem)
        return "Any"

    def deduceTypeFromTypeName(self, item: Name) -> str:
        return item.name

    def deduceTypeFromName(self, func: FunctionDef, item: Name) -> str:
        searchedName = item.name
        for i in range(0, len(func.args.args)):
            if func.args.args[i].name == searchedName:
                if func.args.annotations[i]:
                    return self.handleTypeAnnotation(func.args.annotations[i])
                if (
                    len(func.args.defaults) == len(func.args.args)
                    and func.args.defaults[i]
                ):
                    return self.deduceTypeFromConst(func.args.defaults[i])
                return "Any"
        return "Any"

    def deduceTypeFromTuple(self, item: Tuple) -> str:
        # TODO Handle non const affectation
        innerType = ""
        for elem in item.elts:
            elemType = "Any"
            if isinstance(elem, Const):
                elemType = self.deduceTypeFromConst(elem)
            innerType += elemType + ","
        return "Tuple<" + innerType[:-1] + ">"

    def deduceTypeFromList(self, item: typeList) -> str:
        # TODO Handle non const affectation
        innerType = ""
        for elem in item.elts:
            if isinstance(elem, Const):
                elemType = self.deduceTypeFromConst(elem)
                if len(innerType) == 0:
                    innerType = elemType
                elif innerType != elemType:
                    innerType = "Any"
                    break
        if len(innerType) == 0:
            innerType = "Any"
        return "List<" + innerType + ">"

    def deduceTypeFromDict(self, item: Dict) -> str:
        # TODO Handle non const affectation
        keyType = ""
        valueType = ""
        for dictKV in item.items:
            kvKeyType = "Any"
            if isinstance(dictKV[0], Const):
                kvKeyType = self.deduceTypeFromConst(dictKV[0])
                if len(keyType) == 0:
                    keyType = kvKeyType
                elif keyType != kvKeyType:
                    keyType = "Any"
            kvValueType = "Any"
            if isinstance(dictKV[1], Const):
                kvValueType = self.deduceTypeFromConst(dictKV[1])
                if len(valueType) == 0:
                    valueType = kvValueType
                elif valueType != kvValueType:
                    valueType = "Any"
        return "Dict<" + keyType + "," + valueType + ">"

    def deduceTypeFromConst(self, item: Const) -> str:
        typeName = type(item.value).__name__
        if typeName == "NoneType":
            typeName = "None"
        return typeName

    def handleTypeAnnotation(self, typeNope: Any) -> str:
        if isinstance(typeNope, Subscript):
            outter = typeNope.value.name
            inner = self.handleTypeAnnotation(typeNope.slice)
            if outter == "Optional":
                return inner
            return outter + "<" + inner + ">"
        elif isinstance(typeNope, Tuple):
            res = ""
            for inner in typeNope.elts:
                res += self.handleTypeAnnotation(inner) + ","
            res = res[:-1]
            return res
        elif isinstance(typeNope, Attribute):
            ns = self.deduceNamespaceFromAttribute(typeNope)
            return ns + "::" + typeNope.attrname
        else:
            return typeNope.name

    def deduceNamespaceFromAttribute(
        self, attrib: Attribute, isRoot: bool = True
    ) -> str:
        if isinstance(attrib.expr, Attribute):
            ns = self.deduceNamespaceFromAttribute(attrib.expr, False)
            if not isRoot:
                ns = ns + "::" + attrib.attrname
            return ns
        else:
            return attrib.expr.name

    def deduceNamespace(self, path: str, rootDir: str) -> str:
        namespace = ""
        rootabspath = os.path.abspath(rootDir)
        relPath = rootDir + path.replace(rootabspath, "")
        fileDirPath = os.path.dirname(relPath)
        fileName = os.path.basename(relPath).replace(".py", "")
        dirs = fileDirPath.split(os.sep)
        dirPath = path.replace(relPath, "")
        for i in range(0, len(dirs)):
            dirPath += dirs[i] + os.sep
            moduleInit = dirPath + "__init__.py"
            if os.path.exists(moduleInit):
                namespace += "::" + dirs[i]
            else:
                namespace = ""
        if len(namespace) > 0:
            namespace = namespace[2:] + "::" + fileName
        return namespace

    def getImportsNameSpace(self, item: Any) -> List[str]:
        res = []
        for subItem in item:
            if isinstance(subItem, ImportFrom):
                ns = subItem.modname.replace(".", "::")
                res.append(ns)
        return res
