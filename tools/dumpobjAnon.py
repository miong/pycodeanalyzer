import jsonpickle
import os

from pycodeanalyzer.core.abstraction.objects import (
    AbstractObjectLanguage,
    AbstractClass,
    AbstractEnum,
    AbstractFunction,
    AbstractObject,
)

def main():
    jsonpickle.set_preferred_backend('simplejson')
    jsonpickle.set_encoder_options('simplejson', sort_keys=True, indent=4)
    with open("dumpobj.json", "r+") as dataFile:
        text = dataFile.read()
        objectList = jsonpickle.decode(text)
        for object in objectList:
            object.origin = object.origin.replace(os.getcwd().replace("\\", "/"), "").replace("\\", "/")
        dataFile.seek(0)
        text = jsonpickle.encode(objectList)
        dataFile.write(text)
        dataFile.truncate()

if __name__ == "__main__":
    main()
