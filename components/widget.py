from PySide6.QtWidgets import QLabel, QWidget
from PySide6.QtGui import QImage, QPixmap
from PySide6.QtCore import Qt
from components.component import Component
from typing import Optional


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
        self.data: Optional[QImage] = None
        self.width = width
        self.height = height

    def create(self, parent):
        label = QLabel(parent)
        label.setFixedWidth(self.width)
        label.setFixedHeight(self.height)
        if self.data:
            pixmap = QPixmap.fromImage(self.data)
            pixmap.scaled(self.width, self.height, Qt.KeepAspectRatio)
            label.setPixmap(pixmap)
        return label
