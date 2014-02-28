#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on Feb 27, 2014

@author: as
'''
import unittest
from Artificialintelligence import Artificialintelligence


class ArtificialintelligenceTest(unittest.TestCase):
    ai = None

    def setUp(self):
        self.ai = Artificialintelligence();
        pass


    def tearDown(self):
        pass


    def testTransformNumbers(self):
        response = self.ai.transformNumbers("VIENAS DU TRYS KETURI PENKI ŠEŠI SEPTYNI AŠTUONI DEVYNI NULIS")
        self.assertEqual("1234567890",response);
        pass

    def testSaidHapyPath(self):
        aiContext = self.ai.createContext()
        aiContext = self.ai.said("LABAS",aiContext)
        self.assertEqual(u"Pasakykite kodą iš 3 pavienių skaičių",aiContext.response);
        aiContext = self.ai.said("VIENAS DU TRYS",aiContext)
        self.assertEqual(u"Ar Jūs sakėte 123. Sakykite tesingai arba klaidingai",aiContext.response);
        aiContext = self.ai.said("TEISINGAI",aiContext)
        self.assertEqual(u"Pasakykite gimimo metus iš 4 pavienių skaičių",aiContext.response);
        aiContext = self.ai.said("VIENAS DEVYNI NULIS VIENAS",aiContext)
        self.assertEqual(u"Ar Jūs sakėte 1901. Sakykite tesingai arba klaidingai",aiContext.response);
        aiContext = self.ai.said("TEISINGAI",aiContext)
        self.assertEqual(u"Pasakykite kokios paslaugos ieškote",aiContext.response);
        aiContext = self.ai.said("KIEK MOKĖTI UŽ TURTĄ",aiContext)
        self.assertEqual(u"Ar Jūs sakėte. KIEK MOKĖTI UŽ TURTĄ? tesingai ar klaidingai",aiContext.response);
        aiContext = self.ai.said("TEISINGAI",aiContext)
        self.assertEqual(u"Greitu laiku Jums bus išsiųsta infomacija.",aiContext.response);
        aiContext = self.ai.said("DĖKUI",aiContext)
        self.assertEqual(u"Viso gero.",aiContext.response);
        pass

    def testCodeMissunderstood(self):
        aiContext = self.ai.createContext()
        aiContext.state = aiContext.STATE_VERIFY_CODE
        aiContext = self.ai.said("KLAIDINGAI",aiContext)
        self.assertEqual(aiContext.state,aiContext.STATE_ASK_CODE);
        pass

    def testYearMissunderstood(self):
        aiContext = self.ai.createContext()
        aiContext.state = aiContext.STATE_VERIFY_YEAR
        aiContext = self.ai.said("KLAIDINGAI",aiContext)
        self.assertEqual(aiContext.state,aiContext.STATE_ASK_YEAR);
        pass

    def testServiceMissunderstood(self):
        aiContext = self.ai.createContext()
        aiContext.state = aiContext.STATE_VERIFY_WHAT_SERVICE
        aiContext = self.ai.said("KLAIDINGAI",aiContext)
        self.assertEqual(aiContext.state,aiContext.STATE_ASK_WHAT_SERVICE);
        pass


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()