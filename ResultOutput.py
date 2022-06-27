import time
from threading import Thread

class ResultOutput():
    def __init__(self, window):
        self.window = window

    def changeIconToGray(self):
        self.window.changeIcon(1)

    def changeIconToGreen(self):
        self.window.changeIcon(2)

    def changeIconToYellow(self):
        self.window.changeIcon(3)

    def changeIconToRed(self):
        self.window.changeIcon(4)
        th = Thread(target = self.th)
        th.start()

    def changeIconToGrayWithX(self):
        self.window.changeIcon(5)

    def showAcceptMsg(self, text):
        pass

    def showErrorMsg(self, text):
        pass

    def th(self):
        time.sleep(1)
        self.changeIconToGray()