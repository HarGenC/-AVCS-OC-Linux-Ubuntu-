from LoadSettings import *
from ConnectingModule import *

class TextProcessing():
    def __init__(self, parent=None):
    	#self.func = func
        self.TextIsEntered = False
        self.Message = ""
        self.Listening = True
        self.AssistantIsActive = False
        self.ls = LoadSettings()
        self.CodeWord = self.ls.LoadSettings()["CodeWord"]

    def getRecognizedText(self, text: str):
        if self.Listening:
            if text != "":
                self.TextIsEntered = True
                self.Message = text
                msg = self.Message.split()
                if len(msg) > 0 and msg[0] == self.CodeWord:
                    self.AssistantIsActive = True
                    self.ResultOutput.changeIconToYellow()
            elif self.TextIsEntered:
                if self.CurrentOutput != self.MainOutput:
                    self.CurrentOutput(self.Message)
                    self.CurrentOutput = self.MainOutput
                else:
                    if self.AssistantIsActive:
                        self.ResultOutput.changeIconToGray()
                        if self.Message[:len(self.CodeWord)] == self.CodeWord:
                            self.Message = self.Message[len(self.CodeWord) + 1:]
                        self.CurrentOutput(self.Message, self.Itm, self.ResultOutput, self.mainWindow)
                        self.AssistantIsActive = False
                self.TextIsEntered = False

    def connecting(self, func, resultOutput, itm, mainWindow):
        self.MainOutput = func
        self.CurrentOutput = func
        self.ResultOutput = resultOutput
        self.Itm = itm
        self.mainWindow = mainWindow

    def additionOutput(self, func):
        self.CurrentOutput = func

    def changeListeningMode(self):
        self.Listening = not self.Listening
        if self.Listening:
            self.ResultOutput.changeIconToGray()
        else:
            self.ResultOutput.changeIconToGrayWithX()

    def activatedAssistant(self):
        self.AssistantIsActive = True
        self.ResultOutput.changeIconToYellow()

    def updateCodeWord(self):
        self.CodeWord = self.ls.LoadSettings()["CodeWord"]
