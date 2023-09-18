from PySide6.QtWidgets import (
    QWidget,
    QLayout,
    QSpacerItem,
)
from typing import List, Union


ComponentElement = Union[QLayout, QWidget, QSpacerItem]


class Component:
    def __init__(self, label) -> None:
        self.label = label
        self._dirty = set()

    def clear_dirty(self):
        self._dirty = set()

    def is_dirty(self):
        return len(self._dirty) > 0

    def set_property(self, property, value):
        if not hasattr(self, property):
            raise ValueError(f"{self} don't have property {property}")
        if value != self.get_property(property):
            setattr(self, property, value)
            self._dirty.add(property)

    def get_property(self, property):
        return getattr(self, property)

    def create(self, parent) -> ComponentElement:
        raise RuntimeError()

    def update(self, element, parent) -> ComponentElement:
        raise RuntimeError()
