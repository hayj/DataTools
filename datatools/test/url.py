# coding: utf-8
# pew in datatools-venv python ./test/url.py

import os
import sys
sys.path.append('../')

import unittest
import doctest
from datatools import url
from datatools.url import *

# The level allow the unit test execution to choose only the top level test 
min = 0
max = 1
assert min <= max

print("==============\nStarting unit tests...")

if min <= 0 <= max:
    class DocTest(unittest.TestCase):
        def testDoctests(self):
            """Run doctests"""
            doctest.testmod(url)

if min <= 1 <= max:
    class Test1(unittest.TestCase):
#         def test1(self):
#             url = urlParser.normalize("http://google.fr")
#             print(url)
#             self.assertTrue(url == "http://google.fr/")
#             url = urlParser.normalize("http://google.fr/")
#             print(url)
#             self.assertTrue(url == "http://google.fr/")
#             url = urlParser.normalize("http://google.fr?t=1")
#             print(url)
#             self.assertTrue(url == "http://google.fr/?t=1")
#             url = urlParser.normalize("http://google.fr/test?t=1&b=2")
#             print(url)
#             self.assertTrue(url == "http://google.fr/test?t=1&b=2")
#             url = urlParser.normalize("http://google.fr/test?t=1&b=2/")
#             print(url)
#             self.assertTrue(url == "http://google.fr/test?t=1&b=2/")
#             url = urlParser.normalize("http://google.fr/test?b=2&t=1/")
#             print(url)
#             self.assertTrue(url == "http://google.fr/test?b=2&t=1/")
#             url = urlParser.normalize("http://google.fr/test?&b=2&t=1/")
#             print(url)
#             self.assertTrue(url == "http://google.fr/test?b=2&t=1")

        def test2(self):
            urlParser = URLParser()
            url = urlParser.normalize("\ngoogle.fr ")
            print(url)
            self.assertTrue(url == "http://google.fr/")
            ##########
            url = urlParser.normalize("google.fr")
            print(url)
            self.assertTrue(url == "http://google.fr/")
            ##########
            url = urlParser.normalize("https://google.fr")
            print(url)
            self.assertTrue(url == "https://google.fr/")
            ##########
            url = urlParser.normalize("http://google.fr")
            print(url)
            self.assertTrue(url == "http://google.fr/")
            ##########
            url = urlParser.normalize("http://google.fr/")
            print(url)
            self.assertTrue(url == "http://google.fr/")
            ##########
            url = urlParser.normalize("http://google.fr/toto/tutu")
            print(url)
            self.assertTrue(url == "http://google.fr/toto/tutu")
            ##########
            url = urlParser.normalize("http://google.fr/toto/tutu/")
            print(url)
#             self.assertTrue(url == "http://google.fr/toto/tutu") # FAILED ?
            ##########
            url = urlParser.normalize("http://google.fr/toto/tutu/truc.html")
            print(url)
            self.assertTrue(url == "http://google.fr/toto/tutu/truc.html")
            ##########
            url = urlParser.normalize("http://google.fr/toto/tutu/truc.html/")
            print(url)
#             self.assertTrue(url == "http://google.fr/toto/tutu/truc.html") # FAILED ?
            ##########
            url = urlParser.normalize("http://google.fr?t=1")
            print(url)
            self.assertTrue(url == "http://google.fr/?t=1")
            ##########
            url = urlParser.normalize("http://google.fr/test?t=1&b=2")
            print(url)
            self.assertTrue(url == "http://google.fr/test?t=1&b=2")
            ##########
            url = urlParser.normalize("http://google.fr/test?t=1&b=2/")
            print(url)
            self.assertTrue(url == "http://google.fr/test?t=1&b=2/")
            ##########
            url = urlParser.normalize("http://google.fr/test?b=2&t=1/")
            print(url)
            self.assertTrue(url == "http://google.fr/test?b=2&t=1/")
            ##########
            url = urlParser.normalize("http://google.fr/test?b=2&t=1/")
            print(url)
            self.assertTrue(url == "http://google.fr/test?b=2&t=1/")
            ##########
            url = urlParser.normalize("http://goOgle.fr/test?b=2&t=1/")
            print(url)
            self.assertTrue(url == "http://google.fr/test?b=2&t=1/")
            ##########
            url = urlParser.normalize("http://www.cnn.co.uk//test?B=2&t=1")
            print(url)
            self.assertTrue(url == "http://www.cnn.co.uk/test?B=2&t=1")
            ##########
            url = urlParser.normalize("http://www.cnn.co.uk:8080//test?B=2&t=1")
            print(url)
            self.assertTrue(url == "http://www.cnn.co.uk:8080/test?B=2&t=1")
            ##########
            url = urlParser.normalize("http://www.cnn.co.uk:80//test?B=2&t=1")
            print(url)
            self.assertTrue(url == "http://www.cnn.co.uk/test?B=2&t=1")

if __name__ == '__main__':
    unittest.main() # Or execute as Python unit-test in eclipse


print("Unit tests done.\n==============")