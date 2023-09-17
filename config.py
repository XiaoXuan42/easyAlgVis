import enum
from typing import Dict


class Config:
    @enum.unique
    class Type(enum.IntEnum):
        INT = enum.auto()
        FLOAT = enum.auto()
        STR = enum.auto()
        PATH = enum.auto()

    configtype2pytype = {
        Type.INT: int,
        Type.FLOAT: float,
        Type.STR: str,
        Type.PATH: str,
    }

    def __init__(self) -> None:
        self.config_types: Dict[str, Config.Type] = {}
        self.values = {}

    def init_zero_value(self, type):
        if type == self.Type.INT:
            return 0
        elif type == self.Type.FLOAT:
            return 0.0
        elif type == self.Type.STR:
            return ""
        elif type == self.Type.PATH:
            return ""
        else:
            raise ValueError(f"Invalid configuration type: {type}")

    def add_config(self, name, type: Type, default_value=None):
        self.config_types[name] = type
        if default_value is not None:
            try:
                pytype = self.configtype2pytype[type]
                converted_val = pytype(default_value)
                self.values[name] = converted_val
            except ValueError:
                self.values[name] = self.init_zero_value(type)
        else:
            self.values[name] = self.init_zero_value(type)

    def set_config(self, name, value):
        self.values[name] = value

    def is_correct_type(self, name, value):
        type = self.get_type(name)
        pytype = self.configtype2pytype[type]
        try:
            val = pytype(value)
            return True, val
        except ValueError:
            return False, None

    def set_value(self, name, value: str):
        stat, val = self.is_correct_type(name, value)
        if stat:
            self.values[name] = val
            return True
        return False

    def get_value(self, name):
        return self.values[name]

    def get_type(self, name):
        return self.config_types[name]

    def to_dict(self) -> dict:
        result = {}
        for name in self.config_types.keys():
            result[name] = self.get_value(name)
        return result

    def __iter__(self):
        return iter(self.config_types.items())
