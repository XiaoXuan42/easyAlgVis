from PySide6.QtWidgets import QWidget
from typing import Optional, List, Dict


class Component:
    def __init__(self, label) -> None:
        self.label = label

    def set_property(self, property, value):
        self.__setattr__(property, value)

    def get_property(self, property):
        return self.__getattr__(property)

    def create_widget(self, parent) -> QWidget:
        raise RuntimeError(f"Forget to implement widget")


class LeafComponent(Component):
    def __init__(self, label) -> None:
        super().__init__(label)

    def update_widget(self, widget: QWidget) -> QWidget:
        return widget


class ContainerComponent(Component):
    def __init__(self, label):
        super().__init__(label)
        self.subcomponents: List[Component] = []

    def post_create_widget(self, widget, subwidgets) -> QWidget:
        raise RuntimeError(f"Forget to implement post create widget")

    def __call__(self, *args):
        self.subcomponents = list(args)


class RootComponent(ContainerComponent):
    def __init__(self) -> None:
        super().__init__("")
        self.label2component: Dict[str, Component] = {}

    def visit_components(self, component, f_pre=None, f_in=None, f_post=None):
        if f_pre:
            f_pre(component)
        if isinstance(component, ContainerComponent):
            for c in component.subcomponents:
                self.visit_components(c, f_pre, f_in, f_post)
                if f_in:
                    f_in(component)
        if f_post:
            f_post(component)

    def _build_refs(self):
        self.label2component = {}

        def f(c):
            if c.label in self.label2component:
                raise RuntimeError(f"Conflict label: {c.label}")
            if c.label:
                self.label2component[c.label] = c

        self.visit_components(self, f_pre=f)

    def get_component(self, label) -> Optional[Component]:
        if label in self.label2component:
            return self.label2component[label]
        return None

    def create_widget(self, parent) -> QWidget:
        return QWidget(parent)

    def __call__(self, *args):
        super().__call__(*args)
        self._build_refs()


class HorizonContainer(ContainerComponent):
    def __init__(self, label):
        super().__init__(label)

    def create_widget(self, parent):
        pass


class VerticalContainer(ContainerComponent):
    def __init__(self, label):
        super().__init__(label)

    def create_widget(self, parent):
        pass


class Image(LeafComponent):
    def __init__(self, label) -> None:
        super().__init__(label)
        self._path = None
        self._img = None

    def create_widget(self):
        pass

    def update_widget(self, widget: QWidget) -> QWidget:
        pass
