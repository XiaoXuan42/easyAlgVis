import components as c
from config import Config
from framework import ConfigAlgFramework
from property import PropertyUpdation


def main():
    cnt = 0
    def f_alg(d, queryer):
        nonlocal cnt
        updation = PropertyUpdation()
        updation.add_updation("text", "text", str(cnt))
        return updation

    rt = c.RegionComponent("root")(
        c.Text("text", "0"),
        c.PushButton("", "add")
    )
    config = Config()
    window = ConfigAlgFramework(rt, config, f_alg=f_alg)

    def root_trap(c, e):
        nonlocal window, cnt
        cnt += 1
        window.run_alg()
        window.update_gui()

    window.set_root_trap(root_trap)
    window.exec_gui()


if __name__ == "__main__":
    main()
