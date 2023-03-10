from PyQt5.QtWidgets import QApplication, QMainWindow, QLineEdit, QLabel, QPushButton, QCheckBox, QComboBox
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from io import BytesIO
from PIL import Image

import sys
import requests


class Form(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(300, 300, 780, 800)
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
        self.image.move(20, 150)
        self.image.resize(800, 700)

        self.btn = QPushButton(self)
        self.btn.move(660, 20)
        self.btn.resize(100, 30)
        self.btn.setText('ok')
        self.btn.clicked.connect(self.get_info)

        self.lbl = QLabel(self)
        self.lbl.setText('Введите корректные данные')
        self.lbl.resize(270, 20)
        self.lbl.move(420, 120)
        self.lbl.hide()

        self.btn_reset = QPushButton(self)
        self.btn_reset.setText('X')
        self.btn_reset.resize(30, 30)
        self.btn_reset.move(410, 70)
        self.btn_reset.clicked.connect(self.reset)

        self.cbox1 = QCheckBox(self)
        self.cbox1.move(460, 70)
        self.cbox1.setChecked(False)
        self.cbox1.toggled.connect(self.check_index)

        self.lbl_index = QLabel(self)
        self.lbl_index.move(490, 70)
        self.lbl_index.setText('Индекс')

        self.lbl_layer = QLabel(self)
        self.lbl_layer.move(580, 70)
        self.lbl_layer.setText('Слой:')

        self.layer = QComboBox(self)
        self.layer.move(630, 70)
        self.layer.addItem('схема')
        self.layer.addItem('спутник')
        self.layer.addItem('гибрид')
        if self.layer.objectNameChanged:
            self.get_info()
            print(2)

    def check_index(self):
        try:
            if self.cbox1.isChecked():
                self.lbl.hide()

                try:
                    self.delta = str(float(self.mashtab.text()))
                except Exception:
                    self.delta = '0.005'

                toponym_to_find = self.address.text()
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
                self.toponym_index = toponym["metaDataProperty"]["GeocoderMetaData"]['Address']['postal_code']

                self.address.setText(self.address.text() + ', ' + self.toponym_index)

            else:
                self.address.setText(self.address.text()[:self.address.text().rfind(', ')])
        except Exception as ex:
            print(type(ex))

    def reset(self):
        self.address.setText('Введите адрес')
        self.object.setText('Введите запрос')
        self.get_info()

    def get_info(self):

        self.lbl.hide()

        self.toponym_longitude = self.coord_x.text()
        self.toponym_lattitude = self.coord_y.text()
        self.delta = self.mashtab.text()

        try:
            self.delta = str(float(self.mashtab.text()))
        except Exception:
            self.delta = '0.005'

        try:
            self.toponym_longitude = str(float(self.toponym_longitude))
            self.toponym_lattitude = str(float(self.toponym_lattitude))

        except Exception:
            self.lbl.show()
            return None

        map_layers = {
            "схема": "map",
            "спутник": "sat",
            "гибрид": "skl",
        }

        map_params = {
            "ll": ",".join([self.toponym_longitude, self.toponym_lattitude]),
            "spn": ",".join([self.delta, self.delta]),
            "l": map_layers.get(self.layer.currentText(), "map")
        }

        map_api_server = "http://static-maps.yandex.ru/1.x/"
        response = requests.get(map_api_server, params=map_params)

        im = Image.open(BytesIO(response.content))
        im.save('img.png')
        self.pixmap = QPixmap('img.png')
        self.pixmap = self.pixmap.scaled(730, 600, Qt.KeepAspectRatio)
        self.image.setPixmap(self.pixmap)

        self.cbox1.setChecked(False)

    def get_address(self):
        self.lbl.hide()

        try:
            self.delta = str(float(self.mashtab.text()))
        except Exception:
            self.delta = '0.005'

        toponym_to_find = self.address.text()
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
        self.toponym_index = toponym["metaDataProperty"]["GeocoderMetaData"]['Address']['postal_code']

        map_params = {
            "ll": ",".join([toponym_longitude, toponym_lattitude]),
            "spn": ",".join([self.delta, self.delta]),
            "l": "map"
        }

        self.coord_x.setText(toponym_longitude)
        self.coord_y.setText(toponym_lattitude)
        self.mashtab.setText(self.delta)

        map_api_server = "http://static-maps.yandex.ru/1.x/"
        response = requests.get(map_api_server, params=map_params)

        im = Image.open(BytesIO(response.content))
        im.save('img.png')
        self.pixmap = QPixmap('img.png')
        self.pixmap = self.pixmap.scaled(730, 600, Qt.KeepAspectRatio)
        self.image.setPixmap(self.pixmap)

        self.check_index()

    def get_obj(self):
        self.lbl.hide()

        self.toponym_longitude = self.coord_x.text()
        self.toponym_lattitude = self.coord_y.text()
        self.delta = self.mashtab.text()

        try:
            self.delta = str(float(self.mashtab.text()))
        except Exception:
            self.delta = '0.005'

        try:
            self.toponym_longitude = str(float(self.toponym_longitude))
            self.toponym_lattitude = str(float(self.toponym_lattitude))

            self.coord_x.setText(self.toponym_longitude)
            self.coord_y.setText(self.toponym_lattitude)
            self.mashtab.setText(self.delta)

        except Exception:
            self.lbl.show()
            return None

        search_api_server = "https://search-maps.yandex.ru/v1/"
        api_key = "dda3ddba-c9ea-4ead-9010-f43fbc15c6e3"

        address_ll = ",".join([self.toponym_longitude, self.toponym_lattitude])

        search_params = {
            "apikey": api_key,
            "text": self.object.text(),
            "lang": "ru_RU",
            "ll": address_ll,
            "type": "biz"
        }

        response = requests.get(search_api_server, params=search_params)

        if response:
            json_response = response.json()

            organization = json_response["features"][0]
            org_address = organization["properties"]["CompanyMetaData"]["address"]
            number = org_address[org_address.rfind(','):]
            point = organization["geometry"]["coordinates"]
            org_point = "{0},{1}".format(point[0], point[1])

            self.coord_x.setText(str(point[0]))
            self.coord_y.setText(str(point[1]))
            self.address.setText(org_address + number)

            map_params = {
                "ll": org_point,
                "spn": ",".join([self.delta, self.delta]),
                "l": "map",
                "pt": "{0},pm2dgl".format(org_point)
            }

            map_api_server = "http://static-maps.yandex.ru/1.x/"
            response = requests.get(map_api_server, params=map_params)

            im = Image.open(BytesIO(response.content))
            im.save('img.png')
            self.pixmap = QPixmap('img.png')
            self.pixmap = self.pixmap.scaled(730, 600, Qt.KeepAspectRatio)
            self.image.setPixmap(self.pixmap)

            self.check_index()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    form = Form()
    form.show()
    sys.exit(app.exec())
