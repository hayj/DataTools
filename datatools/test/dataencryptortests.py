from unittest import TestCase
from lri import dataencryptor
from pathlib import Path


import os

print("======================\nStarting unit tests...")


class TestDataEncryptor(TestCase):

    def testInitDataEncryptor(self):
        self.assertIsNotNone(dataencryptor.DataEncryptor())
        self.assertIsNotNone(dataencryptor.DataEncryptor("Test.json"))

    def testGetDict(self):
        handle = open(str(Path.home()) + "/.ssh/encrypted-data/unittest.json", 'w+')
        handle.write("{\
    \"Test1\":\"Value1\",\
    \"Test2\":\"Value2\",\
    \"Test3\":\"AbsolutelyNotValue3\"}")
        handle.close()
        de = dataencryptor.DataEncryptor(filename="unittest")
        dict = de.getDict()

        self.assertIsNotNone(dict, "getDict() has returned None value")
        self.assertTrue(dict["Test3"] == "AbsolutelyNotValue3",
                        "Values contained in Dict weren't do not match expected results")

    def testSeekJsonScript(self):
        de = dataencryptor.DataEncryptor()
        if not os.path.isdir(de.dataDir + "/testFolder"):
            os.mkdir(de.dataDir + "/testFolder")

        de.setPath(de.dataDir + "/testFolder")
        for i in range(0, 4):
            handle = open(de.dataDir + "/test" + str(i) + ".json", 'w+')
            handle.write("Welcome to the test file")
            handle.close()

        de.seekJson() # Encrypt all .json files and delete them

        self.assertTrue(os.path.isfile(de.dataDir + "/test0.json.encrypted.zip"))
        self.assertTrue(os.path.isfile(de.dataDir + "/test1.json.encrypted.zip"))
        self.assertTrue(os.path.isfile(de.dataDir + "/test2.json.encrypted.zip"))
        self.assertTrue(os.path.isfile(de.dataDir + "/test3.json.encrypted.zip"))

        self.assertFalse(os.path.isfile(de.dataDir + "/test0.json"))
        self.assertFalse(os.path.isfile(de.dataDir + "/test1.json"))
        self.assertFalse(os.path.isfile(de.dataDir + "/test2.json"))
        self.assertFalse(os.path.isfile(de.dataDir + "/test3.json"))

        de.seekJson()

        self.assertTrue(os.path.isfile(de.dataDir + "/test0.json"))
        self.assertTrue(os.path.isfile(de.dataDir + "/test1.json"))
        self.assertTrue(os.path.isfile(de.dataDir + "/test2.json"))
        self.assertTrue(os.path.isfile(de.dataDir + "/test3.json"))


if __name__ == "__main__":
    t = TestDataEncryptor()

print("======================\nUnit tests done.")
