"""Program to import pictures from a camera and organize them into folders by capture date."""

from gui.main_ui import Ui_MainWindow
from image_worker import IterateImages
from paths import DEFAULT_OUTPUT_PATH, ICON_PATH, SOURCE_PATH
import sys
from PySide6.QtWidgets import QMessageBox, QFileDialog, QMainWindow
from PySide6.QtCore import QThread, QObject
from PySide6.QtGui import QIcon
import os


class ImportPictures(QObject, Ui_MainWindow):
    def __init__(self, window: QMainWindow):
        super().__init__()
        self.window = window
        self.setupUi(self.window)

        self.output_path = DEFAULT_OUTPUT_PATH
        self.window.setWindowTitle("Simple Importer")
        self.window.setWindowIcon(QIcon(self.get_absolute_path(ICON_PATH)))

        # Signals
        self.new_output_btn.clicked.connect(self.set_new_output_path)
        self.import_btn.clicked.connect(self.import_pictures)
        self.progress_bar.valueChanged.connect(self.update_progress_color)

    def set_progress_maximum(self, value):
        self.progress_bar.setMaximum(value)

    def update_progress_color(self, value):
        if value < self.progress_bar.maximum():
            self.progress_bar.setStyleSheet("QProgressBar::chunk {background-color: rgb(200, 160, 0);}")
        else:
            self.progress_bar.setStyleSheet("QProgressBar::chunk {background-color: rgb(0, 160, 112);}")
            self.progress_bar.setFormat(f"Done Importing {self.progress_bar.maximum()} Images!")

    def set_new_output_path(self):
        try:
            self.output_path = QFileDialog.getExistingDirectory(self.window, caption="Choose A Folder", dir=self.output_path)
            print(self.output_path)
        except Exception as e:
            self._show_error(str(e))

    def import_pictures(self):
        if not self.jpg_checkbox.isChecked() and not self.raw_checkbox.isChecked():
            self._show_error("No file type selected.")
            return

        self.progress_bar.resetFormat()
        self.import_btn.setDisabled(True)

        thread = QThread()
        worker = IterateImages(
            self.output_path,
            SOURCE_PATH,
            {"jpg": self.jpg_checkbox.checkState(), "raw": self.raw_checkbox.checkState()},
        )
        worker.setObjectName("Image Worker")
        worker.moveToThread(thread)

        thread.started.connect(worker.run)

        worker.progress.connect(self.update_progress)
        worker.file_count.connect(self.set_progress_maximum)
        worker.error.connect(self._show_error)

        worker.finished.connect(self._reset_button)
        worker.finished.connect(thread.quit)
        thread.finished.connect(lambda: self.cleanup_threads(thread, worker))

        thread.start()

    def _reset_button(self):
        self.import_btn.setEnabled(True)

    def cleanup_threads(self, thread: QThread, worker: QObject):
        thread.quit()
        thread.deleteLater()
        worker.deleteLater()

    def update_progress(self, value):
        self.progress_bar.setValue(value)

    # -- Helper Functions --
    def get_absolute_path(self, relative_path):
        """Get absolute path to resource, works for dev and for PyInstaller."""
        try:
            base_path = sys._MEIPASS
        except AttributeError:
            base_path = os.path.abspath(".")
        return os.path.join(base_path, relative_path)

    def _show_warning(self, message):
        QMessageBox.warning(self.window, "Warning", message)

    def _show_error(self, message):
        QMessageBox.critical(self.window, "Error", message)

    def _show_info(self, message):
        QMessageBox.information(self.window, "Info", message)
