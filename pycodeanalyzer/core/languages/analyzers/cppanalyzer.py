import argparse
import io
import re
from typing import Any, List

import CppHeaderParser
from pcpp import Action, OutputDirective, Preprocessor

from pycodeanalyzer.core.abstraction.objects import (
    AbstractClass,
    AbstractEnum,
    AbstractFunction,
    AbstractObject,
    AbstractObjectLanguage,
)
from pycodeanalyzer.core.encoding.encodings import Encoding
from pycodeanalyzer.core.languages.analyzer import Analyzer


class CustumCppPreprocessor(Preprocessor):
    def __init__(self) -> None:
        super().__init__()
        self.passthru_includes = re.compile(".*")
        self.expand_linemacro = False
        self.expand_filemacro = False
        self.expand_countermacro = False
        self.bypass_ifpassthru = False

    def parseFile(self, path: str) -> None:
        item: Any = argparse.FileType("rt")(path)
        self.parse(item)

    def addDefine(self, d: str) -> None:
        if "=" not in d:
            d += "=1"
            d = d.replace("=", " ", 1)
        self.define(d)

    def getResult(self) -> str:
        string = ""
        ss = io.StringIO(string)
        self.write(ss)
        return ss.getvalue()

    def on_include_not_found(
        self, is_malformed: Any, is_system_include: Any, curdir: Any, includepath: Any
    ) -> None:
        raise OutputDirective(Action.IgnoreAndPassThrough)

    def on_comment(self, tok: Any) -> Any:
        if tok.value.strip().startswith("/**"):
            return True
        return super().on_comment(tok)

    def on_directive_handle(
        self, directive: Any, toks: Any, ifpassthru: Any, precedingtoks: Any
    ) -> Any:
        if ifpassthru:
            if (
                directive.value == "if"
                or directive.value == "elif"
                or directive == "else"
                or directive.value == "endif"
            ):
                self.bypass_ifpassthru = (
                    len(
                        [
                            tok
                            for tok in toks
                            if tok.value == "__PCPP_ALWAYS_FALSE__"
                            or tok.value == "__PCPP_ALWAYS_TRUE__"
                        ]
                    )
                    > 0
                )
            if not self.bypass_ifpassthru and (
                directive.value == "define" or directive.value == "undef"
            ):
                if toks[0].value != self.potential_include_guard:
                    raise OutputDirective(
                        Action.IgnoreAndPassThrough
                    )  # Don't execute anything with effects when inside an #if expr with undefined macro
        super().on_directive_handle(directive, toks, ifpassthru, precedingtoks)
        return None  # Pass through where possible

    def on_unknown_macro_in_defined_expr(self, tok: Any) -> bool:
        return False


class CustomCppHeader(CppHeaderParser.CppHeader):
    def is_enum_namestack(nameStack: Any) -> bool:
        if not nameStack:
            return False
        if nameStack[0] == "enum" and "*" not in nameStack:
            return True
        if len(nameStack) > 1 and nameStack[0] == "typedef" and nameStack[1] == "enum":
            return "{" in nameStack
        return False

    def is_method_namestack(stack: Any) -> bool:
        r: bool = False
        if "(" not in stack:
            r = False
        elif stack[0] == "typedef":
            r = False  # deal with typedef function prototypes
        elif "operator" in stack:
            r = True  # allow all operators
        elif "{" in stack and stack.index("{") < stack.index("("):
            r = False  # struct that looks like a method/class
        elif "(" in stack and ")" in stack:
            if stack[-1] == ":":
                r = True
            elif "{" in stack and "}" in stack:
                r = True
            elif stack[-1] == ";":
                if CppHeaderParser.CppHeaderParser.is_function_pointer_stack(stack):
                    r = False
                else:
                    r = stack.index("(") > 1
            elif "{" in stack:
                r = True  # ideally we catch both braces...
        else:
            r = False
        # Test for case of property set to something with parens such as "static const int CONST_A = (1 << 7) - 1;"
        if r and "(" in stack and "=" in stack and "operator" not in stack:
            if stack.index("=") < stack.index("("):
                r = False
        return r


class CppAnalyzer(Analyzer):
    def __init__(self) -> None:
        super().__init__()
        CppHeaderParser.CppHeaderParser.ignoreSymbols = []
        CppHeaderParser.CppHeaderParser.is_enum_namestack = (
            CustomCppHeader.is_enum_namestack
        )
        CppHeaderParser.CppHeaderParser.is_method_namestack = (
            CustomCppHeader.is_method_namestack
        )
        self.objectPaths: List[str] = []
        self.encoding: Encoding = Encoding()
        self.forceIgnoredSymbols: List[str] = []

    def analyze(self, rootDir: str, path: str) -> List[AbstractObject]:
        abstractObjects: List[AbstractObject] = []
        self.logger.info("Analysing %s", path)

        encoding: str = self.encoding.getFileEncoding(path)

        try:
            preproc: CustumCppPreprocessor = CustumCppPreprocessor()
            preproc.parseFile(path)
            code: str = preproc.getResult()

            continueTryParsing: bool = True
            while continueTryParsing:
                try:
                    for symb in self.forceIgnoredSymbols:
                        code = code.replace(" " + symb + " ", " ")

                    # TODO handle using namespace
                    header: CustomCppHeader = CustomCppHeader(
                        code, argType="string", encoding=encoding
                    )
                    header.headerFileName = path
                    for klass in header.classes.values():
                        self.handleClass(path, klass, abstractObjects)
                    for enum in header.enums:
                        self.handleEnum(path, enum, abstractObjects)
                    for function in header.functions:
                        self.handleFunction(path, function, abstractObjects)
                    continueTryParsing = False
                except CppHeaderParser.CppHeaderParser.CppParseError as err:
                    unexpectedToken = self.extractUnexpectedFromParseError(err)
                    if (
                        not unexpectedToken
                        or unexpectedToken in self.forceIgnoredSymbols
                    ):
                        continueTryParsing = False
                        print(err)
                        self.logger.error(err)
                        self.logger.error("Error analyzing %s", path)
                    elif (
                        unexpectedToken in CppHeaderParser.CppHeaderParser.ignoreSymbols
                    ):
                        self.logger.warning(
                            "Addind '%s' to forced ignored symbols", unexpectedToken
                        )
                        self.forceIgnoredSymbols.append(unexpectedToken)
                    else:
                        self.logger.warning(
                            "Addind '%s' to ignored symbols", unexpectedToken
                        )
                        CppHeaderParser.CppHeaderParser.ignoreSymbols.append(
                            unexpectedToken
                        )
                        CppHeaderParser.CppHeaderParser.ignoreSymbols.append(
                            unexpectedToken + "()"
                        )
                        CppHeaderParser.CppHeaderParser.ignoreSymbols.append(
                            unexpectedToken + " ()"
                        )
        except AssertionError as err:
            self.logger.error(err)
            self.logger.error("Error analyzing %s", path)
        except UnicodeDecodeError as err:
            self.logger.error(err)
            self.logger.error("Error analyzing %s : can't decode file", path)
        return abstractObjects

    def handleClass(
        self, path: str, klass: Any, abstractObjects: List[AbstractObject]
    ) -> None:
        objectPath = (klass["namespace"] + "::" + klass["name"]).strip()
        if objectPath in self.objectPaths:
            self.logger.warning(
                "Name collision for %s in %s. It will be drop from the analysis.",
                klass["name"],
                path,
            )
            return
        namespace = self.clearNamespace(klass["namespace"])
        abstraction = AbstractClass(str(klass["name"]), namespace, path)
        self.addParents(abstraction, klass)
        self.addMethods(abstraction, klass, "public")
        self.addMethods(abstraction, klass, "protected")
        self.addMethods(abstraction, klass, "private")
        self.addMembers(abstraction, klass, "public")
        self.addMembers(abstraction, klass, "protected")
        self.addMembers(abstraction, klass, "private")
        abstraction.language = AbstractObjectLanguage.CPP
        self.objectPaths.append(objectPath)
        abstractObjects.append(abstraction)

    def addMethods(
        self, abstraction: AbstractClass, klass: Any, visibility: str
    ) -> None:
        for method in klass["methods"][visibility]:
            params = []
            for param in method["parameters"]:
                params.append((str(param["type"]), str(param["name"])))
            rtnType = method["rtnType"]
            if method["name"] == klass["name"]:
                rtnType = klass["name"]
            abstraction.addMethod(str(rtnType), str(method["name"]), params, visibility)

    def addMembers(
        self, abstraction: AbstractClass, klass: Any, visibility: str
    ) -> None:
        for member in klass["properties"][visibility]:
            abstraction.addMember(str(member["type"]), str(member["name"]), visibility)

    def addParents(self, abstraction: AbstractClass, klass: Any) -> None:
        for declParent in klass["inherits"]:
            declName = declParent["class"]
            if "decl_name" in declParent:
                declName = declParent["decl_name"]
            abstraction.addParent(
                str(declParent["class"]), str(declName), str(declParent["access"])
            )

    def handleEnum(
        self, path: str, enum: Any, abstractObjects: List[AbstractObject]
    ) -> None:
        if "name" not in enum:
            self.logger.warning("Anonymous enum found in %s, dropping it", path)
            return
        objectPath = (enum["namespace"] + "::" + enum["name"]).strip()
        if objectPath in self.objectPaths:
            self.logger.warning(
                "Name collision for %s in %s. It will be drop from the analysis.",
                enum["name"],
                path,
            )
            return
        values = []
        for val in enum["values"]:
            values.append(str(val["name"]))
        name = str(enum["name"]) if "name" in enum else "Anon-enum"
        namespace = self.clearNamespace(str(enum["namespace"]))
        abstraction = AbstractEnum(name, namespace, path, values)
        abstraction.language = AbstractObjectLanguage.CPP
        abstractObjects.append(abstraction)
        self.objectPaths.append(objectPath)

    def handleFunction(
        self, path: str, function: Any, abstractObjects: List[AbstractObject]
    ) -> None:
        namespace = self.clearNamespace(str(function["namespace"]))
        params = []
        for param in function["parameters"]:
            params.append((str(param["type"]), str(param["name"])))
        doxygen = "/* No comments in file */"
        if "doxygen" in function:
            doxygen = str(function["doxygen"])
        abstraction = AbstractFunction(
            str(function["name"]),
            path,
            str(function["rtnType"]),
            params,
            namespace,
            doxygen,
        )
        abstraction.language = AbstractObjectLanguage.CPP
        abstractObjects.append(abstraction)

    def clearNamespace(self, namespace: str) -> str:
        cleared = namespace.strip()
        if cleared[-2:] == "::":
            cleared = cleared[:-2]
        if cleared[:2] == "::":
            cleared = cleared[2:]
        return cleared

    def extractUnexpectedFromParseError(
        self, err: CppHeaderParser.CppHeaderParser.CppParseError
    ) -> str:
        msg = str(err)
        startDelim = "evaluating"
        endDelim = ":"
        if startDelim not in msg:
            return None
        token = msg[msg.index(startDelim) + len(startDelim) :]
        token = token[: token.index(endDelim) - 1].replace("'", "").strip()
        return token
