# coding: utf-8

from fr.hayj.util.shape import *;

import unittest

# The level allow the unit test execution to choose only the top level test 
unittestLevel = 1;

if unittestLevel <= 1: 
    class ShapeTest1(unittest.TestCase):
        def setUp(self):
            pass
    
        def testChunk(self):
            partsCount = 3
            for length in range(2, 100):
                chunkedList = chunkList(list(range(length)), partsCount)
                self.assertTrue(len(chunkedList) <= partsCount)

        def testCrossVal(self):
            for length in range(2, 100):
                for partsCount in range(2, 20):
                    data = list(range(length))
                    
                    (trainingSets, testSets) = crossValidationChunk(data, partsCount)
                    
                    okZero = False
                    okEnd = False
                    for i in range(len(trainingSets)):
                        for u in range(len(trainingSets[i])):
                            if trainingSets[i][u] == 0:
                                okZero = True
                            elif trainingSets[i][u] == length - 1:
                                okEnd = True
                    self.assertTrue(okZero)
                    self.assertTrue(okEnd)
                    
                    self.assertTrue(len(trainingSets) <= partsCount)
                    
                    for i in range(len(trainingSets)):
                        self.assertTrue(len(trainingSets[i]) + len(testSets[i]) == length)
        