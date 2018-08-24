# coding: utf-8
# pew in systemtools-venv python ./test/basics.py

import os
import sys
sys.path.append('../')

import unittest
import doctest
from datatools import jsonutils
from datatools.jsonutils import *

# The level allow the unit test execution to choose only the top level test
mini = 0
maxi = 9
assert mini <= maxi

print("==============\nStarting unit tests...")

if mini <= 0 <= maxi:
    class DocTest(unittest.TestCase):
        def testDoctests(self):
            """Run doctests"""
            doctest.testmod(jsonutils)

if mini <= 1 <= maxi:
    class Test1(unittest.TestCase):
        def test1(self):
            ndj = NDJson("a")
            self.assertTrue(ndj.getPath() == tmpDir() + "/a.bz2")

            ndj = NDJson("abc")
            self.assertTrue(ndj.getPath() == tmpDir() + "/abc.bz2")

            ndj = NDJson("abc", compresslevel=0)
            self.assertTrue(ndj.getPath() == tmpDir() + "/abc.ndjson")

            ndj = NDJson("a", compresslevel=0)
            self.assertTrue(ndj.getPath() == tmpDir() + "/a.ndjson")

            try:
                ndj = NDJson("a/b.bz2")
                self.assertTrue(False)
            except: pass

            ndj = NDJson("/a/b.bz2")

            try:
                ndj = NDJson("/a/b")
                self.assertTrue(False)
            except: pass

            try:
                ndj = NDJson("/a.bz2", "/", compresslevel=0)
                self.assertTrue(False)
            except: pass

            ndj = NDJson("a", tmpDir(), compresslevel=0)
            self.assertTrue(ndj.getPath() == "/home/hayj/tmp/a.ndjson")

            ndj = NDJson("a-a", tmpDir(), compresslevel=5)
            self.assertTrue(ndj.getPath() == "/home/hayj/tmp/a-a.bz2")

            ndj = NDJson("a-a.ndjson", tmpDir(), compresslevel=5)
            self.assertTrue(ndj.getPath() == "/home/hayj/tmp/a-a.ndjson")

            try:
                ndj = NDJson("a.bz2", tmpDir(), compresslevel=0)
                self.assertTrue(False)
            except: pass

            ndj = NDJson("a.bz2", compresslevel=6)
            self.assertTrue(ndj.getPath() == "/home/hayj/tmp/a.bz2")


if mini <= 2 <= maxi:
    class Test2(unittest.TestCase):
        def test1(self):
            for compresslevel in [0, 6, 9]:
                def objectYielder(amount=10):
                    for i in range(amount):
                        o = dict()
                        o[getRandomStr()] = getRandomStr()
                        yield o

                ndj = NDJson("a" + str(compresslevel), compresslevel=compresslevel)
                path = ndj.getPath()
                print(path)
                ndj.reset()
                self.assertTrue(not isFile(path))

                ndj.write({"a": 1})
                self.assertTrue(isFile(path))

                objects = []
                for i in range(10):
                    o = dict()
                    o[getRandomStr()] = getRandomStr()
                    objects.append(o)
                ndj.write(objects)

                self.assertTrue(len(list(ndj.readlines())) == 11)

                ndj.write(objectYielder())

                self.assertTrue(len(list(ndj.readlines())) == 21)


                ndj = NDJson(path, compresslevel=compresslevel)
                for current in ndj.readlines():
                    self.assertTrue(len(current.keys()) > 0)



                ndj = NDJson(path, compresslevel=compresslevel)
                for current in ndj.readlines():
                    print(str(current))
                    self.assertTrue(len(current.keys()) > 0)

                ndj.reset()
                self.assertTrue(len(list(ndj.readlines())) == 0)

                print("\n" * 2)


if __name__ == '__main__':
    unittest.main() # Orb execute as Python unit-test in eclipse


print("Unit tests done.\n==============")