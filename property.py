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
            for p, v in updates:
                c.setproperty(p, v)


class PropertyCollection:
    def __init__(self) -> None:
        # label -> List[Tuple[property, keyname]]
        self.collections = {}

    def add_collection(self, label, property, keyname):
        l_label = self.collections.setdefault(label, [])
        l_label.append((property, keyname))

    def collect_properties(self, rt: components.RootComponent) -> dict:
        result = {}
        for label, targets in self.collections.items():
            c = rt.get_component(label)
            if not c:
                raise RuntimeError(label, f"{label} not found")
            for p, keyname in targets:
                result[keyname] = c.__getattr__(p)
        return result
