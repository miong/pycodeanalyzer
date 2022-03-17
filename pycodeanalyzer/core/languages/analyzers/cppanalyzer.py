import argparse
import io
import os
import re

import CppHeaderParser
import magic
from pcpp import Action, OutputDirective, Preprocessor

from pycodeanalyzer.core.abstraction.objects import (
    AbstractClass,
    AbstractEnum,
    AbstractFunction,
)
from pycodeanalyzer.core.languages.analyzer import Analyzer


class CustumCppPreprocessor(Preprocessor):
    def __init__(self):
        super().__init__()
        self.passthru_includes = re.compile(".*")
        self.expand_linemacro = False
        self.expand_filemacro = False
        self.expand_countermacro = False
        self.bypass_ifpassthru = False

    def parseFile(self, path):
        item = argparse.FileType("rt")(path)
        self.parse(item)

    def addDefine(self, d):
        if "=" not in d:
            d += "=1"
            d = d.replace("=", " ", 1)
        self.define(d)

    def getResult(self):
        string = ""
        ss = io.StringIO(string)
        self.write(ss)
        return ss.getvalue()

    def on_include_not_found(
        self, is_malformed, is_system_include, curdir, includepath
    ):
        raise OutputDirective(Action.IgnoreAndPassThrough)

    def on_comment(self, tok):
        return True

    def on_directive_handle(self, directive, toks, ifpassthru, precedingtoks):
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

    def on_unknown_macro_in_defined_expr(self, tok):
        return False


class CustomCppHeader(CppHeaderParser.CppHeader):
    def is_enum_namestack(nameStack):
        if not nameStack:
            return False
        if nameStack[0] == "enum" and "*" not in nameStack:
            return True
        if len(nameStack) > 1 and nameStack[0] == "typedef" and nameStack[1] == "enum":
            return "{" in nameStack
        return False

    def is_method_namestack(stack):
        r = False
        if "(" not in stack:
            r = False
        elif stack[0] == "typedef":
            r = False  # TODO deal with typedef function prototypes
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
                r = True  # ideally we catch both braces... TODO
        else:
            r = False
        # Test for case of property set to something with parens such as "static const int CONST_A = (1 << 7) - 1;"
        if r and "(" in stack and "=" in stack and "operator" not in stack:
            if stack.index("=") < stack.index("("):
                r = False
        return r


class CppAnalyzer(Analyzer):
    def __init__(self):
        super().__init__()
        # TODO : parse it from configuration
        CppHeaderParser.CppHeaderParser.ignoreSymbols = [
            "_sd_printf_attr_()",
            "_sd_hidden_",
            "BAGADM_ATTRIBUTE_FORMAT_PRINTF()",
            "BAGADM_ATTRIBUTE_FORMAT_SCANF()",
            "G_GNUC_PRINTF ()",
            "G_GNUC_PRINTF()",
            "G_GNUC_MALLOC",
            "G_GNUC_ALLOC_SIZE2 ()",
            "G_GNUC_ALLOC_SIZE2()" "PROTOBUF_EXPORT",
            "PROTOBUF_DEPRECATED_ATTR",
            "PROTOBUF_DEPRECATED",
        ]
        CppHeaderParser.CppHeaderParser.is_enum_namestack = (
            CustomCppHeader.is_enum_namestack
        )
        CppHeaderParser.CppHeaderParser.is_method_namestack = (
            CustomCppHeader.is_method_namestack
        )
        self.objectPaths = []

    def analyze(self, rootDir, path):
        abstractObjects = []
        self.logger.info("Analysing %s", path)
        abspath = os.path.join(rootDir, path)

        encoding = magic.Magic(
            mime_encoding=True,
        ).from_file(abspath)

        try:
            preproc = CustumCppPreprocessor()
            preproc.parseFile(abspath)
            header = CustomCppHeader(
                preproc.getResult(), argType="string", encoding=encoding
            )
            header.headerFileName = abspath
            for klass in header.classes.values():
                self.handleClass(path, klass, abstractObjects)
            for enum in header.enums:
                self.handleEnum(path, enum, abstractObjects)
            for function in header.functions:
                self.handleFunction(path, function, abstractObjects)
        except AssertionError as err:
            self.logger.warning(err)
            self.logger.warning("Error analyzing %s", path)
        except CppHeaderParser.CppHeaderParser.CppParseError as err:
            self.logger.warning(err)
            self.logger.warning("Error analyzing %s", path)
        except UnicodeDecodeError as err:
            self.logger.warning(err)
            self.logger.warning("Error analyzing %s : can't decode file", path)
        return abstractObjects

    def handleClass(self, path, klass, abstractObjects):
        objectPath = (klass["namespace"] + "::" + klass["name"]).strip()
        if objectPath in self.objectPaths:
            self.logger.warning(
                "Name collision for %s in %s. It will be drop from the analysis.",
                klass["name"],
                path,
            )
            return
        namespace = self.clearNamespace(klass["namespace"])
        abstraction = AbstractClass(klass["name"], namespace, path)
        self.addParents(abstraction, klass)
        self.addMethods(abstraction, klass, "public")
        self.addMethods(abstraction, klass, "protected")
        self.addMethods(abstraction, klass, "private")
        self.addMembers(abstraction, klass, "public")
        self.addMembers(abstraction, klass, "protected")
        self.addMembers(abstraction, klass, "private")
        self.objectPaths.append(objectPath)
        abstractObjects.append(abstraction)

    def addMethods(self, abstraction, klass, visibility):
        for method in klass["methods"][visibility]:
            params = []
            for param in method["parameters"]:
                params.append((param["type"], param["name"]))
            rtnType = method["rtnType"]
            if method["name"] == klass["name"]:
                rtnType = klass["name"]
            abstraction.addMethod(rtnType, method["name"], params, visibility)

    def addMembers(self, abstraction, klass, visibility):
        for member in klass["properties"][visibility]:
            abstraction.addMember(member["type"], member["name"], visibility)

    def addParents(self, abstraction, klass):
        for declParent in klass["inherits"]:
            declName = declParent["class"]
            if "decl_name" in declParent:
                declName = declParent["decl_name"]
            abstraction.addParent(declParent["class"], declName, declParent["access"])

    def handleEnum(self, path, enum, abstractObjects):
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
            values.append(val["name"])
        name = enum["name"] if "name" in enum else "Anon-enum"
        namespace = self.clearNamespace(enum["namespace"])
        abstraction = AbstractEnum(name, namespace, path, values)
        abstractObjects.append(abstraction)
        self.objectPaths.append(objectPath)

    def handleFunction(self, path, function, abstractObjects):
        namespace = self.clearNamespace(function["namespace"])
        params = []
        for param in function["parameters"]:
            params.append((param["type"], param["name"]))
        doxygen = "/* No comments in file */"
        if "doxygen" in function:
            doxygen = function["doxygen"]
        abstraction = AbstractFunction(
            function["name"], path, function["rtnType"], params, namespace, doxygen
        )
        abstractObjects.append(abstraction)

    def clearNamespace(self, namespace):
        cleared = namespace.strip()
        if cleared[-2:] == "::":
            cleared = cleared[:-2]
        if cleared[:2] == "::":
            cleared = cleared[2:]
        return cleared
