from config import Config
from framework import InputAlgOutFramwork
from property import PropertyUpdation, PropertyQueryer
from PySide6.QtWidgets import QApplication
import components as c
from PIL import Image as Image


def f_config(config: dict):
    path = config["path"]
    updation = PropertyUpdation()
    updation.add_updation("image1", "path", path)
    return updation


def f_alg(queryer: PropertyQueryer):
    updation = PropertyUpdation()
    updation.add_updation("image2", "image", queryer.query("image1", "image"))
    return updation


def main():
    app = QApplication()
    rt = c.RootComponent()(
        c.HBox()(
            c.Image("image1", width=200, height=200),
            c.Image("image2", width=200, height=200),
        )
    )
    config = Config()
    config.add_config("path", Config.Type.PATH)

    framework = InputAlgOutFramwork(
        rt, config, f_config=f_config, f_alg=f_alg
    )
    framework.show()
    import sys

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
