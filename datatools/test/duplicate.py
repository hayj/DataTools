# coding: utf-8
# pew in st-venv python /home/hayj/Workspace/Python/Utils/DataStructureTools/datastructuretools/test/duplicate.py

import os
import sys
sys.path.append('../')

import unittest
import doctest
import time
from systemtools.basics import *
from systemtools.location import *
from systemtools.file import *
from datatools import duplicate
from datatools.duplicate import *

# The level allow the unit test execution to choose only the top level test
min = 0
max = 10
assert min <= max

print("==============\nStarting unit tests...")

if min <= 0 <= max:
    class DocTest(unittest.TestCase):
        def testDoctests(self):
            """Run doctests"""
            doctest.testmod(duplicate)

if min <= 1 <= max:
    class Test1(unittest.TestCase):
        def test1(self):
            print("test1")
            d = Duplicate()
            self.assertTrue(not d.isDuplicate("a"))
            self.assertTrue(d.isDuplicate("a"))
            d = Duplicate(maxDuplicates=2,)
            self.assertTrue(not d.isDuplicate("a"))
            self.assertTrue(not d.isDuplicate("a"))
            self.assertTrue(d.isDuplicate("a"))

        def test2(self):
            print("test2")
            d = Duplicate(limit=3, cleanEachNAction=10000)
            self.assertTrue(not d.isDuplicate("a"))
            d.data.clean()
            self.assertTrue(d.isDuplicate("a"))
            d.data.clean()
            self.assertTrue(d.isDuplicate("a"))
            d.data.clean()
            self.assertTrue(d.isDuplicate("a"))
            d.data.clean()
            self.assertTrue(not d.isDuplicate("b"))
            d.data.clean()
            self.assertTrue(d.isDuplicate("b"))
            d.data.clean()
            self.assertTrue(not d.isDuplicate("c"))
            d.data.clean()
            self.assertTrue(d.isDuplicate("c"))
            d.data.clean()
            self.assertTrue(not d.isDuplicate("d"))
            d.data.clean()
            self.assertTrue(d.isDuplicate("d"))
            d.data.clean()
            self.assertTrue(not d.isDuplicate("a"))

        def test3(self):
            print("test3")
            d = Duplicate()
            self.assertTrue(not d.isDuplicate("a", "r"))
            self.assertTrue(not d.isDuplicate("a", "r"))
            self.assertTrue(not d.isDuplicate("a", "r"))
            self.assertTrue(d.isDuplicate("a", "t"))
            self.assertTrue(not d.isDuplicate("b", "t"))
            self.assertTrue(not d.isDuplicate("c", "t"))
            self.assertTrue(not d.isDuplicate("d", "t"))
            self.assertTrue(d.isDuplicate("a", "t"))
            self.assertTrue(d.isDuplicate("c", "r"))
            self.assertTrue(d.isDuplicate("c"))
            self.assertTrue(d.isDuplicate("c", "r"))

        def test4(self):
            print("test4")
            d = Duplicate()
            self.assertTrue(not d.isDuplicate([1, 2]))
            self.assertTrue(not d.isDuplicate([1, 2, 3]))
            self.assertTrue(d.isDuplicate([1, 2]))
            self.assertTrue(d.duplicateCount([1, 2]) == 2)
            self.assertTrue(d.isDuplicate([1, 2]))
            self.assertTrue(d.duplicateCount([1, 2]) == 3)

if __name__ == '__main__':
    unittest.main() # Or execute as Python unit-test in eclipse
    print("Unit tests done.\n==============")


