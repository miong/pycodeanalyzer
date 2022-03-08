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
        print("Enum : ",self.name)
        print("\tValues : ")
        for value in self.values:
            print("\t\t * ", value)


class AbstractClass(AbstractObject):
    def __init__(self, name, origin):
        self.name = name
        self.type = "Class"
        self.members = []
        self.methodes = []
        self.origin = origin

    def addMember(self, type, name, visibility):
        self.members.append((type, name, visibility))

    def addMethod(self, returnType, name, parameters, visibility):
        self.methodes.append((returnType, name, parameters, visibility))

    def getLinkedTypes(self):
        types = []
        for method in self.methodes:
            if method[0] not in types:
                types.append(method[0].replace('*', '').strip())
            for param in method[2]:
                if param[0] not in types:
                    types.append(param[0].replace('*', '').strip())
        return types

    def print(self):
        print("Class : ",self.name)
        print("\tMethods : ")
        for tuple in self.methodes:
            paramStr = ""
            for param in tuple[2]:
                paramStr = paramStr + param[0] + " " + param[1] + ", "
            paramStr=paramStr[:-2]
            print("\t\t * {3} {0} {1} ({2})".format(tuple[0], tuple[1],paramStr,tuple[3]))
        print("\tMembers : ")
        for tuple in self.members:
            print("\t\t * {2} {0} {1}".format(tuple[0], tuple[1], tuple[2]))
