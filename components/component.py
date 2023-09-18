from PySide6.QtWidgets import (
    QWidget,
    QLayout,
    QSpacerItem,
)
from typing import List, Union, Optional, Callable


class Event:
    def __init__(self, component: "Component", name: str, data) -> None:
        self.component = component
        self.name = name
        self.data = data


ComponentElement = Union[QLayout, QWidget, QSpacerItem]
FTrap = Callable[[Event], Optional[Event]]

class Component:
    def __init__(
        self,
        label,
        trap: Optional[FTrap],
    ) -> None:
        self.label = label
        self._c_parent = None
        self._trap = trap
        self._dirty = set()

    def set_trap(self, trap: FTrap):
        old_trap = self._trap
        self._trap = trap
        return old_trap
    
    def set_parent(self, c_parent: "Component"):
        old_c_parent = self._c_parent
        self._c_parent = c_parent
        return old_c_parent

    def prop_event(self, event: Event):
        cur = self
        while cur is not None:
            if cur._trap:
                event = cur._trap(event)
            if not event:
                break
            cur = cur._c_parent

    def clear_dirty(self):
        self._dirty = set()

    def is_dirty(self):
        return len(self._dirty) > 0

    def clear(self):
        self.clear_dirty()

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
