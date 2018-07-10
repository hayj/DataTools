import os
import json
from systemtools.file import *
from systemtools.basics import *
from systemtools.logger import *
from systemtools.location import *
from datatools.jsonreader import *

from datatools import config as dtConf

class DataEncryptor:
    def __init__\
    (
        self,
        dataDir=None,
        logger=None,
        verbose=True,
        encryptedExtension=".json.encrypted.zip",
        notEncryptedExtension=".json",
    ):
        """
            This class works like an API over you ~/.ssh/encrypted-data directory
            All files are the first key in you class instance, then you can access your encrypted data.
            By default the class will use your ~/.ssh/id_rsa.pub to encrypt/decrypt all your data.
        """
        # We store init data:
        self.encryptedExtension = encryptedExtension
        self.notEncryptedExtension = notEncryptedExtension
        self.encryptedExtensionSecondPart = self.encryptedExtension[len(self.notEncryptedExtension):]
        self.logger = logger
        self.verbose = verbose
        # We make the key:
        self.key = 'f5j7z15j69e94xcn1glo78'
        idRsaPubPath = homeDir() + "/.ssh/id_rsa.pub"
        if isFile(idRsaPubPath):
            idRsa = fileToStr(idRsaPubPath)
            self.key = idRsa + self.key
        self.key = md5(self.key)
        # We find the data dir:
        self.dataDir = dataDir
        if self.dataDir is None:
            self.dataDir = homeDir() + "/.ssh/encrypted-data"
        mkdir(self.dataDir)
        # Other params:
        self.notEncryptedPattern = self.dataDir + "/*" + self.notEncryptedExtension
        self.encryptedPattern = self.dataDir + "/*" + self.encryptedExtension
        self.data = None

    def __getData(self, dataname):
        """
            This function return the data in the file defined by  the given dataname:
            <dataname>.json.encrypted.zip
        """
        encryptedFilePath = self.dataDir + "/" + dataname + self.encryptedExtension
        notEncryptedFilePath = self.dataDir + "/" + dataname + self.notEncryptedExtension
        if isFile(encryptedFilePath) and not isFile(notEncryptedFilePath):
            decryptFile(encryptedFilePath, self.key, remove=False,
                        ext=self.encryptedExtensionSecondPart,
                        logger=self.logger, verbose=self.verbose)
            for i in range(10):
                if not isFile(notEncryptedFilePath):
                    sleep(0.1)
                    log("Waiting for " + dataname + " file decryption...")
            data = jsonToDict(notEncryptedFilePath)
            removeFile(notEncryptedFilePath)
            return data

    def encryptAll(self):
        """
            This function encrypt *.json files in the data dir
        """
        for current in sortedGlob(self.notEncryptedPattern):
            ext = self.encryptedExtensionSecondPart
            log("Encrypting " + current + "...", self)
            encryptFile(current, self.key,
                        ext=self.encryptedExtensionSecondPart,
                        remove=True,
                        logger=self.logger, verbose=self.verbose)

    def decryptAll(self):
        """
            This function decrypt *.json.encrypted.zip files in the data dir
        """
        for current in sortedGlob(self.encryptedPattern):
            ext = self.encryptedExtensionSecondPart
            log("Decrypting " + current + "...", self)
            decryptFile(current, self.key,
                        ext=self.encryptedExtensionSecondPart,
                        remove=True,
                        logger=self.logger, verbose=self.verbose)

    def __delitem__(self, dataname):
        if dataname in self.data:
            del self.data[dataname]

    def __getitem__(self, dataname):
        """
            The item access return the data from the file defined by the given key,
            if the key was not yet used, this function will load the data from the file
            and keep it definitively.
            If you want to reload the data in the file, just use `__delitem__` and re-access the data.
        """
        if self.data is None:
            self.data = dict()
        if dataname not in self.data:
            self.data[dataname] = self.__getData(dataname)
        return self.data[dataname]

def test1():
    de = DataEncryptor()
    printLTS(de["mongoauth"])
    for user in ["hayj", "student"]:
        printLTS(de["mongoauth"]["datascience01"][user])
    exit()

def toggleEncryption():
    de = DataEncryptor()
    if sortedGlob(de.notEncryptedPattern) > sortedGlob(de.encryptedPattern):
        de.encryptAll()
    else:
        de.decryptAll()


if __name__ == "__main__":
#     test1()
    toggleEncryption()




