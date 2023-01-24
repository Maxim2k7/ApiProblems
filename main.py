# -*- coding: utf-8 -*-
import os
import sys

import requests
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QLineEdit

SCREEN_SIZE = [600, 450]


class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.map_file = None
        self.initUI1()

    def getImage(self):
        x = self.x_coord.text()
        y = self.y_coord.text()
        map_request = f"http://static-maps.yandex.ru/1.x/?ll={x},{y}&spn=0.002,0.002&l=map"
        response = requests.get(map_request)

        if not response:
            print("Ошибка выполнения запроса:")
            print(map_request)
            print("Http статус:", response.status_code, "(", response.reason, ")")
            sys.exit(1)

        self.map_file = "map.png"
        with open(self.map_file, "wb") as file:
            file.write(response.content)
        self.pixmap = QPixmap(self.map_file)
        self.image.setPixmap(self.pixmap)
        self.btn.setHidden(True)
        self.x_coord.setHidden(True)
        self.x_text.setHidden(True)
        self.y_coord.setHidden(True)
        self.y_text.setHidden(True)

    def initUI1(self):
        self.setGeometry(100, 100, *SCREEN_SIZE)
        self.setWindowTitle('Отображение карты')

        self.image = QLabel(self)
        self.image.move(0, 0)
        self.image.resize(600, 450)
        self.x_text = QLabel(self)
        self.x_text.setText("Первая координата:")
        self.x_text.move(150, 150)
        self.y_text = QLabel(self)
        self.y_text.setText("Вторая координата:")
        self.y_text.move(350, 150)
        self.x_coord = QLineEdit(self)
        self.x_coord.move(150, 175)
        self.y_coord = QLineEdit(self)
        self.y_coord.move(350, 175)
        self.btn = QPushButton(self)
        self.btn.setText("Получить карту")
        self.btn.move(275, 225)
        self.btn.clicked.connect(self.getImage)


    def initUI2(self):
        self.setGeometry(100, 100, *SCREEN_SIZE)
        self.setWindowTitle('Отображение карты')

    def closeEvent(self, event):
        if self.map_file != None:
            os.remove(self.map_file)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())
