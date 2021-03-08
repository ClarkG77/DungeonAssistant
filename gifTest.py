import sys
import requests
from PyQt5.QtWidgets import QApplication, QWidget, QLabel
from PyQt5.QtGui import QImage, QPixmap


url_image = 'https://i.gifer.com/edF.gif'

app = QApplication([])

image = QImage()
image.loadFromData(requests.get(url_image).content)
image_label = QLabel()
image_label.setPixmap(QPixmap(image))
image_label.show()

app.exec_()