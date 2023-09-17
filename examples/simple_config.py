from widgets import ConfigDialog, Config
from PySide6.QtWidgets import QApplication
import sys


def main():
    config = Config()
    config.add_config("a", config.Type.INT, 1024)
    config.add_config("b", config.Type.FLOAT, 4201.1024)
    config.add_config("greeting", config.Type.STR)
    config.add_config("filepath", config.Type.PATH)
    app = QApplication()
    dialog = ConfigDialog(config)
    ret = dialog.exec()
    if ret == ConfigDialog.DialogCode.Accepted:
        dialog.update_config(config)
    print(config.to_dict())

if __name__ == "__main__":
    main()
