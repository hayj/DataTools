import json
from enum import Enum
import bz2
import re
from systemtools.logger import *
from systemtools.basics import *
from systemtools.location import enhanceDir

class JsonReader():
    ROOT_TYPE = Enum('ROOT_TYPE', 'objects list')
    def __init__(self, filePaths, readerFunct=open,
                 skipDecodeError=True, logger=None, verbose=True):
        assert filePaths is not None
        if not isinstance(filePaths, list):
            filePaths = [filePaths]
        assert len(filePaths) > 0
        self.filePaths = filePaths
        self.skipDecodeError = skipDecodeError
        self.logger = logger
        self.verbose = verbose
        self.readerFunct = readerFunct
        self.filePath = self.filePaths[0]
        if re.match("^.*\.bz2$", self.filePath):
            self.readerFunct = bz2.BZ2File
        self.firstChar = None
        self.rootType = None
        with self.readerFunct(self.filePath) as f:
            self.firstChar = (f.read(1))
            self.firstChar = byteToStr(self.firstChar)
        if self.firstChar is not None:
            if self.firstChar == '{':
                self.rootType = JsonReader.ROOT_TYPE.objects
            else:
                self.rootType = JsonReader.ROOT_TYPE.list
    def log(self, text):
        if self.logger is not None:
            self.logger.info(text)
        else:
            print(text)
    def loads(self, data):
        try:
            return json.loads(data, strict=False)
        except ValueError as e:
            if self.skipDecodeError:
                logException(e, self, message='Decoding this json has failed:\n' + data)
            else:
                raise e
            return None
    def __iter__(self):
        for filePath in self.filePaths:
            with self.readerFunct(filePath) as f:
                if self.rootType == JsonReader.ROOT_TYPE.objects:
                    for line in f:
                        line = byteToStr(line)
                        line = line.strip()
                        if len(line) > 0:
                            result = self.loads(line)
                            if result is not None:
                                yield result
                else:
                    data = f.read()
                    data = byteToStr(data)
                    if len(data) > 0:
                        jsonData = self.loads(data)
                        if jsonData is not None:
                            for current in jsonData:
                                if current is not None:
                                    yield current


def toJsonString(data):
#     strResult = json.dumps(data, indent=4, sort_keys=True).decode('unicode-escape').encode('utf8')
    strResult = json.dumps(data, indent=4, sort_keys=True)
    return strResult

def objectToJsonStr(dictOrList):
    return json.dumps(dictOrList)

def dictOrListToJSON(filename, data, folder="./output/"):
    folder = enhanceDir(folder)
    if not isinstance(data, list):
        data = dictOfListToListOfDict(data)
#     strResult = json.dumps(data, indent=4, sort_keys=True).decode('unicode-escape').encode('utf8')
    strResult = json.dumps(data, indent=4, sort_keys=True)
    with open(folder + filename + ".json", "w") as jsonFile:
        jsonFile.write(strResult)

def dictOrListToJsonBz2(filename, data, folder="./output/", compresslevel=1):
    folder = enhanceDir(folder)
    if not isinstance(data, list):
        data = dictOfListToListOfDict(data)
#     strResult = json.dumps(data, indent=4, sort_keys=True).decode('unicode-escape').encode('utf8')
    strResult = json.dumps(data, indent=4, sort_keys=True)
    strResult = bytes(strResult, 'utf-8')
    strResultCompressed = bz2.compress(strResult, compresslevel=compresslevel)
    with open(folder + filename + ".json.bz2", "wb") as jsonFile:
        jsonFile.write(strResultCompressed)

def jsonListToLineJsonBz2(filename, data, folder="./output/", compresslevel=1):
    folder = enhanceDir(folder)
    strResult = ""
    for current in data:
        strResult += json.dumps(current, indent=None, sort_keys=True) + "\n"
    strResult = bytes(strResult, 'utf-8')
    strResultCompressed = bz2.compress(strResult, compresslevel=compresslevel)
    with open(folder + filename + ".json.bz2", "wb") as jsonFile:
        jsonFile.write(strResultCompressed)

def toJsonFile(filename, data, folder="./output/"):
    folder = enhanceDir(folder)
    with open(folder + filename, 'w') as f:
        json.dump(data, f, indent=4, sort_keys=True)

def jsonToDict(jsonText):
    if jsonText is None:
        return None
    return json.loads(jsonText)

def jsonToList(filename, folder="./data/"):
    folder = enhanceDir(folder)
    with open(folder + filename + '.json') as dataFile:
        data = json.load(dataFile)
        return data
    return None


def jsonFileToObject(path):
    with open(path) as data:
        data = jsonToObject(data)
    return data

def jsonToObject(text):
    return json.load(text)



def jsonTest():
    o1 = {"message": "Hello1", "data": [0, {}]}
    o2 = ["Hello1", [0, {}]]

    print(listToStr(o1))
    print(listToStr(o2))

    o1 = objectToJsonStr(o1)
    o2 = objectToJsonStr(o2)

    print(listToStr(o1))
    print(listToStr(o2))






