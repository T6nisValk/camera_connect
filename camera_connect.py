"""Program to import pictures from a camera and organize them into folders by capture date."""

from gui.main_ui import Ui_MainWindow
from gui.settings_ui import Ui_Settings
from image_worker import IterateImages
from paths import DEFAULT_PATH, ICON_PATH, SOURCE_PATH
import sys
from PySide6.QtWidgets import QMessageBox, QFileDialog, QMainWindow, QDialog
from PySide6.QtCore import QThread, QObject
from PySide6.QtGui import QIcon
import os
import json


class Settings(QDialog, Ui_Settings):
    def __init__(self, parent=None):
        super().__init__()
        self.setupUi(self)

        self.current_settings()

        self.saveButton.clicked.connect(self.save_settings)
        self.browseOutputButton.clicked.connect(self.set_output_path)
        self.browseSourceButton.clicked.connect(self.set_source_path)

    def set_output_path(self):
        output_path = QFileDialog.getExistingDirectory(self, caption="Choose A Folder", dir=DEFAULT_PATH)
        if output_path:  # Only update if user selected a folder
            self.outputPathLabel.setText(output_path)

    def set_source_path(self):
        source_path = QFileDialog.getExistingDirectory(self, caption="Choose A Folder", dir=DEFAULT_PATH)
        if source_path:  # Only update if user selected a folder
            self.sourcePathLabel.setText(source_path)

    def save_settings(self):
        output_path = self.outputPathLabel.text()
        source_path = self.sourcePathLabel.text()
        jpg = self.jpgCheckBox.isChecked()
        raw = self.rawCheckBox.isChecked()

        if not jpg and not raw:
            QMessageBox.critical(self, "Error", "At least one file type must be selected.")
            return

        self.settings = {
            "OutputPath": output_path,
            "SourcePath": source_path,
            "FileTypes": {
                "JPG": jpg,
                "RAW": raw,
            },
        }

        with open("settings.json", "w") as write:
            json.dump(self.settings, write, indent=4)

        self.close()

    def current_settings(self):
        self.settings = self.read_settings()
        output_path = self.settings.get("OutputPath")
        source_path = self.settings.get("SourcePath")
        jpg = self.settings.get("FileTypes").get("JPG")
        raw = self.settings.get("FileTypes").get("RAW")

        self.outputPathLabel.setText(output_path)
        self.sourcePathLabel.setText(source_path)
        self.jpgCheckBox.setChecked(jpg)
        self.rawCheckBox.setChecked(raw)

    def read_settings(self):
        with open(r"settings.json", "r") as settings_file:
            settings = json.load(settings_file)
        return settings


class ImportPictures(QObject, Ui_MainWindow):
    def __init__(self, window: QMainWindow):
        super().__init__()
        self.window = window
        self.setupUi(self.window)

        # Load settings from file
        settings = self.read_settings()
        self.output_path = settings.get("OutputPath", DEFAULT_PATH)
        self.source_path = settings.get("SourcePath", SOURCE_PATH)
        self.file_types = settings.get("FileTypes", {"JPG": True, "RAW": False})

        self.window.setWindowTitle("Simple Importer")
        self.window.setWindowIcon(QIcon(self.get_absolute_path(ICON_PATH)))

        # Signals
        self.import_btn.clicked.connect(lambda: self.import_pictures(copy=True))
        self.import_and_delete_btn.clicked.connect(lambda: self.import_pictures(copy=False))
        self.progress_bar.valueChanged.connect(self.update_progress_color)

        self.settingsAction.triggered.connect(self.open_settings)

    def open_settings(self):
        settings_dialog = Settings(self)
        settings_dialog.exec()
        # Reload settings after dialog closes
        settings = self.read_settings()
        self.output_path = settings.get("OutputPath", DEFAULT_PATH)
        self.source_path = settings.get("SourcePath", SOURCE_PATH)
        self.file_types = settings.get("FileTypes", {"JPG": True, "RAW": False})

    def update_progress_color(self, value):
        if value < self.progress_bar.maximum():
            self.progress_bar.setStyleSheet("QProgressBar::chunk {background-color: rgb(200, 160, 0);}")
        else:
            self.progress_bar.setStyleSheet("QProgressBar::chunk {background-color: rgb(0, 160, 112);}")
            self.progress_bar.setFormat(f"Done Importing {self.progress_bar.maximum()} Images!")

    def import_pictures(self, copy=True):
        # Show confirmation dialog
        if not self._confirm_import(copy):
            return

        self.progress_bar.resetFormat()
        self.import_btn.setDisabled(True)

        thread = QThread()
        worker = IterateImages(
            self.output_path,
            self.source_path,
            copy,
            {"jpg": self.file_types.get("JPG", True), "raw": self.file_types.get("RAW", False)},
        )
        worker.setObjectName("Image Worker")
        worker.moveToThread(thread)

        thread.started.connect(worker.run)

        worker.progress.connect(lambda value: self.progress_bar.setValue(value))
        worker.file_count.connect(lambda value: self.progress_bar.setMaximum(value))
        worker.error.connect(self._show_error)
        worker.error.connect(lambda: self.import_btn.setEnabled(True))

        worker.finished.connect(lambda: self.import_btn.setEnabled(True))
        thread.finished.connect(lambda: self.cleanup_threads(thread, worker))

        thread.start()

    def cleanup_threads(self, thread: QThread, worker: QObject):
        thread.quit()
        thread.deleteLater()
        worker.deleteLater()

    # -- Helper Functions --
    def _confirm_import(self, copy=True):
        """Show confirmation dialog with current import settings."""
        # Build file types string
        file_types = []
        if self.file_types.get("JPG", False):
            file_types.append("JPG")
        if self.file_types.get("RAW", False):
            file_types.append("RAW")

        file_types_str = ", ".join(file_types) if file_types else "None"

        # Build confirmation message
        action = "Copy" if copy else "Move"
        message = (
            f"Ready to {action.lower()} images with the following settings:\n\n"
            f"Action: {action}\n"
            f"File Types: {file_types_str}\n"
            f"Source: {self.source_path}\n"
            f"Destination: {self.output_path}\n\n"
            f"Do you want to continue?"
        )

        reply = QMessageBox.question(self.window, f"Confirm {action}", message, QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        return reply == QMessageBox.Yes

    def read_settings(self):
        """Read settings from settings.json file."""
        try:
            with open("settings.json", "r") as settings_file:
                settings = json.load(settings_file)
            return settings
        except (FileNotFoundError, json.JSONDecodeError):
            # Return default settings if file doesn't exist or is invalid
            return {"OutputPath": DEFAULT_PATH, "SourcePath": SOURCE_PATH, "FileTypes": {"JPG": True, "RAW": False}}

    def get_absolute_path(self, relative_path):
        """Get absolute path to resource, works for dev and for PyInstaller."""
        try:
            base_path = sys._MEIPASS
        except AttributeError:
            base_path = os.path.abspath(".")
        return os.path.join(base_path, relative_path)

    def _show_error(self, message):
        QMessageBox.critical(self.window, "Error", message)
