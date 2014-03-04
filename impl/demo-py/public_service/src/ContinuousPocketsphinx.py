'''
Created on Feb 23, 2014

@author: as
'''

from pocketsphinx import Decoder
import sphinxbase
import time
import os
import pyaudio
import subprocess
from Artificialintelligence import Artificialintelligence


class ContinuousPocketsphinx(object):
    '''
    classdocs
    '''
    CHUNK = 4096
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 16000
    #MODELDIR = "../models"
    MODELDIR = "/home/as/src/speech/sphinx/lt-pocketsphinx-tutorial/impl/models"

    decoder = None
    stream = None
    config = None
    ai = None



    def __init__(self):
        '''
        Constructor
        '''
        print ("[__init__]+++")

        # Create a decoder with certain model
        self.ai = Artificialintelligence()
        self.config = self.createConfig("code");
        self.decoder = Decoder(self.config);
        print ("[__init__] created decoder")
        #self.updateGrammar(self.decoder, "confirmation");

        print ("[__init__]---")

        p = pyaudio.PyAudio()

        self.stream = p.open(format=self.FORMAT,
                channels=self.CHANNELS,
                rate=self.RATE,
                input=True,
                frames_per_buffer=self.CHUNK)
        #Indicate listening for next utterance
        print ("READY....")

    def updateGrammar(self,pDecoder, pGramma):
        '''
        Update decoder language model from fsg file
        '''
        print ("[updateGrammar]+++" + pGramma)
        logmath = pDecoder.get_logmath();
        fsg = sphinxbase.FsgModel(os.path.join("../resource/", pGramma+'.fsg'), logmath, 7.5)
        #pDecoder.readfile(os.path.join("../resource/", pGramma+'.fsg'), logmath)
        pDecoder.set_fsg("default",fsg);
        pDecoder.set_search("default");
        print ("[updateGrammar]---")


    def createConfig(self,pGramma):
        print ("[createConfig]+++")
        config = Decoder.default_config()
        config.set_string('-hmm', os.path.join(self.MODELDIR, 'hmm/lt.cd_cont_200/'))
        config.set_string('-fsg', os.path.join("../resource/", pGramma+'.fsg'))
        #config.set_string('-jsgf', os.path.join("../resource/", pGramma+'.gram'))
        config.set_string('-dict', os.path.join("../resource/", 'service.dict'))
        print ("[createConfig]---")
        return config;

    def speak(self,text):
        print("Speak: ", text)
        if text is not None:
            aProcess = subprocess.Popen(['/home/as/bin/tark-win-lt', text], stderr=subprocess.STDOUT)
            out = aProcess.communicate()[0];
            time.sleep (0.100)
        print("ended Speak: ", out)


    def said(self, aiContext, text):
        print ("[said]+++", text)
        aiContext = self.ai.said(text, aiContext)
        print ('AI response: ',  aiContext.state, aiContext.response)
        self.speak(aiContext.response)
        if aiContext.interactiveStep is False :
            self.said(aiContext, text);
        print ("[said]---")
        return aiContext

    def recognized(self, pStream, pDecoder, aiContext):
        print ("[recognized]+++")
        pStream.stop_stream()
        pDecoder.end_utt()
        # Retrieve hypothesis.
        hypothesis = pDecoder.hyp()
        if hypothesis is not None:
            print ('Best hypothesis: ', hypothesis.uttid, hypothesis.best_score, hypothesis.hypstr)
            self.said(aiContext, hypothesis.hypstr)
            if aiContext.state in aiContext.GRAM:
                self.updateGrammar(pDecoder, aiContext.GRAM[aiContext.state]);
        elif (time.time() - aiContext.stateStarted) > 10:
            self.speak(aiContext.response)
            aiContext.stateStarted = time.time()
        print ("Time: ", (time.time() - aiContext.stateStarted))

        print("AI response ", aiContext.response)
        time.sleep (0.100)
        #Indicate listening for next utterance
        pStream.start_stream()
        pDecoder.start_utt(None)
        print ("READY....")
        print ("[recognized]---")
        return aiContext

    def run(self):
        '''
        Executor
        '''
        print("* start recording")
        self.decoder.start_utt(None)
        cur_vad_state = 0
        aiContext = self.ai.createContext();
        self.said(aiContext, None);
        while True:
            data = self.stream.read(self.CHUNK)
            time.sleep (0.100)
            #frames.append(data)
            self.decoder.process_raw(data, False, False)
            vad_state = self.decoder.get_vad_state()
            if vad_state and not cur_vad_state:
                #silence -> speech transition,
                #let user know that we heard
                print("Listening...\n")
            if not vad_state and cur_vad_state:
                #speech -> silence transition,
                #time to start new utterance
                aiContext = self.recognized(self.stream,self.decoder, aiContext);
                if aiContext.state == aiContext.STATE_THANKS:
                    break
            cur_vad_state = vad_state


if __name__ == "__main__":
    sphinx = ContinuousPocketsphinx();
    sphinx.run()