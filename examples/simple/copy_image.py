from config import Config
from framework import ConfigAlgFramework
from property import PropertyUpdation, PropertyQueryer
import components as c
from PIL import Image as Image


def f_config(config: dict):
    path = config["path"]
    updation = PropertyUpdation()
    updation.add_updation("image1", "path", path)
    return updation


def f_alg(config: dict, queryer: PropertyQueryer):
    updation = PropertyUpdation()
    updation.add_updation("image2", "image", queryer.query("image1", "image"))
    return updation


def main():
    rt = c.RegionComponent("root")(
        c.HBox()(
            c.Image("image1", width=200, height=200),
            c.Image("image2", width=200, height=200),
        )
    )
    config = Config()
    config.add_config("path", Config.Type.PATH)

    framework = ConfigAlgFramework(
        rt, config, f_config=f_config, f_alg=f_alg, automatic=False
    )
    framework.exec_gui()


if __name__ == "__main__":
    main()
