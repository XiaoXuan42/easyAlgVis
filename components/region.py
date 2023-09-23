from PySide6.QtWidgets import QLayout, QBoxLayout
from typing import Dict, Optional
from components.component import Component
from components.container import VBox, ContainerComponent


class RegionComponent(VBox):
    def __init__(self, label) -> None:
        if label == "":
            raise ValueError(f"RegionComponent must have a non-empty label")

        super().__init__(label=label)
        self.label2component: Dict[str, Component] = {}

    def is_region(self):
        return True

    def _build_refs(self):
        self.label2component = {}

        def f(c):
            if c.label in self.label2component:
                raise RuntimeError(f"Conflict label: {c.label}")
            if c.label != "":
                self.label2component[c.label] = c

        self.visit_components(self, f_pre=f, _init=True)

    def create(self, parent) -> QLayout:
        layout = super().create(parent)
        self._build_refs()
        return layout

    def update(self, layout: QBoxLayout, parent) -> QLayout:
        layout = super().update(layout, parent)
        self._build_refs()
        return layout

    def get_component(self, label) -> Optional[Component]:
        sub_labels = label.split("::")
        c = self
        for l in sub_labels:
            if isinstance(c, ContainerComponent):
                if l in c.label2component:
                    c = c.label2component[l]
                else:
                    return None
            else:
                return None
        return c

    def __call__(self, *args):
        super().__call__(*args)
        self._build_refs()
        return self
