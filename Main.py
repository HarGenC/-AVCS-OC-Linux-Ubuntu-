#!/usr/bin/env python

from threading import Thread
from Interface import *
from SpeechConversion import *
from TextProcessing import *
from KeyButtonHandler import *
from ConnectingModule import *
from CommandExecution import *

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    resultOutput = ResultOutput(window)
    tp = TextProcessing()
    kbh = KeyButtonHandler()
    itm = InternalModuleList(window.openWindow, window.closeWindow, tp.changeListeningMode)
    sc = SpeechConversion(tp.getRecognizedText)
    tp.connecting(runCommand, resultOutput, itm, window)
    window.connecting(tp, sc, kbh)
    window.openWindow()
    kbh.connecting(tp)
    sys.exit(app.exec_())
