from typing import Callable
from property import PropertyUpdation, PropertyQueryer
from config import Config
from window import ConfigDialog
from PySide6.QtWidgets import *
import components


class InputAlgOutFramwork:
    def __init__(
        self,
        rt: components.RootComponent,
        config: Config,
        f_config: Callable[[dict], PropertyUpdation],
        f_alg: Callable[[PropertyQueryer], PropertyUpdation],
    ):
        """
        Routine:
            configuration changed --> input updation --> prepare input -->
            run algorithm --> output updation
        """
        self.rt = rt
        self.config = config
        self.f_config = f_config
        self.f_alg = f_alg

        self._create_gui()

    def on_config_btn_clicked(self):
        cdialog = ConfigDialog(self.config, self.main_widget)
        ret = cdialog.exec()
        if ret == cdialog.DialogCode.Accepted:
            cdialog.update_config(self.config)
            self.run()
            self.update_gui()

    def _create_gui(self):
        self.main_widget = QWidget()
        self.vlayout = QVBoxLayout(self.main_widget)
        self.components_gui = self.rt.create(None)
        config_btn = QPushButton("Config")
        config_btn.clicked.connect(self.on_config_btn_clicked)
        self.vlayout.addLayout(self.components_gui)
        self.vlayout.addWidget(config_btn)
        self.main_widget.setLayout(self.vlayout)

    def update_gui(self):
        new_components_gui = self.rt.update(self.components_gui, self.main_widget)
        if not (new_components_gui is self.components_gui):
            self.vlayout.removeItem(self.components_gui)
            self.vlayout.insertLayout(0, new_components_gui)
            self.components_gui = new_components_gui

    def show(self):
        self.main_widget.show()

    def run(self):
        config = self.config.to_dict()
        updation = self.f_config(config)
        updation.update_properties(self.rt)
        queryer = PropertyQueryer(self.rt)
        output_updation = self.f_alg(queryer)
        output_updation.update_properties(self.rt)
