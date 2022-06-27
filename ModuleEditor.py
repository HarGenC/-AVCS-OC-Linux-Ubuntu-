import imp
from PyQt5.QtWidgets import *
from PyQt5 import QtWidgets, QtCore, QtGui
from time import sleep
from threading import Thread
import sys
from ModulesAndCommandsEditor import *
from Notification import *

class ModuleEditor(QWidget):
	def __init__(self, addCommandToModuleEditor, updateModuleList, updateCommandList, notification: Notification):
		super(ModuleEditor, self).__init__()
		self.CurrentModule = ""
		self.SelectedVoiceResponse = ""
		self.CommandList = []
		self.addModuleEditor()
		self.addCommandEditor()
		self.addCommandToModuleEditor = addCommandToModuleEditor
		self.updateModuleList = updateModuleList
		self.updateCommandList = updateCommandList
		self.Notification = notification

	def addModule(self):
		if Editor.AddEmptyModule(self.ModuleName.text()) == -1:
			self.Notification.showErrorNotification("Название данного модуля уже существует")
		else:
			self.ModuleName.setText("")
			self.ModuleWindow.hide()
			self.updateModuleList()


	def addVoiceCommand(self):
		self.addCommandToModuleEditor()

	def changeButtonIconToMcirophone(self):
		self.AddVoiceCommandButton.setIconSize(QtCore.QSize(20, 20))
		self.AddVoiceCommandButton.setText("")

	def changeButtonIconToText(self):
		self.AddVoiceCommandButton.setIconSize(QtCore.QSize(0, 0))
		self.AddVoiceCommandButton.setText("Add")

	def selectModule(self, module):
		self.CurrentModule = module

	def addCommand(self):
		result = Editor.AddCommand(self.CurrentModule, self.CommandName.text(),
		self.CommandList, self.CommandPath.text())
		if result == -1:
			self.Notification.showErrorNotification("Название данной команды уже существует")
		elif result == -2:
			self.Notification.showErrorNotification("Однин из голосовых откликов уже существует")
		elif result == -3:
			self.Notification.showErrorNotification("Один из голосовых откликов пустой")
		else:
			self.CommandName.setText("")
			self.CommandList = []
			self.VoiceResponseList.clear()
			self.CommandPath.setText("")
		self.updateCommandList(self.CurrentModule)

	def voiceResponseListClicked(self):
		for item in self.VoiceResponseList.selectedItems():
			self.SelectedVoiceResponse = item.text()

	def deleteVoiceCommand(self):		
		self.CommandList.remove(self.SelectedVoiceResponse)
		self.VoiceResponseList.clear()
		self.VoiceResponseList.addItems(self.CommandList)

	def addCommandInList(self, text: str):
		self.CommandList.append(text)
		self.VoiceResponseList.addItem(text)

	def showModuleEditor(self):
		if self.CommandWindow.isEnabled == False:
			self.ModuleName.setText("")
		self.ModuleWindow.show()

	def showCommandEditor(self, module: str):
		self.CommandWindow.show()
		self.CurrentModule = module

	def addModuleEditor(self):
		self.ModuleWindow = self.addWidget(" ", 280, 110, "background-color: #3C424F")
		self.ModuleWindowText = self.addLabel(self.ModuleWindow, "Добавить модуль", "color: white;font: 16px ;text-align:center;border: none;border-radius: 8px; background: transparent;", 75, 5)
		self.ModuleName = QtWidgets.QLineEdit(self.ModuleWindow)
		self.ModuleName.setFixedSize(150, 30)
		self.ModuleName.setStyleSheet("background-color: #D2D7D9; color: black; border-radius: 8px; border: none; font: 14px;")
		self.ModuleName.move(90, 35)
		self.ModuleNameText = self.addLabel(self.ModuleWindow, "Название:", "color: white;font: 14px ;text-align:center;border: none;border-radius: 8px; background: transparent;", 10, 40)
		self.AddModuleButton = self.addButton(self.ModuleWindow, "Добавить", "color: white;font: 14px ;text-align:center;border: none;background-color: #50545D;border-radius: 8px",
			100, 30, 90, 70, self.addModule)

	def addCommandEditor(self):
		self.CommandWindow = self.addWidget(" ", 280, 380, "background-color: #3C424F")
		self.CommandWindowText = self.addLabel(self.CommandWindow, "Добавить команду", "color: white;font: 16px ;text-align:center;border: none;border-radius: 8px; background: transparent;", 75, 10)
		self.CommandName = self.addLineEdit(self.CommandWindow, 150, 30, 90, 45, "background-color: #D2D7D9; color: black; border-radius: 8px; border: none; font: 14px;")
		self.CommandNameText = self.addLabel(self.CommandWindow, "Название:", "color: white;font: 14px ;text-align:center;border: none;border-radius: 8px; background: transparent;", 10, 50)
		self.VoiceResponseText = self.addLabel(self.CommandWindow, "Голосовой отклик", "color: white;font: 16px ;text-align:center;border: none;border-radius: 8px; background: transparent;", 70, 90)
		self.VoiceCommand = self.addLabel(self.CommandWindow, "Голосовая команда", "color: white;font: 14px ;text-align:center;border: none;border-radius: 8px; background: transparent;", 20, 215)

		self.addVoiceResponseList()

		self.AddVoiceCommandButton = self.addButton(self.CommandWindow, "Add", "color: white;font: 14px ;text-align:center;border: none;background-color: #50545D;border-radius: 8px",
			50, 30, 170, 210, self.addVoiceCommand)
		self.AddVoiceCommandButton.setIcon(QtGui.QIcon("./Resources/Microphone/Microphone.png"))
		self.AddVoiceCommandButton.setIconSize(QtCore.QSize(0, 0))
		self.DeleteVoiceCommandButton = self.addButton(self.CommandWindow, "", "color: white;font: 14px ;text-align:center;border: none;background-color: #50545D;border-radius: 8px",
			30, 30, 230, 210, self.deleteVoiceCommand)
		self.DeleteVoiceCommandButton.setIcon(QtGui.QIcon("./Resources/DeleteButton/trashcan.png"))
		self.DeleteVoiceCommandButton.setIconSize(QtCore.QSize(25, 25))
		self.PathToFileText = self.addLabel(self.CommandWindow, "Путь к файлу", "color: white;font: 16px ;text-align:center;border: none;border-radius: 8px; background: transparent;", 20, 260)
		self.CommandPath = self.addLineEdit(self.CommandWindow, 240, 30, 20, 285, "background-color: #D2D7D9; color: black; border-radius: 8px; border: none; font: 14px;")
		self.AddCommandButton = self.addButton(self.CommandWindow, "Добавить", "color: white;font: 14px ;text-align:center;border: none;background-color: #50545D;border-radius: 8px",
			100, 30, 90, 330, self.addCommand)

	def addVoiceResponseList(self):
		self.VoiceResponseArea = QtWidgets.QWidget(self.CommandWindow)
		self.VoiceResponseArea.setFixedSize(260, 100)
		self.VoiceResponseArea.move(10, 110)
		self.VoiceResponse = QtWidgets.QGridLayout(self.VoiceResponseArea)
		self.VoiceResponse.setObjectName("VoiceResponse")
		self.ScrollAreaVoiceResponseList = QtWidgets.QScrollArea(self.VoiceResponseArea)
		self.ScrollAreaVoiceResponseList.setStyleSheet("border: none")
		self.ScrollAreaVoiceResponseList.setWidgetResizable(True)
		self.ScrollAreaVoiceResponseList.setObjectName("ScrollAreaVoiceResponseList")
		self.VoiceResponseList = QtWidgets.QListWidget(self.ScrollAreaVoiceResponseList)
		self.VoiceResponseList.setStyleSheet("color: white;font: 20px;border: none;background-color: #363847;border-radius: 8px")
		self.VoiceResponseList.setFixedSize(240, 80)
		self.VoiceResponseList.setObjectName("VoiceResponseList")
		self.VoiceResponseList.itemSelectionChanged.connect(self.voiceResponseListClicked)
		self.ScrollAreaCommands = QtWidgets.QWidget()
		self.ScrollAreaCommands.setGeometry(QtCore.QRect(0, 0, 98, 28))
		self.ScrollAreaCommands.setObjectName("ScrollAreaCommands")
		self.ScrollAreaVoiceResponseList.setWidget(self.ScrollAreaCommands)
		self.VoiceResponse.addWidget(self.ScrollAreaVoiceResponseList, 0, 0, 1, 1)

	def addButton(self, parent, text, style, width, height, x, y, func):
	    Button = QtWidgets.QPushButton(parent)
	    Button.setText(text)
	    Button.setStyleSheet(style)
	    Button.setFixedSize(width, height)
	    Button.move(x, y)
	    Button.clicked.connect(func)
	    return Button

	def addLabel(self, parent, text, style, x, y):
	    Label = QtWidgets.QLabel(parent)
	    Label.setText(text)
	    Label.setStyleSheet(style)
	    Label.move(x, y)
	    return Label

	def addWidget(self, windowTitle, width, height, style):
	    Widget = QtWidgets.QWidget()
	    Widget.setFixedSize(width, height)
	    Widget.setWindowTitle(windowTitle)
	    Widget.setStyleSheet(style)
	    return Widget

	def addLineEdit(self, parent, width, height, x, y, style):
		LineEdit = QtWidgets.QLineEdit(parent)
		LineEdit.setFixedSize(width, height)
		LineEdit.setStyleSheet(style)
		LineEdit.move(x, y)
		return LineEdit