from typing import Optional

from qtpy.QtCore import (
    Qt,
    Signal,
)
from qtpy.QtWidgets import (
    QDialog,
    QDialogButtonBox,
    QGridLayout,
    QLabel,
    QWidget,
)

from ert.gui.ertnotifier import ErtNotifier
from ert.gui.ertwidgets import StringBox, TextModel
from ert.validation.proper_name_argument import (
    ExperimentValidation,
    ProperNameArgument,
)


class CreateExperimentDialog(QDialog):
    onDone = Signal(str, str)

    def __init__(
        self,
        notifier: ErtNotifier,
        title: str = "Create new experiment",
        parent: Optional[QWidget] = None,
    ) -> None:
        QDialog.__init__(self, parent=parent)
        self.setModal(True)
        self.setWindowTitle(title)
        self.setFixedSize(450, 120)

        layout = QGridLayout()

        experiment_label = QLabel("Experiment name:")
        self._experiment_edit = StringBox(
            TextModel(""), placeholder_text="My_experiment", minimum_width=200
        )
        self._experiment_edit.setValidator(ExperimentValidation(notifier.storage))

        ensemble_label = QLabel("Ensemble name:")
        self._ensemble_edit = StringBox(
            TextModel(""), placeholder_text="My_ensemble", minimum_width=200
        )
        self._ensemble_edit.setValidator(ProperNameArgument())

        buttons = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel,
            Qt.Orientation.Horizontal,
            self,
        )
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        ok_button = buttons.button(QDialogButtonBox.Ok)
        assert ok_button
        self._ok_button = ok_button

        self._ok_button.clicked.connect(
            lambda: self.onDone.emit(
                self._experiment_edit.text(), self._ensemble_edit.text()
            )
        )
        self._ok_button.setEnabled(False)

        def enableOkButton() -> None:
            self._ok_button.setEnabled(self.isConfigurationValid())

        self._experiment_edit.textChanged.connect(enableOkButton)
        self._ensemble_edit.textChanged.connect(enableOkButton)

        layout.addWidget(experiment_label, 0, 0)
        layout.addWidget(self._experiment_edit, 0, 1)
        layout.addWidget(ensemble_label, 1, 0)
        layout.addWidget(self._ensemble_edit, 1, 1)
        layout.addWidget(buttons, 2, 1)

        self.setLayout(layout)

        self._experiment_edit.getValidationSupport().validationChanged.connect(
            enableOkButton
        )

        self._ensemble_edit.getValidationSupport().validationChanged.connect(
            enableOkButton
        )

        self._experiment_edit.setFocus()

    @property
    def experiment_name(self) -> str:
        return self._experiment_edit.text()

    @property
    def ensemble_name(self) -> str:
        return self._ensemble_edit.text()

    def isConfigurationValid(self) -> bool:
        return self._experiment_edit.isValid() and self._ensemble_edit.isValid()
