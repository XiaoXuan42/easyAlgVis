import components as c
from config import Config
from framework import ConfigAlgFramework

def main():
    def trap(c, e):
        try:
            c_text = c.get_component("text")
            val = int(c_text.text)
            c_text.set_property("text", str(val + 1))
            return e
        except ValueError:
            return None

    a1 = c.RegionComponent("a1")(c.Text("text", "0"), c.PushButton("", "add"))
    a1.set_trap(trap)
    a2, a3, a4 = a1.copy("a2"), a1.copy("a3"), a1.copy("a4")

    rt = c.RegionComponent("root")(
        c.HBox()(a1, a2),
        c.HBox()(a3, a4),
    )
    config = Config()
    framework = ConfigAlgFramework(rt, config)

    def root_trap(c, e):
        framework.update_gui()

    framework.set_root_trap(root_trap)
    framework.exec_gui()


if __name__ == "__main__":
    main()
