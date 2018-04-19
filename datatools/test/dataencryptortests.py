from unittest import TestCase
import dataencryptor
from pathlib import Path
import os
import sys

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
        de = dataencryptor.DataEncryptor("unittest")
        dict = de.getDict()

        self.assertIsNotNone(dict, "getDict() has returned None value")
        self.assertTrue(dict["Test3"] == "AbsolutelyNotValue3",
                        "Values contained in Dict weren't do not match expected results")

    def testEncryption(self):
        de = dataencryptor.DataEncryptor()
        with open("./testencryption.json", "w+") as handle:
            handle.write("This is a test")
            handle.close()

        with open("./testencryption.json") as handle:
            de._DataEncryptor__encryptData(handle.read(), "./testencryption.encrypted.json")

            # Change the following statement
            # if the encryption method has been modified
        with open("./testencryption.encrypted.json") as handle:
            self.assertTrue(handle.read() == "T hai st eisst",
                            "Message \"This is a test\" was properly encrypted")

    def testSeekJsonScript(self):
        de = dataencryptor.DataEncryptor()
        if not os.path.isdir(de.path + "/testFolder"):
            os.mkdir(de.path + "/testFolder")

        de.setPath(de.path + "/testFolder")
        for i in range(0, 4):
            handle = open(de.path + "/test" + str(i) + ".json", 'w+')
            handle.write("Welcome to the test file")
            handle.close()

        de.seekJson() # Encrypt all .json files and delete them

        self.assertTrue(os.path.isfile(de.path + "/test0.encrypted.json"))
        self.assertTrue(os.path.isfile(de.path + "/test1.encrypted.json"))
        self.assertTrue(os.path.isfile(de.path + "/test2.encrypted.json"))
        self.assertTrue(os.path.isfile(de.path + "/test3.encrypted.json"))

        self.assertFalse(os.path.isfile(de.path + "/test0.json"))
        self.assertFalse(os.path.isfile(de.path + "/test1.json"))
        self.assertFalse(os.path.isfile(de.path + "/test2.json"))
        self.assertFalse(os.path.isfile(de.path + "/test3.json"))

        de.seekJson()

        self.assertTrue(os.path.isfile(de.path + "/test0.json"))
        self.assertTrue(os.path.isfile(de.path + "/test1.json"))
        self.assertTrue(os.path.isfile(de.path + "/test2.json"))
        self.assertTrue(os.path.isfile(de.path + "/test3.json"))

        os.remove(de.path + "/test0.json")
        os.remove(de.path + "/test0.encrypted.json")
        os.remove(de.path + "/test1.json")
        os.remove(de.path + "/test1.encrypted.json")
        os.remove(de.path + "/test2.json")
        os.remove(de.path + "/test2.encrypted.json")
        os.remove(de.path + "/test3.json")
        os.remove(de.path + "/test3.encrypted.json")


if __name__ == "__main__":
    t = TestDataEncryptor()

print("======================\nUnit tests done.")
