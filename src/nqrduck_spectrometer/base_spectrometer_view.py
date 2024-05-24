"""The Base Class for all Spectrometer Views."""

import logging
from PyQt6.QtWidgets import (
    QWidget,
    QLabel,
    QHBoxLayout,
    QSizePolicy,
    QSpacerItem,
    QVBoxLayout,
    QPushButton,
)
from nqrduck.module.module_view import ModuleView
from nqrduck.assets.icons import Logos

logger = logging.getLogger(__name__)


class BaseSpectrometerView(ModuleView):
    """The View Class for all Spectrometers."""

    def __init__(self, module):
        """Initializes the spectrometer view."""
        super().__init__(module)

    def load_settings_ui(self) -> None:
        """This method automatically generates a view for the settings of the module.

        If there is a widget file that has been generated by Qt Designer, it will be used. Otherwise, a default view will be generated.
        """
        from .base_spectrometer_widget import Ui_Form

        widget = QWidget()
        widget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self._ui_form = Ui_Form()
        self.widget = widget
        self._ui_form.setupUi(self)

        grid = self._ui_form.gridLayout
        self._ui_form.verticalLayout.removeItem(self._ui_form.gridLayout)
        # Add name of the spectrometer to the view
        label = QLabel(f"{self.module.model.toolbar_name} Settings:")
        label.setStyleSheet("font-weight: bold;")
        self._ui_form.verticalLayout.setSpacing(5)
        self._ui_form.verticalLayout.addWidget(label)
        self._ui_form.verticalLayout.addLayout(grid)

        for category_count, category in enumerate(self.module.model.settings.keys()):
            logger.debug("Adding settings for category: %s", category)
            category_layout = QVBoxLayout()
            category_label = QLabel(f"{category}:")
            category_label.setStyleSheet("font-weight: bold;")
            row = category_count // 2
            column = category_count % 2

            category_layout.addWidget(category_label)
            for setting in self.module.model.settings[category]:
                logger.debug("Adding setting to settings view: %s", setting.name)

                spacer = QSpacerItem(20, 20)
                # Create a label for the setting
                setting_label = QLabel(setting.name)
                setting_label.setMinimumWidth(200)

                edit_widget = setting.widget
                logger.debug("Setting widget: %s", edit_widget)

                # Add a icon that can be used as a tooltip
                if setting.description is not None:
                    logger.debug("Adding tooltip to setting: %s", setting.name)
                    icon = Logos.QuestionMark_16x16()
                    icon_label = QLabel()
                    icon_label.setPixmap(icon.pixmap(icon.availableSizes()[0]))
                    icon_label.setFixedSize(icon.availableSizes()[0])

                    icon_label.setToolTip(setting.description)

                # Add a horizontal layout for the setting
                layout = QHBoxLayout()
                # Add the label and the line edit to the layout
                layout.addItem(spacer)
                layout.addWidget(setting_label)
                layout.addWidget(edit_widget)
                layout.addStretch(1)
                layout.addWidget(icon_label)

                # Add the layout to the vertical layout of the widget
                category_layout.addLayout(layout)

            category_layout.addStretch(1)
            self._ui_form.gridLayout.addLayout(category_layout, row, column)

        # Push all the settings to the top of the widget
        self._ui_form.verticalLayout.addStretch(1)

        # Now we add a save and load button to the widget
        self.button_layout = QHBoxLayout()
        self.save_button = QPushButton("Save Settings")
        self.save_button.setIcon(Logos.Save16x16())
        #self.save_button.setIconSize(self.save_button.size())
        self.save_button.clicked.connect(self.on_save_button_clicked)
        self.button_layout.addWidget(self.save_button)

        self.load_button = QPushButton("Load Settings")
        self.load_button.setIcon(Logos.Load16x16())
        #self.load_button.setIconSize(self.load_button.size())
        self.load_button.clicked.connect(self.on_load_button_clicked)
        self.button_layout.addWidget(self.load_button)

        self._ui_form.verticalLayout.addLayout(self.button_layout)


    def on_save_button_clicked(self):
        """This method is called when the save button is clicked."""
        logger.debug("Save button clicked")
        # Open a dialog to save the settings to a file
        file_manager = self.FileManager(
            extension=self.module.model.SETTING_FILE_EXTENSION, parent=self
        )
        path = file_manager.saveFileDialog()
        if path:
            self.module.controller.save_settings(path)

    def on_load_button_clicked(self):
        """This method is called when the load button is clicked."""
        logger.debug("Load button clicked")
        # Open a dialog to load the settings from a file
        file_manager = self.FileManager(
            extension=self.module.model.SETTING_FILE_EXTENSION, parent=self
        )
        path = file_manager.loadFileDialog()
        self.module.controller.load_settings(path)
        if path:
            self.module.controller.load_settings(path)
