#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Created on Feb 27, 2014

@author: as
'''
import logging as logging
import time
import re


class Artificialintelligence(object):
    '''
    classdocs
    '''

    def __init__(self):
        '''
        Constructor
        '''
        logging.basicConfig(format='%(asctime)s %(message)s', level=logging.INFO)
        logging.info("AI initialised")

    def transformNumbers(self, stringWitNumbers):
        logging.info("transformNumbers %s", stringWitNumbers)
        if stringWitNumbers is None:
            return stringWitNumbers
        response = stringWitNumbers
        response = re.sub(r'VIENAS\s*', "1", response)
        response = re.sub(r'DU\s*', "2", response)
        response = re.sub(r'TRYS\s*', "3", response)
        response = re.sub(r'KETURI\s*', "4", response)
        response = re.sub(r'PENKI\s*', "5", response)
        response = re.sub(r'ŠEŠI\s*', "6", response)
        response = re.sub(r'SEPTYNI\s*', "7", response)
        response = re.sub(r'AŠTUONI\s*', "8", response)
        response = re.sub(r'DEVYNI\s*', "9", response)
        response = re.sub(r'NULIS\s*', "0", response)
        return response

    def createContext(self):
        aiContext = AiContext();
        aiContext.state = aiContext.STATE_INIT
        aiContext.interactiveStep = False
        aiContext.stateStarted = time.time()
        aiContext.response = AiContext.MSG[aiContext.state]
        return aiContext;

    def eq(self, a, b):
        try:
            return a.upper().decode('utf-8') == b.upper().decode('utf-8')
        except AttributeError:
            return a == b

    def updateState(self, aiContext, state):
        aiContext.stateStarted = time.time()
        aiContext.state = state
        return aiContext

    def said(self, said, aiContext):
        logging.info("said %s", said)
        said = self.transformNumbers(said)
        aiContext.interactiveStep = True
        if(aiContext.state == aiContext.STATE_INIT):
            self.updateState(aiContext, aiContext.STATE_HI);
            aiContext.response = AiContext.MSG[aiContext.state]
            aiContext.interactiveStep = False
        elif(aiContext.state == aiContext.STATE_HI):
            self.updateState(aiContext, aiContext.STATE_ASK_CODE)
            aiContext.response = AiContext.MSG[aiContext.state]
        elif(aiContext.state == aiContext.STATE_ASK_CODE):
            self.updateState(aiContext, aiContext.STATE_VERIFY_CODE)
            aiContext.response = AiContext.MSG[aiContext.state].format(said);
        elif(aiContext.state == aiContext.STATE_VERIFY_CODE):
            if(self.eq(said, "teisingai")):
                self.updateState(aiContext, aiContext.STATE_ASK_YEAR)
                aiContext.response = AiContext.MSG[aiContext.state]
            elif(self.eq(said, "klaidingai")):
                self.updateState(aiContext, aiContext.STATE_ASK_CODE)
                aiContext.response = AiContext.MSG[aiContext.state]
        elif(aiContext.state == aiContext.STATE_ASK_YEAR):
                self.updateState(aiContext, aiContext.STATE_VERIFY_YEAR)
                aiContext.response = AiContext.MSG[aiContext.state].format(said);
        elif(aiContext.state == aiContext.STATE_VERIFY_YEAR):
            if(self.eq(said, "teisingai")):
                self.updateState(aiContext, aiContext.STATE_ASK_WHAT_SERVICE)
                aiContext.response = AiContext.MSG[aiContext.state]
            elif(self.eq(said, "klaidingai")):
                self.updateState(aiContext, aiContext.STATE_ASK_YEAR)
                aiContext.response = AiContext.MSG[aiContext.state]
        elif(aiContext.state == aiContext.STATE_ASK_WHAT_SERVICE):
                self.updateState(aiContext, aiContext.STATE_VERIFY_WHAT_SERVICE)
                aiContext.response = AiContext.MSG[aiContext.state].format(said);
        elif(aiContext.state == aiContext.STATE_VERIFY_WHAT_SERVICE):
            if(self.eq(said, "teisingai")):
                self.updateState(aiContext, aiContext.STATE_NOTIFY_SERVICE_ORDERED)
                aiContext.response = AiContext.MSG[aiContext.state]
            elif(self.eq(said, "klaidingai")):
                self.updateState(aiContext, aiContext.STATE_ASK_WHAT_SERVICE)
                aiContext.response = AiContext.MSG[aiContext.state]
        elif(aiContext.state == aiContext.STATE_NOTIFY_SERVICE_ORDERED):
            self.updateState(aiContext, aiContext.STATE_THANKS)
            aiContext.interactiveStep = False
            aiContext.response = AiContext.MSG[aiContext.state]
        elif(aiContext.state == aiContext.STATE_THANKS):
            aiContext.interactiveStep = False
            self.updateState(aiContext, aiContext.STATE_HI)
            aiContext.response = AiContext.MSG[aiContext.state]



        return aiContext

class AiContext(object):
    STATE_INIT = -2
    STATE_HI = -1
    STATE_ASK_CODE = 0
    STATE_VERIFY_CODE = 1
    STATE_ASK_YEAR = 2
    STATE_VERIFY_YEAR = 3
    STATE_ASK_WHAT_SERVICE = 4
    STATE_VERIFY_WHAT_SERVICE = 5
    STATE_NOTIFY_SERVICE_ORDERED = 6
    STATE_THANKS = 7
    STATE_FINISH = 8


    GRAM = {
            STATE_ASK_CODE: "code",
            STATE_VERIFY_CODE: "confirmation",
            STATE_ASK_YEAR: "year",
            STATE_VERIFY_YEAR: "confirmation",
            STATE_ASK_WHAT_SERVICE: "service_request",
            STATE_VERIFY_WHAT_SERVICE: "confirmation",
            STATE_NOTIFY_SERVICE_ORDERED:"request_submited"
            }

    MSG = {
           STATE_INIT: None,
           STATE_HI: u"Sveiki. Mano vardas Liepa. Prašau prisistatykite.",
           STATE_ASK_CODE:u"Pasakykite kodą iš trijų pavienių skaičių.",
           STATE_VERIFY_CODE:u"Ar Jūs sakėte {0}. Sakykite tesingai arba klaidingai.",
           STATE_ASK_YEAR: "Pasakykite gimimo metus iš keturių pavienių skaičių.",
           STATE_VERIFY_YEAR:u"Ar Jūs sakėte {0}. Sakykite tesingai arba klaidingai.",
           STATE_ASK_WHAT_SERVICE:u"Pasakykite kokios paslaugos ieškote.",
           STATE_VERIFY_WHAT_SERVICE:u"Ar Jūs sakėte. {0}? tesingai ar klaidingai.",
           STATE_NOTIFY_SERVICE_ORDERED: u"Greitu laiku Jums bus išsiųsta infomacija.",
           STATE_THANKS: u"Viso gero.",
           STATE_FINISH: None
    }

    state = None
    stateStarted = None
    interactiveStep = None
    response = None

    def __init__(self):
            logging.info("AI context initialised")

