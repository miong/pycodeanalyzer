from pycodeanalyzer.core.languages.analyzer import Analyzer
from pycodeanalyzer.core.abstraction.objects import *

import CppHeaderParser
import os
import magic

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
        #TODO : parse it from configuration
        CppHeaderParser.CppHeaderParser.ignoreSymbols = [
            "_sd_printf_attr_()",
            "_sd_hidden_",
            "BAGADM_ATTRIBUTE_FORMAT_PRINTF()",
            "BAGADM_ATTRIBUTE_FORMAT_SCANF()",
            "G_GNUC_PRINTF ()",
            "G_GNUC_PRINTF()",
            "G_GNUC_MALLOC",
            "G_GNUC_ALLOC_SIZE2 ()",
            "G_GNUC_ALLOC_SIZE2()"
        ]
        CppHeaderParser.CppHeaderParser.is_enum_namestack = CustomCppHeader.is_enum_namestack
        CppHeaderParser.CppHeaderParser.is_method_namestack = CustomCppHeader.is_method_namestack

    def analyze(self, rootDir, path):
        abstractObjects = []
        self.logger.info("Analysing %s", path)
        abspath = os.path.join(rootDir, path)

        blob = open(abspath, 'rb').read()
        m = magic.open(magic.MAGIC_MIME_ENCODING)
        m.load()
        encoding = m.buffer(blob)

        try:
            header = CustomCppHeader(abspath, encoding=encoding)
            for klass in header.classes.values():
                #TODO Handle namespace !
                #TODO Handle nested !
                abstraction = AbstractClass(klass["name"], path)
                self.addMethods(abstraction, klass, "public")
                self.addMethods(abstraction, klass, "protected")
                self.addMembers(abstraction, klass, "public")
                self.addMembers(abstraction, klass, "protected")
                self.addMembers(abstraction, klass, "private")
                abstractObjects.append(abstraction)
            for enum in header.enums:
                values = []
                for val in enum["values"]:
                    values.append(val["name"])
                name = enum["name"] if "name" in enum else "Anon-enum"
                abstraction = AbstractEnum(name, path, values)
                abstractObjects.append(abstraction)
        except AssertionError as err:
            self.logger.warning("Error analyzing %s", path)
        except CppHeaderParser.CppHeaderParser.CppParseError as err:
            self.logger.warning("Error analyzing %s", path)
        return abstractObjects

    def addMethods(self, abstraction, klass, visibility):
        for method in klass["methods"][visibility]:
            params = [];
            for param in method["parameters"]:
                params.append((param["type"], param["name"]))
            abstraction.addMethod(method["rtnType"], method["name"], params, visibility)

    def addMembers(self, abstraction, klass, visibility):
        for member in klass["properties"][visibility]:
            abstraction.addMember(member["type"], member["name"], visibility)
