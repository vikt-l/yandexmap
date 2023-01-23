from PyQt5.QtWidgets import QApplication, QMainWindow, QLineEdit, QLabel, QPushButton
from PyQt5.QtGui import QPixmap
from PyQt5 import QtCore
from io import BytesIO
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

        self.object = QLineEdit(self)
        self.object.setText('Введите запрос')
        self.object.move(10, 70)
        self.object.resize(300, 30)

        self.btn_obj = QPushButton(self)
        self.btn_obj.setText('Искать')
        self.btn_obj.move(320, 70)
        self.btn_obj.resize(70, 30)
        self.btn_obj.clicked.connect(self.get_obj)

        self.address = QLineEdit(self)
        self.address.setText('Введите адрес')
        self.address.move(10, 120)
        self.address.resize(300, 30)

        self.btn_address = QPushButton(self)
        self.btn_address.setText('Искать')
        self.btn_address.move(320, 120)
        self.btn_address.resize(70, 30)
        self.btn_address.clicked.connect(self.get_address)

        self.image = QLabel(self)
        self.image.move(20, 80)
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

    def get_address(self):
        toponym_to_find = self.object.text()

        geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"

        geocoder_params = {
            "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
            "geocode": toponym_to_find,
            "format": "json"}

        response = requests.get(geocoder_api_server, params=geocoder_params)

        if not response:
            pass

        json_response = response.json()
        toponym = json_response["response"]["GeoObjectCollection"][
            "featureMember"][0]["GeoObject"]
        toponym_coodrinates = toponym["Point"]["pos"]
        toponym_longitude, toponym_lattitude = toponym_coodrinates.split(" ")

        delta = "0.005"
        map_params = {
            "ll": ",".join([toponym_longitude, toponym_lattitude]),
            "spn": ",".join([delta, delta]),
            "l": "map"
        }

        map_api_server = "http://static-maps.yandex.ru/1.x/"
        response = requests.get(map_api_server, params=map_params)

        im = Image.open(BytesIO(response.content))
        im.save('img.png')
        self.pixmap = QPixmap('img.png')
        self.pixmap = self.pixmap.scaled(730, 600, QtCore.Qt.KeepAspectRatio)
        self.image.setPixmap(self.pixmap)


    def get_obj(self):
        pass


if __name__ == "__main__":
    app = QApplication(sys.argv)
    form = Form()
    form.show()
    sys.exit(app.exec())
