import os
import json
import time
import glob
from pathlib import Path

from systemtools.file import *


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
    jsonFilename = None

    key = 'f5j7z15j69e94xcn1glo78'

    def __init__(self, dataDir=None, filename = None, logger=None, verbose=False):

        """ Note: if verbose = True, data contained in filename WILL be displayed """

        self.logger = logger
        self.verbose = verbose
        self.dataDir = dataDir
        if filename:
            self.jsonFilename = filename
        if self.dataDir is None:
            self.dataDir = str(Path.home()) + "/.ssh/encrypted-data"
        mkdir(self.dataDir)
        self.cache = dict()

    def __encryptData(self, text, outputFilename):
        myMode = "encrypt"

        if (self.verbose):
            print('%sing...' % (myMode.title()))
        startTime = time.time()
        translated = encryptFile(outputFilename, self.key, text)
        totalTime = round(time.time() - startTime, 2)
        if self.verbose:
            print('%sion time: %s secondes' % (myMode.title(), totalTime))

    def __getitem__(self, key):
        if key not in self.cache:
            self.cache[key] = self.getDict(key)
        return self.cache[key]

    def getDict(self, filename = None):
        """
            :param:
                filename = The file in which the json data is contained. If no filename, uses the name given in Ctor.
            If no filename given in Ctor, throws exception

            If file has extension '.encrypted.zip', will be decrypted. If not, an encrypted copy will be made.

            :return:
                Dictionary containing data from .json file

            :example:
            >>>
            accessgetter = DataEncryptor("notEncryptedFile.json")
            dict = accessgetter.getDict() # Creates notEncryptedFile.encrypted.zip

            dict = accessgetter.getDict(".twitter.encrypted.zip")

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
                os.path.exists(self.dataDir + '/' + self.jsonFilename + ".encrypted.zip"):
            raise RuntimeError("DataEncryptor.getDict: failed to provide valid .json file to get Dict from")

        if os.path.exists(self.dataDir + '/' + self.jsonFilename + ".json"):
            jsonfile = open(self.dataDir + '/' + self.jsonFilename + ".json")
            self.jsonFilename = self.jsonFilename + ".json"
        else:
            jsonfile = open(self.dataDir + '/' + self.jsonFilename + ".encrypted.zip")
            self.jsonFilename = self.jsonFilename + ".encrypted.zip"

        if not self.jsonFilename.lower().endswith('.encrypted.zip'):
            name = os.path.splitext(self.dataDir + '/' + self.jsonFilename)[0]
            outputFileName = name + '.encrypted.zip'
            readString = jsonfile.read()
        else:
            print("Unciphering")
            outputFileName = self.jsonFilename
            readString = decryptFile(self.jsonFilename, self.key)

        if (self.verbose):
            print("File " + self.jsonFilename + " contains: \n" + readString)
        jsonfile.close()
        self.jsonDataDict = json.loads(readString)

        print("Final output file name")
        self.__encryptData(readString, outputFileName)
        return self.jsonDataDict

    def setPath(self, path):
        self.dataDir = path

    def seekJson(self):
        files = sorted(glob.glob(self.dataDir + "/*"))
        print(files)
        cnt = 0
        for filename in files:
            if filename.endswith(".encrypted.zip"):
                pass
            elif filename.endswith(".json"):
                cnt -= 1000
                handle = open(filename, 'r')
                text = handle.read()
                handle.close()
                self.__encryptData(text, filename)

        if cnt == 0:
            for filename in files:
                if filename.endswith(".encrypted.zip"):
                    print("Modifying " + filename)
                    handle = open(filename, "r")
                    text = decryptFile(handle.name, self.key)
                    print("Text found : ", text)
                    handle.close()
                    outputname = filename[:-len(".encrypted.zip")]
                    print("Outputfile : " + outputname)
                    outputhandle = open(outputname, "w+")
                    outputhandle.write(text)
                    outputhandle.close()


if __name__ == "__main__":
    de = DataEncryptor()
    de.seekJson()

