from PyQt5.QtWidgets import *
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtGui import QPixmap
import time
from threading import Thread
import sys

class Notification(QWidget):
	def __init__(self):
		super(Notification, self).__init__()
		q = QDesktopWidget().availableGeometry()
		self.width = q.width()
		self.height = q.height()
		self.NotificationList = []
		self.StopThread = False
		self.th = Thread(target = self.closeNotification)
		self.th.start()

	def showAcceptNotification(self, text):
		if len(self.NotificationList) <= 20:
			notification = self.notification(text, False)
			notification.show()
			self.NotificationList.append([notification, time.time()])

	def showErrorNotification(self, text):
		if len(self.NotificationList) <= 20:
			notification = self.notification(text, True)
			notification.show()
			self.NotificationList.append([notification, time.time()])

	def closeNotification(self):
		while True:
			time.sleep(0.5)
			if self.StopThread == True:
				break
			if (len(self.NotificationList) > 0):
				index1 = 0
				index2 = 0
				for item in self.NotificationList:
					index1 += 1
					if (time.time() - item[1] > 3.0):
						item[0].hide()
						index2 += 1
				if (index1 == index2):
					self.NotificationList = []

	def notification(self, text, error):
		Notification = QtWidgets.QWidget()
		Notification.setWindowTitle(' ')
		Notification.setFixedSize(380, 150)
		Notification.move(self.width - 380, self.height - 182)
		Notification.setStyleSheet("background-color: #3C424F")
		NotificationText = QtWidgets.QLabel(Notification)
		NotificationText.setStyleSheet("color: white;font: 16px ;text-align:center;border: none;border-radius: 8px; background: transparent;")
		NotificationText.move(180, 5)
		NotificationImage = QtWidgets.QLabel(Notification)
		if (error == True):
			Pixmap = QPixmap("./Resources/Notification/krestik.png")
			NotificationText.setText("Ошибка")
		else:
			Pixmap = QPixmap("./Resources/Notification/galochka.png")
			NotificationText.setText("Команда принята")
		NotificationImage.setPixmap(Pixmap)
		NotificationImage.move(0, 10)
		AcceptText = QtWidgets.QLabel(Notification)
		AcceptText.setStyleSheet("color: white; font: 16px; border: none; background-color: #363847; border-radius: 8px;")
		AcceptText.setAlignment(QtCore.Qt.AlignCenter)
		AcceptText.setFixedSize(220, 110)
		AcceptText.move(155, 35)
		AcceptText.setWordWrap(True)
		AcceptText.setText(text)
		return Notification

if __name__ == "__main__":
	app = QApplication(sys.argv)
	notific = Notification()
	notific.showAcceptNotification("Хаха")
	time.sleep(5)
	notific.StopThread = True
	sys.exit(app.exec_())