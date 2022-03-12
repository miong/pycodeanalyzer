class DependancyAnalyser:
    def analyze(self, klasses, enums, target):
        linkedClasses = []
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
                typeDeclaredNamespace, typeName, klasses, target.namespace
            )
            if linkedClass:
                linkedClasses.append(linkedClass)
        return (target, linkedClasses, [], [])

    def findClass(self, namespace, name, klasses, currentNamespace):
        for klass in klasses:
            if klass.namespace == namespace and klass.name == name:
                return klass
            if (
                klass.namespace == currentNamespace + "::" + namespace
                and klass.name == name
            ):
                return klass
        return None
