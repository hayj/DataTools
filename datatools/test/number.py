# coding: utf-8

from fr.hayj.util.number import *;
from fr.hayj.util.duration import *;

import unittest
import re

# The level allow the unit test execution to choose only the top level test 
unittestLevel = 1


if unittestLevel <= 1: 
    class UtilTest(unittest.TestCase):
        def test1(self):
            self.assertTrue(truncateFloat(0.00002000002, 2) == 0.00)
            self.assertTrue(truncateFloat(0.00002000002, 8) == 0.00002)
            self.assertTrue(truncateFloat(0.00002000002, 20) == 0.00002000002)
            self.assertTrue(truncateFloat(0.02, 8) == 0.02)
            self.assertTrue(truncateFloat(0.02, 1) == 0.0)
            self.assertTrue(truncateFloat(5e-5, 1) == 0.0)
            self.assertTrue(truncateFloat(5e-5, 10) == 0.00005)
           
