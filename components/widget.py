from PySide6.QtWidgets import QLabel, QWidget
from PySide6.QtGui import QImage, QPixmap
from PySide6.QtCore import Qt
from components.component import Component
from typing import Optional
import numpy as np


class WidgetComponent(Component):
    def __init__(self, label) -> None:
        super().__init__(label)

    def update(self, element, parent) -> QWidget:
        if self.is_dirty():
            new_widget = self.create(parent)
            return new_widget
        return element


class Image(WidgetComponent):
    def __init__(self, label, width=100, height=100) -> None:
        super().__init__(label)
        self.image: Optional[QImage] = None
        self.data: Optional[np.ndarray] = None
        self.data_format = "rgb"
        self.path: Optional[str] = None
        self.width = width
        self.height = height

    def _set_image(self, property):
        img = None
        if property in {"data", "data_format"}:
            if self.data_format == "rgb":
                format = QImage.Format.Format_RGB888
            img = QImage(self.data, self.data[1], self.data[0], format)
        elif property == "path":
            img2 = QImage()
            if img2.load(self.path):
                img = img2
        if img:
            self.image = img

    def set_property(self, property, value):
        super().set_property(property, value)
        self._set_image(property)

    def create(self, parent):
        label = QLabel(parent)
        label.setFixedWidth(self.width)
        label.setFixedHeight(self.height)

        img = None
        if self.image:
            img = self.image
        elif self.data:
            if self.data_format == "rgb":
                format = QImage.Format.Format_RGB888
            img = QImage(self.data, self.data[1], self.data[0], format)
        elif self.path:
            img2 = QImage()
            if img2.load(self.path):
                img = img2

        if img:
            self.image = img
            pixmap = QPixmap.fromImage(img)
            pixmap.scaled(self.width, self.height, Qt.KeepAspectRatio)
            label.setPixmap(pixmap)
        return label
