# coding: utf-8

from fr.hayj.util.text import *;
from fr.hayj.util.duration import *;

import unittest
import re

# The level allow the unit test execution to choose only the top level test 
unittestLevel = 5

if unittestLevel <= 1: 
    class UtilTest(unittest.TestCase):
        def setUp(self):
            pass
    
        def testStopWords(self):
            t1 = ['A', 'a', 'the', 'house', '.', 'yodsfb', '?', '#tHings', 'THE', '4'];
            result1 = removeStopWordsAndPunct(t1, lower=True);
            self.assertTrue(len(result1) == 4);
            
               
        def testNonASCII(self):
            s1 = "360° !";
            result1 = removeNonASCII(s1);
            self.assertTrue(result1 == "360 !");


        def testIsWord(self):
            self.assertTrue(not isWord('.'));
            self.assertTrue(isWord('dfg!df'));
            self.assertTrue(isWord('df51g'));
            self.assertTrue(not isWord(':;,;:$*'));
            self.assertTrue(isWord('1'));
            self.assertTrue(isWord('.1'));

        def testLemma(self):
            t = ['cats', 'dog', 'Cats']
            t = lemmatize(t)
            print(t)
            self.assertTrue(t[0] == 'cat')
            
            t = 'cats'
            t = lemmatize(t)
            self.assertTrue(t == 'cat')


if unittestLevel <= 2: 
    class TimeTest(unittest.TestCase):
        def testStopWords(self):
            t1 = ['A', 'a', 'the', 'house', '.', 'with', 'then', 'yodsfb', '?', '#tHings', 'THE', '4'];
             
            functions = [removeStopWords, removeStopWords2]
             
            for function in functions:
                tt = TicToc()
                tt.tic(function.__name__)
                for i in range(10000):
                    result1 = removeStopWords(t1)
                    self.assertTrue(len(result1) == 6)
                diffTimeSec = tt.toc(function.__name__)
                self.assertTrue(diffTimeSec > 3)
            
            t1 = removePunct(t1)
            t1 = toLower(t1)
             
            functions = [removeStopWordsAlreadyLowered]
             
            for function in functions:
                tt = TicToc()
                tt.tic(function.__name__)
                for i in range(10000):
                    result1 = removeStopWords(t1)
                    self.assertTrue(len(result1) == 4)
                diffTimeSec = tt.toc(function.__name__)
                self.assertTrue(diffTimeSec > 3)
                 
if unittestLevel <= 3: 
    class NumberTest(unittest.TestCase):
        def testNumber(self):
            self.assertTrue(isDigit("10"))
            self.assertTrue(not isDigit("10.0"))
            self.assertTrue(not isDigit("104g"))
            self.assertTrue(not isDigit("-104"))
            self.assertTrue(not isDigit("a104"))
                        
            
                 
if unittestLevel <= 4: 
    class ListToStrTest(unittest.TestCase):
        def testNumber(self):
            t = [{'a':'b', 'b':[2.0, {'r': [2.0, 3.0], 'i': None, 'w': [], "x": [[1, 2.0, True], [{}]]}]}, 1, 2, [1, 2], [True, False]]
            tStr = listToStr(t)
            print(tStr)
            print(len(re.findall('\n', tStr)))
            self.assertTrue(len(re.findall('\n', tStr)) == 25)
                       
           
                 
if unittestLevel <= 5: 
    class PunctTest3(unittest.TestCase):
        def test1(self):
            for current in ['(','.',',','-','?','!',';','_',':','{','}','[','/',']','...','"','\'',')']:
                self.assertTrue(isPunct(current))
            
            self.assertTrue(isPunct('££$$£'))
            self.assertTrue(not isPunct('#truc'))
            self.assertTrue(not isPunct('#x#'))
            self.assertTrue(isPunct('#@&'))
            self.assertTrue(not isPunct('42'))
            self.assertTrue(not isPunct('42_'))
           
           
if unittestLevel <= 6: 
    class PunctTest3(unittest.TestCase):
        def test1(self):
            self.assertTrue(not isDLS2015SwOrPunct2('42_'))
            self.assertTrue(isDLS2015SwOrPunct2('_'))
            self.assertTrue(isDLS2015SwOrPunct2('_'))
            self.assertTrue(isDLS2015SwOrPunct2("'s"))
            self.assertTrue(isDLS2015SwOrPunct2("'s"))
            self.assertTrue(not isDLS2015SwOrPunct2("job"))
           
