# coding: utf-8

from fr.hayj.util.parser import *;


import unittest

# The level allow the unit test execution to choose only the top level test 
unittestLevel = 1;

if unittestLevel <= 2: 
    class KwargsTest(unittest.TestCase):
        def setUp(self):
            pass
    
        def test1(self):
            data = {'toto': (1, 2), 'titi': (3, 4)}
            
            sp = SerializableParser(fileId="testKwargs1", verbose=True, autoSerialize=False);
            sp.clean();
            for (key, (score1, score2)) in list(data.items()):
                sp.parse(key, self.parseFunct1, score1, score2)
            sp.serializeIfChanged()
            
            self.assertTrue(sp.getOne('toto') == 'toto3')
            self.assertTrue(sp.getOne('titi') == 'titi7')
            
            sp.setAutoSerialize(True)
            data['tutu'] = (10, 11)
            sp.parseAll(list(data.keys()), self.parseFunct1, data)
            self.assertTrue(sp.getOne('toto') == 'toto3')
            self.assertTrue(sp.getOne('titi') == 'titi7')
            self.assertTrue(sp.getOne('tutu') == 'tutu21')
            
        def parseFunct1(self, sentence, score1, score2):
            return sentence + str(score1 + score2)
        
        def test2(self):
            data = {'toto': {'score1': 1, 'score2': 2}, 'titi': {'score1': 3, 'score2': 4}}
            
            sp = SerializableParser(fileId="testKwargs1", verbose=True, autoSerialize=False);
            sp.clean();
            for (key, params) in list(data.items()):
                sp.parse(key, self.parseFunct2, **params)
            sp.serializeIfChanged()
            
            self.assertTrue(sp.getOne('toto') == 'toto3')
            self.assertTrue(sp.getOne('titi') == 'titi7')
            
            sp.setAutoSerialize(True)
            data['tutu'] = {'score1': 10, 'score2': 11}
            sp.parseAll(list(data.keys()), self.parseFunct2, data)
            self.assertTrue(sp.getOne('toto') == 'toto3')
            self.assertTrue(sp.getOne('titi') == 'titi7')
            self.assertTrue(sp.getOne('tutu') == 'tutu21')
        
        def parseFunct2(self, sentence, **kwargs):
            score1 = kwargs['score1']
            score2 = kwargs['score2']
            return sentence + str(score1 + score2)    
            
        def test3(self):
            data = {'toto': {'score1': 1, 'score2': 2}, 'titi': {'score1': 3, 'score2': 4}}
            
            sp = SerializableParser(fileId="testKwargs1", verbose=True, autoSerialize=False);
            sp.clean();
            for (key, params) in list(data.items()):
                sp.parse(key, self.parseFunct3, **params)
            sp.serializeIfChanged()
            
            self.assertTrue(sp.getOne('toto') == 'toto3')
            self.assertTrue(sp.getOne('titi') == 'titi7')
            
            sp.setAutoSerialize(True)
            data['tutu'] = {'score1': 10, 'score2': 11}
            sp.parseAll(list(data.keys()), self.parseFunct3, data)
            self.assertTrue(sp.getOne('toto') == 'toto3')
            self.assertTrue(sp.getOne('titi') == 'titi7')
            self.assertTrue(sp.getOne('tutu') == 'tutu21')
        
        def parseFunct3(self, sentence, score1=None, score2=None):
            print(score1)
            print(score2)
            return sentence + str(score1 + score2)


if unittestLevel <= 1: 
    class SerializableParserTest(unittest.TestCase):
        def setUp(self):
            s1 = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j"];
            s1 += list(s1);
            self.sentences = s1;
    
        def test1(self):
            self.assertTrue(len(self.sentences) == 20);
            sp = SerializableParser(fileId="test1", percentEach=1, verbose=False);
            sp.clean();
            sp.parseAll(self.sentences, self.parserFunct);
            temp1 = sp.parse("a", self.parserFunct);
            self.assertTrue(temp1 == "a");
            sp2 = SerializableParser(fileId="test1", percentEach=1, verbose=False);
            self.assertTrue(temp1 == sp2.getOne("a"));
            sp.clean();
        
        def parserFunct(self, sentence):
            return sentence;
        
        def testParseAll(self):
            sentences = [];
            import random;
            for i in range(2002):
                sentences.append(str(random.random()));
            sp = SerializableParser(fileId="test2", verbose=False);
            sp.parseAll(sentences, self.parserFunct);
            
            sp2 = SerializableParser(fileId="test2", verbose=False);
            for sentence in sentences:
                self.assertTrue(sentence in sp2.hm);
            
            sp.clean();
        
        def testParseAll2(self):
            import os.path, time
            sentences = [];
            import random;
            for i in range(2002):
                sentences.append(str(random.random()));
            sp = SerializableParser(fileId="test3", verbose=False);
            sp.clean()
            sp.parseAll(sentences, self.parserFunct);
            
            filePath = sp.filePath
            mTime = time.ctime(os.path.getmtime(filePath))
            print(mTime)
            
            time.sleep(1)
            sp = SerializableParser(fileId="test3", verbose=False);
            sp.parseAll(sentences, self.parserFunct);
            mTime2 = time.ctime(os.path.getmtime(filePath))
            print(mTime2)
            self.assertTrue(mTime == mTime2)
            
            time.sleep(1)
            sentences.insert(0, "yo")
            sp = SerializableParser(fileId="test3", verbose=False);
            sp.parseAll(sentences, self.parserFunct);
            mTime3 = time.ctime(os.path.getmtime(filePath))
            print(mTime3)
            self.assertTrue(mTime != mTime3)
            

            
            












