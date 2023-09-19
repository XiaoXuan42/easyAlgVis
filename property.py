import components

class PropertyUpdation:
    def __init__(self):
        # label -> Dict[property, value]
        self.label2updation = {}
    
    def add_updation(self, label, property, value):
        d_label = self.label2updation.setdefault(label, {})
        d_label[property] = value

    def update_properties(self, rt: components.RootComponent):
        for label, updates in self.label2updation.items():
            c = rt.get_component(label)
            if not c:
                raise RuntimeError(label, f"{label} not found")
            for p, v in updates.items():
                c.set_property(p, v)


class PropertyQueryer:
    def __init__(self, rt: components.RootComponent) -> None:
        self.rt = rt

    def query(self, label, property=None):
        if property is None:
            return self.rt.get_component(label)
        else:
            return self.rt.get_component(label).get_property(property)
