#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pygtk
from gi.repository import Gtk, GLib
import subprocess
import gobject
import os, signal, re
import random
import unicodedata as ud
import telnetlib

HOST = "127.0.0.1"


tn = telnetlib.Telnet(HOST, 32000)


#wordStr = u'pagrindinis meniu,prašau aktyvink pagrindinį meniu,prašau pagrindinį meniu, aktyvink pagrindinį meniu,visas ekranas,rodyk visame ekrane,normalus ekranas,grįžk iš viso ekrano,išjunk visą ekraną,įprastas ekranas'
#wordList = wordStr.split(u",")

class MySpawned(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self)
        self.set_default_size(1000,600)


        hbox = Gtk.HBox(spacing=6)
        self.add(hbox)

        #self.wordToSay = random.choice(wordList).encode("utf-8")
        self.wordHeard = u""
        #self.correctWords = 0
        #self.totalWords = 0

        self.label = Gtk.Label()
        self.label.set_markup('<span foreground="blue" size="xx-large">Spauskite: Pradėti</span>')
        self.label.set_justify(Gtk.Justification.LEFT)


        vb = Gtk.VBox(spacing=26)

        self.tw_out = Gtk.TextView()

        sw = Gtk.ScrolledWindow()
        vb.pack_start(sw, True, True, 0)
        sw.add(self.tw_out)

        self.tw_err = Gtk.TextView()

        sw = Gtk.ScrolledWindow()
        vb.pack_start(sw, True, True, 0)
        sw.add(self.tw_err)

        self.progress = Gtk.ProgressBar()
        vb.pack_start(self.progress, False, True, 0)

        bt = Gtk.Button(u'Pradėti')
        bt.connect('clicked', self.process)
        vb.pack_start(bt, False, False, 0)

        bt = Gtk.Button(u'Pabaiga')
        bt.connect('clicked', self.kill)
        vb.pack_start(bt, False, False, 0)

        self.add(hbox)
        hbox.add(self.label)
        hbox.pack_start(self.label, True, True, 0)
        hbox.add(vb)
        hbox.pack_start(vb, True, True, 0)
        #self.set_size_request(200, 300)
        self.connect('delete-event', Gtk.main_quit)
        self.show_all()

    def run(self):
        Gtk.main()

    def update_progress(self, data=None):
        self.progress.pulse()
        return True

    def kill(self, widget, data=None):
        os.kill(self.pid, signal.SIGTERM)

    def process(self, widget, data=None):
#         params = ['du', '--si', '/']
        params = ["pocketsphinx_continuous", '-hmm', "/home/mgreibus/src/liepa/mgreibus/impl/models/hmm/liepa.cd_semi_200",
              "-jsgf", "/home/mgreibus/src/liepa/mgreibus/impl/lm/browser-min.gram",
             "-dict", "/home/mgreibus/src/liepa/mgreibus/impl/models/dict/browser.dict"]
        def scroll_to_end(textview):
            i = textview.props.buffer.get_end_iter()
            mark = textview.props.buffer.get_insert()
            textview.props.buffer.place_cursor(i)
            textview.scroll_to_mark(mark, 0.0, True, 0.0, 1.0)


        def write_to_textview(io, condition, tw):
            if condition is GLib.IO_HUP:
                GLib.source_remove(self.source_id_out)
                GLib.source_remove(self.source_id_err)
                return False

            line = io.readline()
            tw.props.buffer.insert_at_cursor(line)
            scroll_to_end(tw)

            while Gtk.events_pending():
                Gtk.main_iteration_do(False)

            return True

        def write_to_textview_out(io, condition, tw):
            if condition is GLib.IO_HUP:
                GLib.source_remove(self.source_id_out)
                GLib.source_remove(self.source_id_err)
                return False

            line = io.readline()
            processLine(line);
            tw.props.buffer.insert_at_cursor(line)
            scroll_to_end(tw)

            while Gtk.events_pending():
                Gtk.main_iteration_do(False)

            return True

        def processLine(line):


            if re.search('READY...', line):
                    wh = self.wordHeard.lower()
                    #wts = self.wordToSay.lower()
                    recognitionRate = u"0"
                    #if self.totalWords > 0:
                    #     recognitionRate = u'teisingai %d iš %d' % (self.correctWords, self.totalWords)
                    label = u'<span foreground="green" size="xx-large">Pasakyta: '+wh.decode('UTF-8') + '</span>'
                    self.label.set_markup(label)

            else:
                match = re.search('^\d+: ([\s\wąčęėįšųūžĄČĘĖĮŠŲŪŽ]+)$', line)
                if not match is None:
                    #self.totalWords = self.totalWords +1
                    self.wordHeard = match.group(1)
                    wh = self.wordHeard.strip().lower()
                    if "važiuok aukščiau" == wh:
                        tn.write("window.scrollBy(0,-200);\n")
                    elif "važiuok žemiau" == wh :
                        tn.write("window.scrollBy(0,200);\n")  
                    if "važiuok į pradžią" == wh:
                        tn.write("window.scrollBy(0,-window.pageYOffset);\n")
                    elif "važiuok į galą" == wh :
                        tn.write("window.scrollTo(0,document.body.scrollHeight);;\n")            
                    elif "atverk kortelę" == wh :
                        tn.write("tab-new\n")            
                    elif "užverk kortelę" == wh :
                        tn.write("tab-close\n")  
                    elif "praeita kortelė" == wh :
                        tn.write("tab-prev\n")   
                    elif "tolimesnė kortelė" == wh :
                        tn.write("tab-next\n")   
                    elif "užverk visas korteles" == wh :
                        tn.write("closealltab\n")
                    elif "atverk naują langą" == wh :
                        tn.write("window-new\n")   
                    elif "atverk ieškos puslapį" == wh :
                        tn.write("tab-new http://online.lt/\n")   
                    elif "perkrauk tinklapį" == wh :
                        tn.write("location.reload();\n")                                                                          
                    elif "stabdyk krovimą" == wh :
                        tn.write("page-stop\n")      
                    elif "rodyk visame ekrane" == wh :
                        tn.write("fullscreen\n")                         
                    elif "rodyk įprastą ekraną" == wh :
                        tn.write("full-regular\n")    
                    elif "spausdink tinklapį" == wh :
                        tn.write("window.print()\n")           
                    elif "rodyk sportą" == wh :
                        tn.write("tab-new www.lrt.lt/sportas\n")     
                    elif "rodyk paštą naršyklėje" == wh :
                        tn.write("tab-new one.lt\n")                                                                            
                    elif "rodyk filmus" == wh :
                        tn.write("tab-new youtu.be\n")     
                    elif "rodyk muziką" == wh :
                        tn.write("tab-new rock.lt\n")                                                     
                    elif "rodyk naujienas" == wh :
                        tn.write("tab-new www.lrt.lt/naujienos\n")
                    elif "rodyk orus" == wh :
                        tn.write("tab-new meteo.lt\n")
                    elif "rodyk draugus" == wh :
                        tn.write("tab-new klase.lt\n")

                      
                        
                                      

                    #wts = self.wordToSay.strip().lower()

                    #print (wh, wts)         
                    #if ud.normalize('NFC', wh)  == ud.normalize('NFC',wts) :
                    #if wh  == wts :
                    #    self.correctWords = self.correctWords +1

                    #self.wordToSay = random.choice(wordList).encode('UTF-8')
                    #wts = self.wordToSay
                    #wts = wts.lower()
                    #recognitionRate = u'teisingai %d iš %d' % (self.correctWords, self.totalWords)
                    label = u'<span foreground="green" size="xx-large">Pasakyta: '+wh.decode('UTF-8') + '</span>'
                    self.label.set_markup(label)



        self.pid, stdin, stdout, stderr = GLib.spawn_async(params,
            flags=GLib.SpawnFlags.SEARCH_PATH|GLib.SpawnFlags.DO_NOT_REAP_CHILD,
            standard_output=True,
            standard_error=True)

        self.progress.set_text('Runnig du --si')

        io = GLib.IOChannel(stdout)
        err = GLib.IOChannel(stderr)

        self.source_id_out = io.add_watch(GLib.IO_IN|GLib.IO_HUP,
                                 write_to_textview_out,
                                 self.tw_out,
                                 priority=GLib.PRIORITY_HIGH)

        self.source_id_err = err.add_watch(GLib.IO_IN|GLib.IO_HUP,
                                 write_to_textview,
                                 self.tw_err,
                                 priority=GLib.PRIORITY_HIGH)

        timeout_id = GLib.timeout_add(100, self.update_progress)

        def closure_func(pid, status, data):
            GLib.spawn_close_pid(pid)
            GLib.source_remove(timeout_id)
            self.progress.set_fraction(0.0)

        GLib.child_watch_add(self.pid, closure_func, None)

if __name__ == '__main__':
    s = MySpawned()
    s.run()
