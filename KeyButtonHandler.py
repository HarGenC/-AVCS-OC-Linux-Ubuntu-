from pynput import keyboard
from pynput.keyboard import Key
import time
from threading import Thread
from LoadSettings import *
from TextProcessing import *

class KeyButtonHandler():
	def __init__(self):
		self.ChangingTheButton = False
		self.HotKeyIsPressed = False
		self.LongPress = False
		self.ls = LoadSettings()
		self.CurrentButton = self.ls.LoadSettings()["KeyButton"]
		self.pressedButtons = []
		self.NewHotKeys = []
		self.th = Thread(target=self.startKeyButtonListener)
		self.th.start()
		self.time = time.time()

	def on_key_press(self, key):
		if not key in self.pressedButtons:
			self.pressedButtons.append(key)
			if self.convertKeysToString(self.pressedButtons) == self.CurrentButton and not self.ChangingTheButton:
				#print("Equal")
				self.HotKeyIsPressed = True
				self.time = time.time()
				if time.time() > self.time + 1.0 and not self.LongPress:
					#print("Long press")
					self.LongPress = True
					self.TextProcessing.changeListeningMode()
			elif self.ChangingTheButton:
				self.NewHotKeys.append(key)
		else:
			if time.time() > self.time + 1.0 and not self.LongPress and self.convertKeysToString(self.pressedButtons) == self.CurrentButton:
				#print("Long press")
				self.LongPress = True
				self.TextProcessing.changeListeningMode()

	def on_key_release(self, key):
		#print(self.pressedButtons)
		if key in self.pressedButtons:
			self.pressedButtons.remove(key)
		if self.ChangingTheButton:
			self.ChangingTheButton = False
			str = self.convertKeysToString(self.NewHotKeys)
			self.Func(str)
			self.NewHotKeys = []
		if self.HotKeyIsPressed:
			self.HotKeyIsPressed = False
			if not self.LongPress:
				self.TextProcessing.activatedAssistant()
		if self.LongPress:
			self.LongPress = False

	def startKeyButtonListener(self):
		self.keyboard_listener = keyboard.Listener(on_press=self.on_key_press, on_release=self.on_key_release)
		self.keyboard_listener.start()

	def connecting(self, TextProcessing: TextProcessing):
		self.TextProcessing = TextProcessing

	def changeKeyButton(self):
		self.CurrentButton = self.ls.LoadSettings()["KeyButton"]

	def getPressedButton(self, func):
		self.ChangingTheButton = True
		self.Func = func

	def convertKeysToString(self, keys):
		str = ""
		ctrlIsEntered = False
		for item in keys:
			if isinstance(item, Key):
				key = item.name
				str = str + key + "+"
				if key == "ctrl_l" or key == "ctrl_r":
					ctrlIsEntered = True
			else:
				if not ctrlIsEntered:
					str = str + item.char + "+"
				else:
					num = ord(item.char)
					str = str + chr(num + 96) + "+"
		return str[:-1]

class KeyButtonHandler2():
	def __init__(self):
		self.ChangingTheButton = False
		self.HotKeyIsPressed = False
		self.LongPress = False
		self.ls = LoadSettings()
		self.CurrentButton = self.ls.LoadSettings()["KeyButton"]
		keyboard.add_hotkey(self.CurrentButton, self.pressButton)
		keyboard.on_release(self.releaseButton, suppress=False)

	def connecting(self, TextProcessing: TextProcessing):
		self.TextProcessing = TextProcessing

	def pressButton(self):
		if not self.ChangingTheButton:
			if not self.HotKeyIsPressed:
				self.HotKeyIsPressed = True
				self.Time = time.time()
			elif not self.LongPress and time.time() - 1.0 > self.Time:
				self.TextProcessing.changeListeningMode()
				self.LongPress = True

	def releaseButton(self, button):
		if self.HotKeyIsPressed and not self.ChangingTheButton:
			if not self.LongPress:
				self.TextProcessing.activatedAssistant()
			self.LongPress = False
			self.HotKeyIsPressed = False

	def changeKeyButton(self):
		self.CurrentButton = self.ls.LoadSettings()["KeyButton"]
		keyboard.unhook_all()
		keyboard.add_hotkey(self.CurrentButton, self.pressButton)
		keyboard.on_release(self.releaseButton, suppress=False)

	def getPressedButton(self, func):
		self.ChangingTheButton = True
		Thread(target=self.readHotKey, args=(func,)).start()

	def readHotKey(self, func):
		str = keyboard.read_hotkey(suppress=False)
		time.sleep(0.3)
		func(str)
		self.ChangingTheButton = False

