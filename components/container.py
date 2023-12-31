from PySide6.QtWidgets import (
    QWidget,
    QLayout,
    QSpacerItem,
    QBoxLayout,
    QVBoxLayout,
    QHBoxLayout,
)
from typing import List
from components.component import Component, ComponentElement


class ContainerComponent(Component):
    def __init__(self, label, trap):
        super().__init__(label, trap=trap)
        self.subcomponents: List[Component] = []

    def is_region(self):
        return False

    def visit_components(
        self, component, f_pre=None, f_in=None, f_post=None, _init=False, _all=False
    ):
        """
        Args:
            _init: initial call to visit_components or not
            _all: visit all subnodes in the tree or not
        """
        pre, post = None, None
        if f_pre:
            pre = f_pre(component)

        if isinstance(component, ContainerComponent) and (
            _init or (not component.is_region()) or _all
        ):
            for c in component.subcomponents:
                subpre, subpost = self.visit_components(
                    c, f_pre, f_in, f_post, _init=False, _all=_all
                )
                if f_in:
                    f_in(component, pre, subpre, subpost)
        if f_post:
            post = f_post(component, pre)
        return pre, post

    def clear_subcomponents(self):
        self.subcomponents = []
    
    def add_subcomponent(self, c):
        self.subcomponents.append(c)
        c.set_parent(self)

    def clear_all_dirty(self):
        f_pre = lambda c: c.clear_dirty()
        self.visit_components(self, f_pre)

    def clear_all(self):
        f_pre = lambda c: c.clear()
        self.visit_components(self, f_pre)

    def create(self, parent) -> QLayout:
        element = self.create_layout(parent)
        subelements = []
        for c in self.subcomponents:
            subelements.append(c.create(parent))
        self.post_create(element, subelements)
        return element

    def create_layout(self, parent) -> QLayout:
        raise RuntimeError()

    def post_create(self, element, subelements: List[ComponentElement]) -> None:
        pass

    def __call__(self, *args):
        self.clear_subcomponents()
        for c in list(args):
            self.add_subcomponent(c)
        return self


class BoxContainer(ContainerComponent):
    def __init__(self, label, trap):
        super().__init__(label, trap=trap)

    def update(self, layout: QBoxLayout, parent) -> QLayout:
        subitems: List[ComponentElement] = []
        for i, c in enumerate(self.subcomponents):
            item = layout.itemAt(i)
            if item.widget():
                w = item.widget()
                subitems.append(c.update(w, parent))
            else:
                subitems.append(c.update(item, parent))
        self.post_update(layout, subitems)
        return layout

    def post_create(
        self, layout: QBoxLayout, subelements: List[ComponentElement]
    ) -> None:
        for ele in subelements:
            if isinstance(ele, QWidget):
                layout.addWidget(ele)
            elif isinstance(ele, QLayout):
                layout.addLayout(ele)
            elif isinstance(ele, QSpacerItem):
                layout.addSpacerItem(ele)
            else:
                raise TypeError(ele)

    def post_update(self, layout: QBoxLayout, subitems: List[ComponentElement]):
        for i, item in enumerate(subitems):
            old_item = layout.itemAt(i)
            if isinstance(item, QWidget):
                old_widget = old_item.widget()
                if not (old_widget is item):
                    layout.removeWidget(old_widget)
                    old_widget.deleteLater()
                    layout.insertWidget(i, item)
            elif isinstance(item, QLayout):
                old_layout = old_item.layout()
                if not (old_layout is item):
                    layout.removeItem(old_item)
                    old_layout.deleteLater()
                    layout.insertItem(i, item)
            elif isinstance(item, QSpacerItem):
                old_spacer = old_item.spacerItem()
                if not (old_spacer is item):
                    layout.removeItem(old_item)
                    layout.insertItem(i, item)
            else:
                raise TypeError(f"Wrong element type: {item}")


class HBox(BoxContainer):
    def __init__(self, label="", trap=None):
        super().__init__(label, trap=trap)

    def create_layout(self, parent):
        val = QHBoxLayout(parent)
        return val


class VBox(BoxContainer):
    def __init__(self, label="", trap=None):
        super().__init__(label, trap=trap)

    def create_layout(self, parent):
        return QVBoxLayout(parent)
