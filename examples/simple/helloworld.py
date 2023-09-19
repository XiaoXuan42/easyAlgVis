from framework import ConfigAlgFramework
from property import PropertyUpdation
from config import Config
import components as c


def f_config(config: dict):
    return PropertyUpdation()


def f_alg(config: dict, queryer):
    updation = PropertyUpdation()
    updation.add_updation("text1", "text", config["text"])
    return updation


def main():
    rt = c.RootComponent()(c.Text("text1", text="hello world"))
    config = Config()
    config.add_config("text", config.Type.STR, default_value="hello world")
    framwork = ConfigAlgFramework(
        rt, config, f_config=f_config, f_alg=f_alg, automatic=True
    )
    framwork.exec_gui()


if __name__ == "__main__":
    main()
