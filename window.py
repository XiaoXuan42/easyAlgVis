from config import Config
from PySide6.QtWidgets import (
    QWidget,
    QDialog,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QFileDialog
)
from PySide6.QtGui import QRegularExpressionValidator
from typing import Dict


class ConfigDialog(QDialog):
    def __init__(self, config: Config, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.item2widget: Dict[str, QLineEdit] = {}
        self.build_from_config(config)

    def _filepath_line_edit_btn(self, hlayout):
        line_edit = QLineEdit()
        btn = QPushButton("Open")

        def _filepath_btn_clicked():
            nonlocal line_edit
            dialog = QFileDialog(self)
            dialog.setFileMode(QFileDialog.FileMode.AnyFile)
            ret = dialog.exec()
            if ret == QDialog.DialogCode.Accepted:
                filelist = dialog.selectedFiles()
                if filelist:
                    line_edit.setText(filelist[-1])

        btn.clicked.connect(_filepath_btn_clicked)
        hlayout.addWidget(line_edit)
        hlayout.addWidget(btn)
        return line_edit, btn

    def build_from_config(self, config: Config):
        vlayout = QVBoxLayout(self)

        for name, type in config:
            hlayout = QHBoxLayout()
            label = QLabel()
            label.setText(name + ": ")
            hlayout.addWidget(label)

            value = config.get_value(name)

            if (
                type == config.Type.INT
                or type == config.Type.FLOAT
                or type == config.Type.STR
            ):
                widget = QLineEdit()
                if type == config.Type.INT:
                    validator = QRegularExpressionValidator(r"-?[0-9]+", widget)
                    widget.setValidator(validator)
                elif type == config.Type.FLOAT:
                    re = r"-?(([0-9]*\.?[0-9]+)|([0-9]+e-?[0-9]+))"
                    validator = QRegularExpressionValidator(re, widget)
                    widget.setValidator(validator)
                widget.setText(str(value))
                self.item2widget[name] = widget
                hlayout.addWidget(widget)

            elif type == config.Type.PATH:
                line_edit, _ = self._filepath_line_edit_btn(hlayout)
                line_edit.setText(str(value))
                self.item2widget[name] = line_edit

            else:
                raise ValueError(f"Invalid configuration type: {type}")

            vlayout.addLayout(hlayout)

        edit_btn = QPushButton("edit")
        cancel_btn = QPushButton("cancel")
        edit_btn.clicked.connect(self.accept)
        cancel_btn.clicked.connect(self.reject)
        btn_hlayout = QHBoxLayout()
        btn_hlayout.addWidget(edit_btn)
        btn_hlayout.addWidget(cancel_btn)
        vlayout.addLayout(btn_hlayout)

        self.setLayout(vlayout)

    def update_config(self, config: Config) -> bool:
        for name, widget in self.item2widget.items():
            config.set_value(name, widget.text())
