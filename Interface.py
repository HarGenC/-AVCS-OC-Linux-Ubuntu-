#!/usr/bin/env python

from PyQt5.QtWidgets import *
from PyQt5 import QtWidgets, QtCore, QtGui
import sys, webbrowser, os, pyaudio
from HistoryDisplay import *
from Notification import *
from ModuleEditor import *
from LoadSettings import *
from KeyButtonHandler import *
from ConnectingModule import *
from SearchModulesAndCommands import *


class MainWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__()
        self.recognizeNumber = 0
        self.chronologicallyNumber = 0
        self.amountNumber = 0
        self.MicrophoneList = self.getMicrophoneList()
        self.initUI()
        self.Recognition = False

    def connecting(self, TextProcessing, SpeechConversion, kbh: KeyButtonHandler):
        self.TextProcessing = TextProcessing
        self.SpeechConversion = SpeechConversion
        self.kbh = kbh

    def deleteModule(self):
        self.CommandsList.clear()
        editor = Editor()
        editor.DeleteModule(self.SelectedModule)
        self.updateModuleList()

    def deleteCommand(self):
        editor = Editor()
        editor.DeleteCommand(self.SelectedModule, self.SelectedCommand)
        self.updateCommandList(self.SelectedModule)

    def updateModuleList(self):
        if self.SearchModule.text() != "":
            searchModule()
        else:
            self.SelectedModule = ""
            self.SelectedCommand = ""
            ml = ModuleList()
            self.ModulesList.clear()
            for item in ml.modules:
                self.ModulesList.addItem(item.name)

    def updateCommandList(self, module: str):
        if self.SearchCommandLine.text() != "":
            self.searchCommand()
        else:
            self.SelectedCommand = ""
            ml = ModuleList()
            self.CommandsList.clear()
            for item in ml.modules:
                if item.name == module:
                    for command in item.commands:
                        self.CommandsList.addItem(command.name)

    def searchCommand(self):
        self.CommandsList.clear()
        if self.SearchCommandLine.text() == "":
            self.updateCommandList(self.SelectedModule)
        else:
            self.SelectedCommand = ""
            Commands = SearchCommand(self.SearchCommandLine.text(), ModuleList(), self.SelectedModule)
            self.CommandsList.addItems(Commands)

    def searchModule(self):
        self.CommandsList.clear()
        self.ModulesList.clear()
        if self.SearchModule.text() == "":
            self.updateModuleList()
        else:
            self.SelectedModule = ""
            self.SelectedCommand = ""
            self.SearchCommandLine.setText("")
            Modules = SearchModule(self.SearchModule.text(), ModuleList())
            self.ModulesList.addItems(Modules)


    def updateCodeWord(self, text: str):
        self.Recognition = False
        self.CodeWordButton.setText("Изменить")
        self.CodeWordButton.setIconSize(QtCore.QSize(0, 0))
        word = text.split()
        self.data["CodeWord"] = word[0]
        self.CodeWord.setText(word[0])

    def addVoiceResponseToCommandEditor(self, text: str):
        self.Recognition = False
        self.ModuleEditor.changeButtonIconToText()
        self.ModuleEditor.addCommandInList(text)

    def getMicrophoneList(self):
        list = []
        p = pyaudio.PyAudio()
        info = p.get_host_api_info_by_index(0)
        numdevices = info.get('deviceCount')
        for i in range(0, numdevices):
            if (p.get_device_info_by_host_api_device_index(0, i).get('maxInputChannels')) > 0:
                list.append([p.get_device_info_by_host_api_device_index(0, i).get('name'), i])
        return list

    def updateMicrophoneList(self):
        index = 0
        self.MicrophoneComboBox.clear()
        for item in self.MicrophoneList:
            self.MicrophoneComboBox.addItem(item[0])
            if (item[0] == self.data["MicrophoneName"]):
                index = item[1]
        self.MicrophoneComboBox.setCurrentIndex(index)

    def moduleListClicked(self):
        for item in self.ModulesList.selectedItems():
            self.ModuleEditor.selectModule(item.text())
            self.SelectedModule = item.text()
            self.updateCommandList(item.text())

    def commandListClicked(self):
        for item in self.CommandsList.selectedItems():
            self.SelectedCommand = item.text()
            

    def addModule(self):
        self.ModuleEditor.showModuleEditor()

    def addCommand(self):
        if self.SelectedModule == "":
            self.Notification.showErrorNotification("Выберите модуль")
            #self.Notification.showAcceptNotification("Команда выполнена")
        else:
            self.ModuleEditor.showCommandEditor(self.SelectedModule)

    def changeCodeWord(self):
        if (self.Recognition == False):
            self.Recognition = True
            self.CodeWordButton.setText("")
            self.CodeWordButton.setIconSize(QtCore.QSize(20, 20))
            self.TextProcessing.additionOutput(self.updateCodeWord)
        else:
            self.Notification.showErrorNotification("В данный момент идет запись голосового отклика команды")

    def addCommandToModuleEditor(self):
        if (self.Recognition == False):
            self.Recognition = True
            #self.StartRecognizeText(self.addVoiceResponseToCommandEditor)
            self.ModuleEditor.changeButtonIconToMcirophone()
            self.TextProcessing.additionOutput(self.addVoiceResponseToCommandEditor)
        else:
            self.Notification.showErrorNotification("В данный момент идет запись кодового слова")

    def changeKeyButton(self):
        self.kbh.getPressedButton(self.changeKeyButtonText)

    def changeKeyButtonText(self, text: str):
        self.KeyButton.setText(text)
        self.KeyButtonText = text

    def saveSettings(self):
        self.data["MicrophoneName"] = str(self.MicrophoneComboBox.currentText())
        self.data["KeyButton"] = self.KeyButtonText
        self.data["Notification"] = self.ShowNotifications
        self.loadSettings.SaveSettings(self.data)
        self.kbh.changeKeyButton()
        self.TextProcessing.updateCodeWord()
        self.SpeechConversion.changeMicrophone()

    def quitApp(self):
        self.closeWindow()
        self.TrayIcon.hide()
        self.SpeechConversion.stop()
        self.Notification.StopThread = True
        sys.exit()

    def managementButtonClicked(self):
        url = str(os.getcwd()) + "/Manual/Manual.html"
        webbrowser.open(url)

    def recognizedButtonClicked(self):
        self.recognizeNumber = ((self.recognizeNumber + 1)%3)
        if (self.recognizeNumber == 0):
            self.RecognizedButton.setText("Распознанные/\nНераспознанные")
        elif (self.recognizeNumber == 1):
            self.RecognizedButton.setText("Распознанные")
        elif (self.recognizeNumber == 2):
            self.RecognizedButton.setText("Нераспознанные")
        updateHistory(self)

    def chronologicallyButtonClicked(self):
        self.chronologicallyNumber = ((self.chronologicallyNumber + 1)%2)
        if (self.chronologicallyNumber == 0):
            self.СhronologicallyButton.setText("Хронологически")
        elif (self.chronologicallyNumber == 1):
            self.СhronologicallyButton.setText("Статистически")
        updateHistory(self)

    def amountButtonClicked(self):
        self.amountNumber = ((self.amountNumber + 1)%4)
        if (self.amountNumber == 0):
            self.AmountButton.setText("Количество отображаемых\nкоманд: 10")
        elif (self.amountNumber == 1):
            self.AmountButton.setText("Количество отображаемых\nкоманд: 25")
        elif (self.amountNumber == 2):
            self.AmountButton.setText("Количество отображаемых\nкоманд: 50")
        elif (self.amountNumber == 3):
            self.AmountButton.setText("Количество отображаемых\nкоманд: 100")
        updateHistory(self)

    def clearHistoryList(self):
        self.HistoryList.clear()

    def addItemsInHistoryList(self, items):
        self.HistoryList.addItems(items)

    def changeListener(self):
        self.TextProcessing.changeListeningMode()

    def openWindow(self):
        self.show()

    def closeWindow(self):
        self.hide()

    def closeEvent(self, event):
        event.ignore()
        self.closeWindow()

    def changeIcon(self, index):
        if index == 1:
            self.TrayIcon.setIcon(QtGui.QIcon("./Resources/Icons/GrayIcon.png"))
        elif index == 2:
            self.TrayIcon.setIcon(QtGui.QIcon("./Resources/Icons/GreenIcon.png"))
        elif index == 3:
            self.TrayIcon.setIcon(QtGui.QIcon("./Resources/Icons/YellowIcon.png"))
        elif index == 4:
            self.TrayIcon.setIcon(QtGui.QIcon("./Resources/Icons/RedIcon.png"))
        elif index == 5:
            self.TrayIcon.setIcon(QtGui.QIcon("./Resources/Icons/GrayIconWithX.png"))

    def addTrayIcon(self):
        self.TrayIcon = QtWidgets.QSystemTrayIcon(self)
        self.TrayIcon.setIcon(QtGui.QIcon("./Resources/Icons/GrayIcon.png"))
        
        self.TrayMenu = QtWidgets.QMenu()
        self.ShowAction = QAction("Открыть", self)
        self.QuitAction = QAction("Выход", self)
        self.onOffListener = QAction("Вкл/Выкл прослушивание", self)
        self.TrayMenu.addAction(self.ShowAction)
        self.TrayMenu.addAction(self.onOffListener)
        self.TrayMenu.addAction(self.QuitAction)
        self.TrayIcon.setContextMenu(self.TrayMenu)
        self.TrayMenu.setStyleSheet("background-color: #4F535C; color: white;")
        self.ShowAction.triggered.connect(self.openWindow)
        self.QuitAction.triggered.connect(self.quitApp)
        self.onOffListener.triggered.connect(self.changeListener)

        self.TrayIcon.show()

    def addModulePage(self):
        self.ModulePage = self.addWidget(self, "ModulePage", 580, 600, 0, 0)
        self.ModuleVL = QtWidgets.QVBoxLayout(self.ModulePage)

        self.addSearchArea()

        self.ModuleLists = self.addWidget(self, "ModuleLists", 580, 350, 0, 0)
        self.ModuleVL.addWidget(self.ModuleLists)
        self.ModuleListHL = QtWidgets.QHBoxLayout(self.ModuleLists)

        self.addModuleList()
        self.addCommandList()
        self.addButtonsModulePage()
        
        self.StackedWidget.addWidget(self.ModulePage)

    def addButtonsModulePage(self):
        self.ModuleButtonsArea = QtWidgets.QWidget()
        self.ModuleButtonsArea.setFixedSize(580, 50)
        self.ModuleVL.addWidget(self.ModuleButtonsArea)
        self.AddModuleButton = self.addButton(self.ModulePage, "Добавить модуль","color: white;font: 14px ;text-align:center;border: none;background-color: #50545D;border-radius: 8px",
            "AddModuleButton", 150, 30, 80, 410, self.addModule)
        self.AddCommandButton = self.addButton(self.ModulePage, "Добавить команду", "color: white;font: 14px ;text-align:center;border: none;background-color: #50545D;border-radius: 8px",
            "AddCommandButton", 150, 30, 365, 410, self.addCommand)
        self.DeleteModuleButton = self.addButton(self.ModulePage, "","color: white;font: 14px ;text-align:center;border: none;background-color: #50545D;border-radius: 8px",
            "AddModuleButton", 30, 30, 240, 410, self.deleteModule)
        self.DeleteCommandButton = self.addButton(self.ModulePage, "","color: white;font: 14px ;text-align:center;border: none;background-color: #50545D;border-radius: 8px",
            "AddModuleButton", 30, 30, 525, 410, self.deleteCommand)
        self.DeleteModuleButton.setIcon(QtGui.QIcon("./Resources/DeleteButton/trashcan.png"))
        self.DeleteCommandButton.setIcon(QtGui.QIcon("./Resources/DeleteButton/trashcan.png"))
        self.DeleteModuleButton.setIconSize(QtCore.QSize(25, 25))
        self.DeleteCommandButton.setIconSize(QtCore.QSize(25, 25))

    def addCommandList(self):
        self.CommandListArea = QtWidgets.QWidget()
        self.CommandListArea.setObjectName("CommandListArea")

        self.CommandListAreaLayout = QtWidgets.QGridLayout(self.CommandListArea)
        self.CommandListAreaLayout.setObjectName("CommandListAreaLayout")
        self.ScrollAreaCommandList = self.addScroll(self.CommandListArea, "ScrollAreaCommandList")
        self.CommandsList = self.addListWidget(self.ScrollAreaCommandList, "color: white;font: 20px;border: none;background-color: #363847;border-radius: 8px", 260, 300)
        self.CommandsList.itemSelectionChanged.connect(self.commandListClicked)
        self.ScrollAreaCommands = QtWidgets.QWidget()
        self.ScrollAreaCommands.setGeometry(QtCore.QRect(0, 0, 98, 28))
        self.ScrollAreaCommands.setObjectName("ScrollAreaCommands")
        self.ScrollAreaCommandList.setWidget(self.ScrollAreaCommands)
        self.CommandListAreaLayout.addWidget(self.ScrollAreaCommandList, 0, 0, 1, 1)
        self.ModuleListHL.addWidget(self.CommandListArea)

        self.CommandListText = self.addLabel(self.ModulePage, "Команда", "color: white;font: 16px ;text-align:center;border: none;border-radius: 8px; background: transparent;", 
            "CommandListText", 150, 30, 335, 60)

    def addModuleList(self):
        self.ModuleListArea = QtWidgets.QWidget()
        self.ModuleListArea.setObjectName("ModuleListArea")

        self.ModuleListAreaLayout = QtWidgets.QGridLayout(self.ModuleListArea)
        self.ModuleListAreaLayout.setObjectName("ModuleListAreaLayout")
        self.ScrollAreaModuleList = self.addScroll(self.ModuleListArea, "ScrollAreaModuleList")
        self.ModulesList = self.addListWidget(self.ScrollAreaModuleList, "color: white;font: 20px;border: none;background-color: #363847;border-radius: 8px", 260, 300)
        self.ModulesList.itemSelectionChanged.connect(self.moduleListClicked)
        self.ScrollAreaModules = QtWidgets.QWidget()
        self.ScrollAreaModules.setGeometry(QtCore.QRect(0, 0, 98, 28))
        self.ScrollAreaModules.setObjectName("ScrollAreaModules")
        self.ScrollAreaModuleList.setWidget(self.ScrollAreaModules)
        self.ModuleListAreaLayout.addWidget(self.ScrollAreaModuleList, 0, 0, 1, 1)
        self.ModuleListHL.addWidget(self.ModuleListArea)

        self.ModuleListText = self.addLabel(self.ModulePage, "Модуль", "color: white;font: 16px ;text-align:center;border: none;border-radius: 8px; background: transparent;", 
            "ModuleListText", 150, 30, 50, 60)

    def addSearchArea(self):
        self.SearchArea = self.addWidget(self.ModulePage, "SearchArea", 580, 100, 0, 0)
        self.SearchCommandLine = QtWidgets.QLineEdit(self.SearchArea)
        self.SearchCommandLine.setFixedSize(200, 30)
        self.SearchCommandLine.setStyleSheet("background-color: #D2D7D9; color: black; border-radius: 8px; border: none;font: 20px;")
        self.SearchCommandLine.move(360, 10)
        self.SearchCommandButton = self.addButton(self.SearchArea, "","color: white;font: 14px ;text-align:center;border: none;background-color: #D2D7D9;border-radius: 8px",
            "SearchCommandButton", 30, 30, 325, 10, self.searchCommand)
        self.SearchCommandButton.setIcon(QtGui.QIcon("./Resources/Search/Search.png"))
        self.SearchCommandButton.setIconSize(QtCore.QSize(25, 25))

        self.SearchModule = QtWidgets.QLineEdit(self.SearchArea)
        self.SearchModule.setFixedSize(200, 30)
        self.SearchModule.setStyleSheet("background-color: #D2D7D9; color: black; border-radius: 8px; border: none;font: 20px;")
        self.SearchModule.move(80, 10)

        self.SearchModuleButton = self.addButton(self.SearchArea, "","color: white;font: 14px ;text-align:center;border: none;background-color: #D2D7D9;border-radius: 8px",
            "SearchCommandButton", 30, 30, 40, 10, self.searchModule)
        self.SearchModuleButton.setIcon(QtGui.QIcon("./Resources/Search/Search.png"))
        self.SearchModuleButton.setIconSize(QtCore.QSize(25, 25))

    def addSettingsPage(self):
        self.SettingsPage = self.addWidget(self, "SettingsPage", 600, 600, 0, 0)
        self.SettingsVL = QtWidgets.QVBoxLayout(self.SettingsPage)

        self.addChangeKeyArea()
        self.addComboBox()
        self.addCodeWord()
        self.addCheckBox()
        self.addSaveButton()

        self.StackedWidget.addWidget(self.SettingsPage)

    def changeNotification(self):
        if (self.ShowNotifications):
            self.NotificationCheckBox.setIcon(QtGui.QIcon("./Resources/Checkbox/Var2.png"))
            self.ShowNotifications = False
        else:
            self.NotificationCheckBox.setIcon(QtGui.QIcon("./Resources/Checkbox/Var1.png"))
            self.ShowNotifications = True

    def addSaveButton(self):
        self.SaveButtonArea = self.addWidget(self, "SaveButtonArea", 550, 50, 0, 0)
        self.SaveButton = self.addButton(self.SaveButtonArea, "Сохранить", "color: white;font: 18px;text-align:center;border: none;background-color: #50545D;border-radius: 8px", 
            "SaveButton", 120, 50, 430, 0, self.saveSettings)
        self.SettingsVL.addWidget(self.SaveButtonArea)

    def addChangeKeyArea(self):
        self.ChangeKey = self.addWidget(self, "ChangeKey", 550, 100, 0, 0)
        self.TextChangeKey = self.addLabel(self.ChangeKey, "    Клавиша активации\n  голосового ассистента", "color: white;font: 14px ;text-align:center;border: none;background-color: #50545D;border-radius: 8px", 
            "TextChangeKey", 190, 50, 0, 0)
        self.KeyButton = self.addButton(self.ChangeKey, self.KeyButtonText, "color: black;font: 24px;text-align:center;border: none;background-color: #5193E2;border-radius: 8px",
            "KeyButton", 200, 50, 210, 0, self.changeKeyButton)
        self.SettingsVL.addWidget(self.ChangeKey)

    def addComboBox(self):
        self.ChangeMicrophone = self.addWidget(self, "ChangeMicrophone", 550, 100, 0, 0)
        self.MicrophoneText = self.addLabel(self.ChangeMicrophone, " Микрофон:", "color: white;font: 24px;text-align:center;border: none;background-color: #50545D;border-radius: 8px", 
            "MicrophoneText", 150, 50, 0, 0)
        self.MicrophoneComboBox = QtWidgets.QComboBox(self.ChangeMicrophone)
        self.MicrophoneComboBox.setStyleSheet("color: white;font: 24px;text-align:center;border: none;background-color: #50545D;border-radius: 8px")
        self.updateMicrophoneList()
        self.MicrophoneComboBox.setFixedSize(350, 50)
        self.MicrophoneComboBox.move(138, 0)
        self.SettingsVL.addWidget(self.ChangeMicrophone)

    def addCheckBox(self):
        self.ChangeNotification = self.addWidget(self, "ChangeNotification", 550, 100, 0, 0)
        self.NotificationText = self.addLabel(self.ChangeNotification, "               Показывать\n  всплывающие уведомления", "color: white;font: 14px; text-align: center;border: none;background-color: #50545D;border-radius: 8px", 
            "NotificationText", 225, 50, 0, 0)
        self.NotificationCheckBox = QtWidgets.QPushButton(self.ChangeNotification)
        self.NotificationCheckBox.setFixedSize(50, 50)
        self.NotificationCheckBox.move(230, 0)
        if (self.ShowNotifications):
            self.NotificationCheckBox.setIcon(QtGui.QIcon("./Resources/Checkbox/Var1.png"))
        else:
            self.NotificationCheckBox.setIcon(QtGui.QIcon("./Resources/Checkbox/Var2.png"))
        self.NotificationCheckBox.setStyleSheet("border:none")
        self.NotificationCheckBox.clicked.connect(self.changeNotification)
        self.NotificationCheckBox.setIconSize(QtCore.QSize(100, 100))
        self.SettingsVL.addWidget(self.ChangeNotification)

    def addCodeWord(self):
        self.ChangeCodeWord = self.addWidget(self, "ChangeCodeWord", 550, 100, 0, 0)
        self.CodeWordText = self.addLabel(self.ChangeCodeWord, "       Кодовое слово\n активации ассистента", "color: white;font: 16px; text-align: center;border: none;background-color: #50545D;border-radius: 8px", 
            "CodeWordText", 200, 50, 0, 0)
        self.CodeWordButton = self.addButton(self.ChangeCodeWord, "Изменить", "color: black;font: 16px;text-align:center;border: none;background-color: #5193E2;border-radius: 8px",
            "CodeWordButton", 100, 30, 220, 10, self.changeCodeWord)
        self.CodeWordButton.setIcon(QtGui.QIcon("./Resources/Microphone/Microphone.png"))
        self.CodeWordButton.setIconSize(QtCore.QSize(0, 0))
        self.CodeWord = self.addLabel(self.ChangeCodeWord, self.data["CodeWord"], "color: black;font: 16px;text-align:center;background-color: #D2D7D9;border-radius: 8px", 
            "CodeWord", 100, 30, 50, 60)
        self.SettingsVL.addWidget(self.ChangeCodeWord)

    def addHistoryPage(self):
        self.HistoryPage = self.addWidget(self, "HistoryPage", 600, 600, 0, 0)
        self.HistoryVL = QtWidgets.QVBoxLayout(self.HistoryPage)

        self.addHistoryMenuButtons()
        self.HistoryVL.addWidget(self.HistoryMenuButtons)

        self.addHistoryList()
        self.HistoryVL.addWidget(self.HistoryListArea)
        self.StackedWidget.addWidget(self.HistoryPage)

    def addHistoryList(self):
        self.HistoryListArea = QtWidgets.QWidget()
        self.HistoryListArea.setObjectName("HistoryListArea")
        self.GridLayout = QtWidgets.QGridLayout(self.HistoryListArea)
        self.GridLayout.setObjectName("gridLayout_4")
        self.ScrollHistory = self.addScroll(self.HistoryListArea, "ScrollHistory")
        self.HistoryList = self.addListWidget(self.ScrollHistory, "color: white;font: 20px;border: none;background-color: #363847;border-radius: 8px", 560, 490)
        updateHistory(self)
        self.ScrollAreaHistory = QtWidgets.QWidget()
        self.ScrollAreaHistory.setGeometry(QtCore.QRect(0, 0, 98, 28))
        self.ScrollAreaHistory.setObjectName("ScrollAreaHistory")
        self.ScrollHistory.setWidget(self.ScrollAreaHistory)
        self.GridLayout.addWidget(self.ScrollHistory, 0, 0, 1, 1)

    def addInformationPage(self):
        self.InformationPage = self.addWidget(self, "InformationPage", 600, 600, 0, 0)

        self.InformationText = QtWidgets.QLabel(self.InformationPage)
        self.InformationText.setStyleSheet("color: white; font: 16px; border: none; background-color: #363847; border-radius: 8px;")
        self.InformationText.setAlignment(QtCore.Qt.AlignCenter)
        self.InformationText.setFixedSize(550, 520)
        self.InformationText.move(25, 35)
        self.InformationText.setWordWrap(True)
        self.InformationText.setText("Информация о приложении")

        self.StackedWidget.addWidget(self.InformationPage)

    def addHistoryMenuButtons(self):
        self.HistoryMenuButtons = QtWidgets.QWidget()
        self.HistoryMenuButtonsHL = QtWidgets.QHBoxLayout(self.HistoryMenuButtons)
        self.HistoryMenuButtonsHL.setSpacing(5)

        self.RecognizedButton = self.addButton(self, "Распознанные/\nНераспознанные", "color: white;font: 14px ;text-align:center;border: none;background-color: #50545D;border-radius: 8px", 
            "RecognizedButton", 185, 50, 0, 0, self.recognizedButtonClicked)
        self.HistoryMenuButtonsHL.addWidget(self.RecognizedButton)

        self.СhronologicallyButton = self.addButton(self, "Хронологически", "color: white;font: 14px ;text-align:center;border: none;background-color: #50545D;border-radius: 8px", 
            "ChronologicallyButton", 185, 50, 0, 0, self.chronologicallyButtonClicked)
        self.HistoryMenuButtonsHL.addWidget(self.СhronologicallyButton)

        self.AmountButton = self.addButton(self, "Количество отображаемых\nкоманд: 10", "color: white;font: 12px ;text-align:center;border: none;background-color: #50545D;border-radius: 8px", 
            "AmountButton", 185, 50, 0, 0, self.amountButtonClicked)
        self.HistoryMenuButtonsHL.addWidget(self.AmountButton)


    def addMenu(self):
        self.MenuButtons = self.addWidget(self, "MenuButtons", 200, 600, 0, 0)
        self.MenuButtons2 = self.addWidget(self.MenuButtons, "MenuButtons2", 200, 250, 0, 0)
        self.MenuVL = QtWidgets.QVBoxLayout(self.MenuButtons2)

        self.ButtonHistory = self.addButton(self, "  История", "color: white;font: 24px ;text-align:left;border: none",
            "ButtonModules", 180, 40, 0, 0, self.historyButtonClicked)
        self.MenuVL.addWidget(self.ButtonHistory)

        self.ButtonSettings = self.addButton(self, "  Настройки", "color: white;font: 24px ;text-align:left;border: none",
            "ButtonModules", 180, 40, 0, 0, self.settingsButtonClicked)
        self.MenuVL.addWidget(self.ButtonSettings)

        self.ButtonModules = self.addButton(self, "  Модули", "color: white;font: 24px ;text-align:left;border: none",
            "ButtonModules", 180, 40, 0, 0, self.moduleButtonClicked)
        self.MenuVL.addWidget(self.ButtonModules)

        self.ButtonManagement = self.addButton(self, "  Руководство", "color: white;font: 24px ;text-align:left;border: none",
            "ButtonManagement", 180, 40, 0, 0, self.managementButtonClicked)
        self.MenuVL.setContentsMargins(0, 50, 0, 0)
        self.MenuVL.addWidget(self.ButtonManagement)

        self.ButtonInformation = self.addButton(self, "  О приложении", "color: white;font: 22px ;text-align:left;border: none",
            "ButtonModules", 180, 40, 0, 0, self.informationButtonClicked)
        self.MenuVL.addWidget(self.ButtonInformation)

        self.HorizontalLayout.addWidget(self.MenuButtons)

    def historyButtonClicked(self):
        self.switchPage(0)

    def settingsButtonClicked(self):
        self.switchPage(1)

    def moduleButtonClicked(self):
        self.switchPage(2)

    def informationButtonClicked(self):
        self.switchPage(3)

    def switchPage(self, page):
        self.ButtonHistory.setStyleSheet("color: white;font: 24px ;text-align:left;border: none;background-color: #3C424F")
        self.ButtonSettings.setStyleSheet("color: white;font: 24px ;text-align:left;border: none;background-color: #3C424F")
        self.ButtonModules.setStyleSheet("color: white;font: 24px ;text-align:left;border: none;background-color: #3C424F")
        self.ButtonInformation.setStyleSheet("color: white;font: 24px ;text-align:left;border: none;background-color: #3C424F")
        if (page == 0):
            self.ButtonHistory.setStyleSheet("color: white;font: 24px ;text-align:left;border: none;background-color: #5194E4")
            self.StackedWidget.setCurrentIndex(0)
        elif (page == 1):
            self.ButtonSettings.setStyleSheet("color: white;font: 24px ;text-align:left;border: none;background-color: #5194E4")
            self.StackedWidget.setCurrentIndex(1)
            self.MicrophoneList = self.getMicrophoneList()
            self.updateMicrophoneList()
            self.KeyButton.setText(self.data["KeyButton"])
            self.KeyButtonText = self.data["KeyButton"]
            self.CodeWord.setText(self.data["CodeWord"])
            if (self.ShowNotifications != self.data["Notification"]):
                self.changeNotification()
        elif (page == 2):
            self.ButtonModules.setStyleSheet("color: white;font: 24px ;text-align:left;border: none;background-color: #5194E4")
            self.StackedWidget.setCurrentIndex(2)
            self.SearchCommandLine.setText("")
            self.SearchModule.setText("")
            self.updateModuleList()
            self.CommandsList.clear()
        elif (page == 3):
            self.ButtonInformation.setStyleSheet("color: white;font: 24px ;text-align:left;border: none;background-color: #5194E4")
            self.StackedWidget.setCurrentIndex(3)

    def addButton(self, parent, text, style, objectName, width, height, x, y, func):
        Button = QtWidgets.QPushButton(parent)
        Button.setText(text)
        Button.setStyleSheet(style)
        Button.setObjectName(objectName)
        Button.setFixedSize(width, height)
        Button.move(x, y)
        Button.clicked.connect(func)
        return Button

    def addLabel(self, parent, text, style, objectName, width, height, x, y):
        Label = QtWidgets.QLabel(parent)
        Label.setText(text)
        Label.setStyleSheet(style)
        Label.setFixedSize(width, height)
        Label.move(x, y)
        return Label

    def addWidget(self, parent, objectName, width, height, x, y):
        Widget = QtWidgets.QWidget(parent)
        Widget.setFixedSize(width, height)
        Widget.move(x, y)
        Widget.setObjectName(objectName)
        return Widget

    def addScroll(self, parent, objectName):
        Scroll = QtWidgets.QScrollArea(parent)
        Scroll.setStyleSheet("border: none")
        Scroll.setWidgetResizable(True)
        Scroll.setObjectName(objectName)
        return Scroll

    def addListWidget(self, parent, style, width, height):
        List = QtWidgets.QListWidget(parent)
        List.setStyleSheet(style)
        List.setFixedSize(560, 490)
        return List

    def initUI(self):
        self.setStyleSheet("background-color: #3C424F")
        self.setGeometry(100, 100, 800, 600)
        self.setFixedSize(800, 600)
        self.CentralWidget = QtWidgets.QWidget(self)
        self.CentralWidget.setObjectName("CentralWidget")
        self.HorizontalLayout = QtWidgets.QHBoxLayout(self.CentralWidget)
        self.HorizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.HorizontalLayout.setObjectName("HorizontalLayout")
        self.StackedWidget = QtWidgets.QStackedWidget()
        self.addMenu()
        self.HorizontalLayout.addWidget(self.StackedWidget)
        self.loadSettings = LoadSettings()
        self.data = self.loadSettings.LoadSettings()
        self.KeyButtonText = self.data["KeyButton"]
        self.ShowNotifications = self.data["Notification"]
        self.addHistoryPage()
        self.addSettingsPage()
        self.addModulePage()
        self.addInformationPage()
        self.addTrayIcon()
        self.SelectedModule = ""
        self.SelectedCommand = ""
        self.switchPage(0)
        self.Notification = Notification()
        self.ModuleEditor = ModuleEditor(self.addCommandToModuleEditor, self.updateModuleList, self.updateCommandList, self.Notification)
        

if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = MainWindow()
    w.openWindow()
    sys.exit(app.exec_())
