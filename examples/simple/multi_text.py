import components as c

from framework import ConfigAlgFramework
from config import Config
from property import PropertyUpdation


def f_alg(d, queryer):
    try:
        i = int(queryer.query("t1::1", "text"))
        updation = PropertyUpdation()
        updation.add_updation("t1::1", "text", str(i + 4))
        updation.add_updation("t2::1", "text", str(i + 1))
        updation.add_updation("t3::1", "text", str(i + 2))
        updation.add_updation("t4::1", "text", str(i + 3))
        return updation
    except ValueError:
        return PropertyUpdation()


def main():
    texts = c.RegionComponent("t1")(c.HBox()(c.Text("1", "1"), c.Text("2", "2")))
    rt = c.RegionComponent("root")(
        texts, texts.copy("t2"), texts.copy("t3"), texts.copy("t4")
    )
    config = Config()
    framework = ConfigAlgFramework(rt, config, f_alg=f_alg)
    framework.exec_gui()


if __name__ == "__main__":
    main()
