class AbstractObject:
    def __init__(self, name, origin):
        self.name = name
        self.type = "Object"
        self.origin = origin


class AbstractEnum(AbstractObject):
    def __init__(self, name, origin, values):
        self.name = name
        self.type = "Enum"
        self.values = values
        self.origin = origin

    def print(self):
        print("Enum : ", self.name)
        print("\tValues : ")
        for value in self.values:
            print("\t\t * ", value)


class AbstractFunction(AbstractObject):
    def __init__(self, name, origin, returnType, parameters):
        self.name = name
        self.type = "Function"
        self.returnType = returnType
        self.origin = origin
        self.parameters = parameters

    def print(self):
        print("Enum : ", self.name)
        print("\tValues : ")
        for value in self.values:
            print("\t\t * ", value)


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
            type = self.getDependanceFromType(parent[1])
            if type not in types:
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
                    type = self.getDependanceFromType(templateType)
                    if type not in types:
                        types.append(type)
        for method in self.methodes:
            type = self.getDependanceFromType(method[0])
            if type not in types:
                types.append(type)
            for param in method[2]:
                type = self.getDependanceFromType(param[0])
                if type not in types:
                    types.append(type)
        for member in self.members:
            if "<" in member[0]:
                # TODO Handle nested
                print(member[0])
                index = member[0].index("<")
                templateTypeList = (
                    member[0][index:].replace("<", "").replace(">", "").split(",")
                )
                print(templateTypeList)
                for templateType in templateTypeList:
                    type = self.getDependanceFromType(templateType)
                    if type not in types:
                        types.append(type)
            type = self.getDependanceFromType(member[0])
            if type not in types:
                types.append(type)
        types = self.removeNonObjectTypes(types)
        return types

    def getDependanceFromType(self, type):
        # remove all languages artefact that are not needed to get the type we depends on
        return type.replace("*", "").replace("&", "").replace("const", "").strip()

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
            "uint8_t",
            "uint16_t",
            "uint32_t",
            "uint64_t",
        ]
        cleaned_list = [x for x in typeList if x not in NonObjectTypes]
        return cleaned_list

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
