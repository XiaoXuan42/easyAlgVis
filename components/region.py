from PySide6.QtWidgets import QLayout, QBoxLayout
from typing import Dict, Optional
from components.component import Component
from components.container import VBox, ContainerComponent
import copy


class RegionComponent(VBox):
    def __init__(self, label) -> None:
        if label == "":
            raise ValueError(f"RegionComponent must have a non-empty label")

        super().__init__(label=label)
        self.label2component: Dict[str, Component] = {}

    def clear_subcomponents(self):
        super().clear_subcomponents()
        self.label2component = {}

    def is_region(self):
        return True

    def _build_refs(self):
        self.label2component = {}

        def f(c):
            if c.label in self.label2component:
                raise RuntimeError(f"Conflict label: {c.label}")
            if c.label != "":
                self.label2component[c.label] = c

        self.visit_components(self, f_pre=f, _init=True, _all=False)

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

    def copy(self, new_label):
        def f_pre(c):
            copy_c = copy.deepcopy(c)
            if isinstance(c, ContainerComponent):
                copy_c.clear_subcomponents()
            return copy_c

        def f_in(c, pre, subpre, subpost):
            pre.add_subcomponent(subpost)

        def f_post(c, pre):
            if isinstance(pre, RegionComponent):
                pre._build_refs()
            return pre

        _, c = self.visit_components(
            self, f_pre=f_pre, f_in=f_in, f_post=f_post, _init=True, _all=True
        )
        c.label = new_label
        return c

    def __call__(self, *args):
        super().__call__(*args)
        self._build_refs()
        return self
