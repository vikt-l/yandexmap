from PyQt5.QtWidgets import QApplication, QMainWindow, QLineEdit, QLabel, QPushButton
from PyQt5.QtGui import QPixmap
from PyQt5 import QtCore
from io import BytesIO, StringIO
from PIL import Image

import sys
import requests


class Form(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(300, 300, 780, 670)
        self.setWindowTitle('Maps API')

        self.coord_x = QLineEdit(self)
        self.coord_y = QLineEdit(self)
        self.mashtab = QLineEdit(self)

        self.coord_x.setText('Введите широту')
        self.coord_y.setText('Введите долготу')
        self.mashtab.setText('Введите масштаб')

        self.coord_x.move(10, 20)
        self.coord_y.move(220, 20)
        self.mashtab.move(430, 20)

        self.coord_x.resize(200, 30)
        self.coord_y.resize(200, 30)
        self.mashtab.resize(200, 30)

        self.image = QLabel(self)
        self.image.move(20, 25)
        self.image.resize(800, 700)

        self.btn = QPushButton(self)
        self.btn.move(660, 20)
        self.btn.resize(100, 30)
        self.btn.setText('ok')
        self.btn.clicked.connect(self.get_info)

    def get_info(self):
        self.toponym_longitude = self.coord_x.text()
        self.toponym_lattitude = self.coord_y.text()
        self.delta = self.mashtab.text()

        map_params = {
            "ll": ",".join([self.toponym_longitude, self.toponym_lattitude]),
            "spn": ",".join([self.delta, self.delta]),
            "l": "map"
        }

        map_api_server = "http://static-maps.yandex.ru/1.x/"
        response = requests.get(map_api_server, params=map_params)

        im = Image.open(BytesIO(response.content))
        im.save('img.png')
        self.pixmap = QPixmap('img.png')
        self.pixmap = self.pixmap.scaled(730, 600, QtCore.Qt.KeepAspectRatio)
        self.image.setPixmap(self.pixmap)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    form = Form()
    form.show()
    sys.exit(app.exec())
