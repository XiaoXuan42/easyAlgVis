from typing import Callable
from property import PropertyUpdation, PropertyCollection
from config import Config
import components


class InputAlgOutFramwork:
    def __init__(
        self,
        rt: components.RootComponent,
        config: Config,
        f_config: Callable[[dict], PropertyUpdation],
        f_collector: Callable[[], PropertyCollection],
        f_alg: Callable[[dict], PropertyUpdation],
    ):
        """
        Routine:
            configuration changed --> input updation --> prepare input -->
            run algorithm --> output updation
        """
        self.rt = rt
        self.config = config
        self.f_config = f_config
        self.f_collector = f_collector
        self.f_alg = f_alg

    def show(self):
        pass

    def run(self):
        config = self.config.to_dict()
        updation = self.f_config(config)
        updation.update_properties(self.rt)
        collector = self.f_collector()
        inputs = collector.collect_properties(self.rt)
        output_updation = self.f_alg(inputs)
        output_updation.update_properties(self.rt)
