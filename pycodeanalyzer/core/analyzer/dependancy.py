from pycodeanalyzer.core.abstraction.objects import AbstractClass


class DependancyAnalyser:
    def analyze(self, klasses, enums, target):
        linkedClasses = []
        linkedEnums = []
        linkedFunctions = []  # TODO : need to process .c / .cc / .cpp files
        for type in target.getLinkedTypes():
            typeDeclaredNamespace = ""
            typeName = ""
            if "::" in type:
                lastSeparatorIndx = type.rindex("::")
                typeDeclaredNamespace = type[:lastSeparatorIndx]
                typeName = type[lastSeparatorIndx + 2 :]
            else:
                typeName = type
            linkedClass = self.findClass(
                typeDeclaredNamespace, typeName, klasses, target.namespace, target.name
            )
            linkedEnum = self.findEnum(
                typeDeclaredNamespace, typeName, enums, target.namespace, target.name
            )
            if linkedEnum:
                linkedEnums.append(linkedEnum)
            elif linkedClass:
                linkedClasses.append(linkedClass)
            else:
                linkedClasses.append(
                    AbstractClass(typeName, typeDeclaredNamespace, None)
                )
        return (target, linkedClasses, linkedEnums, linkedFunctions)

    def findClass(self, namespace, name, klasses, currentNamespace, currentClassName):
        for klass in klasses:
            if klass.namespace == namespace and klass.name == name:
                return klass
            if klass.namespace == currentClassName and klass.name == name:
                return klass
            if klass.namespace == currentNamespace and klass.name == name:
                return klass
            if (
                klass.namespace == currentNamespace + "::" + namespace
                and klass.name == name
            ):
                return klass
            if (
                klass.namespace == currentClassName + "::" + namespace
                and klass.name == name
            ):
                return klass
            if (
                klass.namespace
                == currentNamespace + "::" + currentClassName + "::" + namespace
                and klass.name == name
            ):
                return klass
        return None

    def findEnum(self, namespace, name, enums, currentNamespace, currentClassName):
        for enum in enums:
            if enum.namespace == namespace and enum.name == name:
                return enum
            if enum.namespace == currentClassName and enum.name == name:
                return enum
            if enum.namespace == currentNamespace and enum.name == name:
                return enum
            if (
                enum.namespace == currentNamespace + "::" + namespace
                and enum.name == name
            ):
                return enum
            if (
                enum.namespace == currentClassName + "::" + namespace
                and enum.name == name
            ):
                return enum
            if (
                enum.namespace
                == currentNamespace + "::" + currentClassName + "::" + namespace
                and enum.name == name
            ):
                return enum
        return None
