from typing import Callable
from property import PropertyUpdation, PropertyQueryer
from config import Config
from window import ConfigDialog
from PySide6.QtWidgets import *
import components


class ConfigAlgFramework:
    def __init__(
        self,
        rt: components.RootComponent,
        config: Config,
        f_config: Callable[[dict], PropertyUpdation],
        f_alg: Callable[[dict, PropertyQueryer], PropertyUpdation],
        automatic=False,
        title=None
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
        self.automatic = automatic
        self.title = title

    def on_config_btn_clicked(self):
        cdialog = ConfigDialog(self.config, self.main_widget)
        ret = cdialog.exec()
        if ret == cdialog.DialogCode.Accepted:
            cdialog.update_config(self.config)
            updation = self.f_config(self.config.to_dict())
            updation.update_properties(self.rt)
            if self.automatic:
                self.run_alg()
            self.update_gui()

    def on_run_btn_clicked(self):
        self.run_alg()
        self.update_gui()

    def _create_gui(self):
        self.main_widget = QWidget()
        self.vlayout = QVBoxLayout(self.main_widget)
        self.components_gui = self.rt.create(None)

        hlayout = QHBoxLayout()
        config_btn = QPushButton("Config")
        config_btn.clicked.connect(self.on_config_btn_clicked)
        hlayout.addWidget(config_btn)

        if not self.automatic:
            run_btn = QPushButton("Run")
            run_btn.clicked.connect(self.on_run_btn_clicked)
            hlayout.addWidget(run_btn)

        self.vlayout.addLayout(self.components_gui)
        self.vlayout.addLayout(hlayout)

        self.main_widget.setLayout(self.vlayout)

        if self.title:
            self.main_widget.setWindowTitle(self.title)

    def update_gui(self):
        new_components_gui = self.rt.update(self.components_gui, self.main_widget)
        if not (new_components_gui is self.components_gui):
            self.vlayout.removeItem(self.components_gui)
            self.vlayout.insertLayout(0, new_components_gui)
            self.components_gui = new_components_gui

    def run_alg(self):
        queryer = PropertyQueryer(self.rt)
        d_config = self.config.to_dict()
        output_updation = self.f_alg(d_config, queryer)
        output_updation.update_properties(self.rt)

    def show(self):
        self.main_widget.show()

    def exec_gui(self):
        app = QApplication()
        self._create_gui()
        self.show()
        app.exec()
