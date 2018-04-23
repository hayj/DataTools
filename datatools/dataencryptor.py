import os
import json
import time
import glob
from pathlib import Path
from systemtools.location import *
from systemtools.basics import *



def encrypt(message, key):
    index = 0
    count = 0
    cipher = []

    for letter in message:
        cipher.append(message[index])
        index += int(key)

        if index > len(message) - 1:
            count += 1
            index = count
    return ''.join(cipher)


def decrypt(cipher, key):
    message = [''] * len(cipher)
    index = 0
    count = 0

    for letter in cipher:
        message[index] = letter
        index += int(key)
        if index > len(cipher) - 1:
            count += 1
            index = count

    return ''.join(message)


class DataEncryptor:
    targetFile = None
    jsonDataDict = None
    jsonFilename = ".projectData.json"

    # key = 'mDn5S2JoGGMVw5CkfmBtNRV_dYfhLqNByesoPZhJVuQ='
    # TODO: Use this base64 encoded string as key when upgrading encryption program

    def __init__(self, dataDir=None, logger=None, verbose=False):

        """ Note: if verbose = True, data contained in filename WILL be displayed """

        self.logger = logger
        self.verbose = verbose
        self.dataDir = dataDir
        if self.dataDir is None:
            self.dataDir = str(Path.home()) + "/.ssh/encrypted-data"
        mkdir(self.dataDir)
        self.cache = dict()

    def __encryptData(self, text, outputFilename):
        myMode = "encrypt"
        outputFile = open(outputFilename, 'w+')

        if (self.verbose):
            print('%sing...' % (myMode.title()))
        startTime = time.time()
        translated = encrypt(text, 7)
        totalTime = round(time.time() - startTime, 2)
        if (self.verbose):
            print('%sion time: %s secondes' % (myMode.title(), totalTime))
        outputFile.write(translated)
        outputFile.close()

    def __getitem__(self, key):
        if key not in self.cache:
            self.cache[key] = self.getDict(key)
        return self.cache[key]

    def getDict(self, filename):
        """
            :param:
                filename = The file in which the json data is contained. If no filename, uses the name given in Ctor.
            If no filename given in Ctor, throws exception

            If file has extension '.encrypted.json', will be decrypted. If not, an encrypted copy will be made.

            :return:
                Dictionary containing data from .json file

            :example:
            >>>
            accessgetter = DataEncryptor("notEncryptedFile.json")
            dict = accessgetter.getDict() # Creates notEncryptedFile.encrypted.json

            dict = accessgetter.getDict(".twitter.encrypted.json")

            Note: DataEncryptor.filename is replaced when calling getDict with a filename
        """
        if filename:
            self.jsonFilename = filename
            self.jsonDataDict = None
            filename = filename.lower()
        elif not filename and not self.jsonDataDict and not self.jsonFilename:
            raise RuntimeError("DataEncryptor.getDict: failed to provide valid .json file to get Dict from")
        if self.jsonDataDict:
            return self.jsonDataDict
        else:
            return self.__getDictFromJson()

    def __getDictFromJson(self):
        if not os.path.exists(self.dataDir + '/' + self.jsonFilename + ".json") and not\
                os.path.exists(self.dataDir + '/' + self.jsonFilename + ".encrypted.json"):
            raise RuntimeError("DataEncryptor.getDict: failed to provide valid .json file to get Dict from")

        if os.path.exists(self.dataDir + '/' + self.jsonFilename + ".json"):
            jsonfile = open(self.dataDir + '/' + self.jsonFilename + ".json")
            self.jsonFilename = self.jsonFilename + ".json"
        else:
            jsonfile = open(self.dataDir + '/' + self.jsonFilename + ".encrypted.json")
            self.jsonFilename = self.jsonFilename + ".encrypted.json"

        if not self.jsonFilename.lower().endswith('.encrypted.json'):
            name = os.path.splitext(self.dataDir + '/' + self.jsonFilename)[0]
            outputFileName = name + '.encrypted.json'
            readString = jsonfile.read()
        else:
            print("Unciphering")
            outputFileName = self.jsonFilename
            readString = decrypt(jsonfile.read(), 7)

        if (self.verbose):
            print("File " + self.jsonFilename + " contains: \n" + readString)
        jsonfile.close()
        self.jsonDataDict = json.loads(readString)

        self.__encryptData(readString, outputFileName)
        return self.jsonDataDict

    def setPath(self, path):
        self.dataDir = path

    def seekJson(self):
        files = sorted(glob.glob(self.dataDir + "/*"))
        print(files)
        cnt = 0
        for filename in files:
            if filename.endswith(".encrypted.json"):
                pass
            elif filename.endswith(".json"):
                cnt -= 1000
                handle = open(filename, 'r')
                text = handle.read()
                handle.close()
                outputname = filename.replace(".json", ".encrypted.json")
                self.__encryptData(text, outputname)
                os.remove(filename)

        if cnt == 0:
            for filename in files:
                if filename.endswith(".encrypted.json"):
                    print("Modifying " + filename)
                    handle = open(filename, "r")
                    text = decrypt(handle.read(), 7)
                    print("Text found : ", text)
                    handle.close()
                    outputname = filename.replace(".encrypted.json", ".json")
                    print("Outputfile : " + outputname)
                    outputhandle = open(outputname, "w+")
                    outputhandle.write(text)
                    outputhandle.close()


# TODO: Code a better encryption/decryption system
# TODO: Write doc/comments
# TODO: Import datatools for Logger, replace prints with log(..., self)
# TODO: Unit testing via template https://github.com/hayj/SystemTools/blob/master/systemtools/test/basics.py


if __name__ == "__main__":
    de = DataEncryptor()
    de.seekJson()



