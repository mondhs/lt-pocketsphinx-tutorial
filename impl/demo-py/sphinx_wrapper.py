#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pygtk
from gi.repository import Gtk, GLib
import subprocess
import gobject
import os, signal, re
import random

wordStr = u'Būti,Kuris,Galėti,Visas,Kaip,Lietuva,Kitas,Turėti,Savas,Darbas,Žmogus,Metai,Labai,Vienas,Nebūti,Reikėti,Žinoti,Didelis,Tačiau,Teisė,Laikas,Diena,Dabar,Pagal,Valstybė,Jeigu,Respublika,Nustatyti,Dalis,Įstatymas,Straipsnis,Įmonė,Žodis,Norėti,Kalba,Šalis,Sudaryti,Asmuo,Naujas,Sistema,Sakyti,Todėl,Kartas,Gauti,Aukštas,Žemė,Metas,Vieta,Niekas,Įvairus,Lietuviai,Svarbus,Vaikas,Gerai,Prieš,Tarp,Dažnai,Skirti,Veikla,Eiti,Atlikti,Pasakyti,Gyventi,Priimti,Valstybinis,Mokslas,Akis,Geras,Atvejis,Dirbti,Antras,Mažas,Miestas,Ranka,Bendras,Įstaiga,Mokykla,Teismas,Kalbėti,Forma,Bankas,Tada,Kultūra,Sąlyga,Viskas,Tyrimas,Vanduo,Matyti,Grupė,Priemonė,Vyriausybė,Būdas,Naudoti,Medžiaga,Nors,Procesas,Pasaulis,Ūkis,Kiek,Rašyti,Nulis,Du,Trys,Keturi,Penki,Šeši,Septyni,Aštuoni,Devyni,Pradžia,Pabaiga'
wordList = wordStr.split(u",")

class MySpawned(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self)
        self.set_default_size(1000,600)


        hbox = Gtk.HBox(spacing=6)
        self.add(hbox)

        self.wordToSay = random.choice(wordList).encode("utf-8")
        self.wordHeard = u""
        self.correctWords = 0
        self.totalWords = 0

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
#        params = ["pocketsphinx_continuous", '-hmm', "../models/hmm/lt.cd_cont_200/", "-jsgf", "../models/lm/robotas.gram", "-dict", "../models/dict/robotas.dict"]
        params = ["/home/mgreibus/src/speech/sphinx/lt-pocketsphinx-tutorial/impl/demo-py/robotas_mic_ps.py"]
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
                    wts = self.wordToSay.lower()
                    recognitionRate = u"0"
                    if self.totalWords > 0:
                         recognitionRate = u'%.2f' % (self.correctWords/self.totalWords)
                    label = u'<span foreground="green" size="xx-large">Pasakyta: '+wh.decode('UTF-8') +u'</span>\n'
                        #u'<span foreground="blue" size="xx-large">Sakyk: '+wts.decode('UTF-8')+u'</span>\n'+
                        #u'<span foreground="green">Atpažinta: '+ recognitionRate +u'</span>'
                    self.label.set_markup(label)

            else:
                match = re.search('\d+: ([\w()ąčęėįšųūž]+)', line.lower())
                if not match is None:
                    self.totalWords = self.totalWords +1
                    self.wordHeard = match.group(1)
                    wh = self.wordHeard.lower()
                    wts = self.wordToSay.lower()

                    if wh  == wts :
                        self.correctWords = self.correctWords +1

                    self.wordToSay = random.choice(wordList).encode('UTF-8')
                    wts = self.wordToSay
                    wts = wts.lower()
                    recognitionRate = u'%.2f' % (self.correctWords/self.totalWords)
                    label = u'<span foreground="green" size="xx-large">Pasakyta: '+wh.decode('UTF-8') +u'</span>\n'
                        #u'<span foreground="blue" size="xx-large">Sakyk: '+wts.decode('UTF-8')+u'</span>\n'+
                        #u'<span foreground="green">Atpažinta: '+ recognitionRate +u'</span>'
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
