class AbstractObject:
    def __init__(self, name, origin):
        self.name = name
        self.type = "Object"
        self.origin = origin


class AbstractEnum(AbstractObject):
    def __init__(self, name, namespace, origin, values):
        self.name = name
        self.namespace = namespace
        self.type = "Enum"
        self.values = values
        self.origin = origin

    def getFullName(self):
        if len(self.namespace) <= 0:
            return self.name
        return self.namespace + "::" + self.name

    def print(self):
        print("Enum : ", self.name)
        print("\tValues : ")
        for value in self.values:
            print("\t\t * ", value)


class AbstractFunction(AbstractObject):
    def __init__(self, name, origin, returnType, parameters, namespace, doxygen):
        self.name = name
        self.namespace = namespace
        self.type = "Function"
        self.returnType = returnType
        self.origin = origin
        self.parameters = parameters
        self.doxygen = doxygen

    def print(self):
        print("Function : ", self.name)
        print("\tNamespace :", self.namespace)
        print("\tReturn :", self.returnType)
        print("\tParams :")
        for param in self.parameters:
            print("\t\t -", param[0], param[1])

    def getFullDef(self):
        ret = self.returnType + " " + self.namespace + "::" + self.name + "("
        for param in self.parameters:
            ret += param[0] + " " + param[1] + ", "
        ret = ret[:-2]
        ret += ")"
        return ret


class AbstractClass(AbstractObject):
    def __init__(self, name, namespace, origin):
        self.name = name
        self.namespace = namespace
        self.type = "Class"
        self.members = []
        self.methodes = []
        self.parents = []
        self.origin = origin

    def addMember(self, type, name, visibility):
        self.members.append((type, name, visibility))

    def addMethod(self, returnType, name, parameters, visibility):
        self.methodes.append((returnType, name, parameters, visibility))

    def addParent(self, completetype, name, visibility):
        self.parents.append((completetype, name, visibility))

    def getLinkedTypes(self):
        types = []
        for parent in self.parents:
            for type in self.getDependanceFromType(parent[1]):
                if type not in types and self.isPotentialClassName(type):
                    types.append(type)
            if parent[0] != parent[1]:
                # TODO Handle nested
                templateTypeList = (
                    parent[0]
                    .replace(parent[1], "")
                    .replace("<", "")
                    .replace(">", "")
                    .split(",")
                )
                for templateType in templateTypeList:
                    for type in self.getDependanceFromType(templateType):
                        if type not in types and self.isPotentialClassName(type):
                            types.append(type)
        for method in self.methodes:
            for type in self.getDependanceFromType(method[0]):
                if (
                    type not in types
                    and type != self.name
                    and self.isPotentialClassName(type)
                ):
                    types.append(type)
            for param in method[2]:
                for type in self.getDependanceFromType(param[0]):
                    if type not in types and self.isPotentialClassName(type):
                        types.append(type)
        for member in self.members:
            for type in self.getDependanceFromType(member[0]):
                if type not in types and self.isPotentialClassName(type):
                    types.append(type)
        types = self.removeNonObjectTypes(types)
        return types

    def isPotentialClassName(self, type):
        if not type:
            return False
        if len(type) <= 0:
            return False
        if "(" in type:
            return False
        return True

    def getDependanceFromType(self, type):
        deps = []
        if "<" in type:
            # TODO Handle nested
            index = type.index("<")
            templateTypeList = type[index:].replace("<", "").replace(">", "").split(",")
            for templateType in templateTypeList:
                innerTypes = self.getDependanceFromType(templateType)
                for dep in innerTypes:
                    if dep not in deps:
                        deps.append(self.cleanLanguageArtifacts(dep))
            type = type[:index].replace("<", "")
        deps.append(self.cleanLanguageArtifacts(type))
        return deps

    def getFullName(self):
        if len(self.namespace) <= 0:
            return self.name
        return self.namespace + "::" + self.name

    def cleanLanguageArtifacts(self, type):
        # remove all languages artefact that are not needed to get the type we depends on
        return (
            type.replace("*", "")
            .replace("&", "")
            .replace("const", "")
            .replace("static", "")
            .replace("...", "")
            .strip()
        )

    def removeNonObjectTypes(self, typeList):
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
        ]
        cleaned_list = [
            x for x in typeList if x not in NonObjectTypes and "std::" not in x
        ]
        return cleaned_list

    def isParent(self, klass):
        for tuple in self.parents:
            if tuple[0] == klass.name:
                return True
        return False

    def print(self):
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
