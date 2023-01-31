# -*- coding: utf-8 -*-
import os
import sys

import requests
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QLineEdit, QInputDialog

SCREEN_SIZE = [600, 450]


class Example(QMainWindow):
    def __init__(self):
        super().__init__()
        self.map_file = None
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
        self.btn.move(250, 225)
        self.btn.clicked.connect(self.getImage)
        self.maptpmenu_btn = QPushButton(self)
        self.maptpmenu_btn.setText("Выбрать слой")
        self.maptpmenu_btn.move(475, 15)
        self.maptpmenu_btn.setFocusPolicy(Qt.FocusPolicy())
        self.maptpmenu_btn.clicked.connect(self.set_map_type)

        self.x = 0
        self.y = 0
        self.x_b_lim = -180
        self.x_t_lim = 180
        self.y_b_lim = -90
        self.y_t_lim = 90
        self.s = 0.002
        self.s_t_lim = 0.064
        self.s_b_lim = 0.001
        self.map_type = "map"
        self.initcompl = False
        self.setMouseTracking(True)

    def getImage(self):
        if not self.initcompl:
            self.x = float(self.x_coord.text())
            self.y = float(self.y_coord.text())
            self.initcompl = True
        map_request = f"http://static-maps.yandex.ru/1.x/?ll={self.x},{self.y}&spn={self.s},{self.s}&l={self.map_type}"
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
        self.btn.setEnabled(False)
        self.x_coord.setEnabled(False)
        self.x_text.setEnabled(False)
        self.y_coord.setEnabled(False)
        self.y_text.setEnabled(False)
        self.btn.setHidden(True)
        self.x_coord.setHidden(True)
        self.x_text.setHidden(True)
        self.y_coord.setHidden(True)
        self.y_text.setHidden(True)

    def set_map_type(self):
        map_type, ok_pressed = QInputDialog.getItem(
            self, "Выберите тип карты", "Тип карты",
            ("Схема", "Спутник", "Гибрид"), 0, False)
        if ok_pressed:
            if map_type == "Схема":
                self.map_type = "map"
            elif map_type == "Спутник":
                self.map_type = "sat"
            else:
                self.map_type = "sat,skl"
            if self.initcompl:
                self.getImage()

    def keyPressEvent(self, event):
        if self.initcompl:
            if event.key() == Qt.Key_PageUp:
                self.s *= 2
                if self.s > self.s_t_lim:
                    self.s = self.s_t_lim
            elif event.key() == Qt.Key_PageDown:
                self.s /= 2
                if self.s < self.s_b_lim:
                    self.s = self.s_b_lim
            if event.key() == Qt.Key_Up:
                self.y += self.s
                if self.y + self.s > self.y_t_lim:
                    self.y = self.y_t_lim - self.s
            elif event.key() == Qt.Key_Down:
                self.y -= self.s
                if self.y - self.s < self.y_b_lim:
                    self.y = self.y_b_lim + self.s
            if event.key() == Qt.Key_Right:
                self.x += self.s
                if self.x + self.s > self.x_t_lim:
                    self.x = self.x_t_lim - self.s
            elif event.key() == Qt.Key_Left:
                self.x -= self.s
                if self.x - self.s < self.x_b_lim:
                    self.x = self.x_b_lim + self.s
            self.getImage()

    def closeEvent(self, event):
        if self.map_file != None:
            os.remove(self.map_file)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())