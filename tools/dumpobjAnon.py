import os

from pycodeanalyzer.core.abstraction.objects import (
    AbstractObjectLanguage,
    AbstractClass,
    AbstractEnum,
    AbstractFunction,
    AbstractObject,
)
from pycodeanalyzer.core.json.pickler import Pickler

def main():
    pickler = Pickler()
    with open("dumpobj.json", "r+") as dataFile:
        text = dataFile.read()
        objectList = pickler.decode(text)
        for object in objectList:
            object.origin = object.origin.replace(os.getcwd().replace("\\", "/"), "").replace("\\", "/")
        dataFile.seek(0)
        text = pickler.encode(objectList)
        dataFile.write(text)
        dataFile.truncate()

if __name__ == "__main__":
    main()
