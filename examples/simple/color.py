import components as c
from framework import ConfigAlgFramework
from config import Config
from property import PropertyUpdation
import numpy as np


def f_alg(d, queryer):
    try:
        r = int(queryer.query("r", "text"))
        g = int(queryer.query("g", "text"))
        b = int(queryer.query("b", "text"))
        data = np.zeros((100, 100, 3), dtype=np.uint8)
        data += np.array([r, g, b], dtype=np.uint8)
        updation = PropertyUpdation()
        updation.add_updation("image", "data", data)
        return updation
    except ValueError:
        return PropertyUpdation()


def main():
    rt = c.RegionComponent("root")(
        c.HBox()(
            c.VBox()(
                c.LineEdit("r", text="0"),
                c.LineEdit("g", text="0"),
                c.LineEdit("b", text="0")
            ),
            c.Image("image", width=100, height=100)
        )
    )
    config = Config()
    framework = ConfigAlgFramework(rt, config, f_alg=f_alg, title="color")
    def trap(e):
        nonlocal framework
        if e.name == "text_changed":
            framework.run_alg()
            framework.update_gui()
    framework.set_root_trap(trap)
    framework.exec_gui()

if __name__ == "__main__":
    main()
