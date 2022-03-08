class IdentityAnalyser:

    def __init__(self):
        self.mapping = {}
        self.mapping["Classes"] = []
        self.mapping["Enums"] = []

    def analyze(self, objects):
        for object in objects:
            if object.type == "Class":
                self.mapping["Classes"].append(object)
            elif object.type == "Enum":
                self.mapping["Enums"].append(object)


    def getClasses(self):
        return self.mapping["Classes"]

    def getEnums(self):
        return self.mapping["Enums"]
