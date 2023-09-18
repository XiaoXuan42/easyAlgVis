from PySide6.QtWidgets import QLayout, QBoxLayout
from typing import Dict, Optional
from components.component import Component
from components.container import VBox


class RootComponent(VBox):
    def __init__(self) -> None:
        super().__init__("")
        self.label2component: Dict[str, Component] = {}

    def _build_refs(self):
        self.label2component = {}

        def f(c):
            if c.label in self.label2component:
                raise RuntimeError(f"Conflict label: {c.label}")
            if c.label != "":
                self.label2component[c.label] = c

        self.visit_components(self, f_pre=f)

    def create(self, parent) -> QLayout:
        layout = super().create(parent)
        self._build_refs()
        return layout

    def update(self, layout: QBoxLayout, parent) -> QLayout:
        layout = super().update(layout, parent)
        self._build_refs()
        return layout

    def get_component(self, label) -> Optional[Component]:
        if label in self.label2component:
            return self.label2component[label]
        return None

    def __call__(self, *args):
        super().__call__(*args)
        self._build_refs()
        return self
