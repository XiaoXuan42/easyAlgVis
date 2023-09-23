import components as c
from framework import ConfigAlgFramework
from config import Config


def main():
    rt = c.RegionComponent("root")(
        c.LineEdit("", "")
    )
    config = Config()
    framework = ConfigAlgFramework(rt, config, automatic=True, title="print directly")

    def trap(c, e):
        if e.name == "text_changed":
            print(e.data)

    framework.set_root_trap(trap=trap)
    framework.exec_gui()

if __name__ == "__main__":
    main()
