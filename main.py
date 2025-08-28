"""Program to import pictures from a camera and organize them into folders by capture date."""

from gui.ui_main import Ui_MainWindow
import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QMessageBox, QFileDialog
from PySide6.QtCore import Signal, QThread, QObject, Slot, Qt
from PySide6.QtGui import QIcon
import os
import time
import shutil
import datetime

SOURCE_PATH = r"C:\Users\valk_to\Desktop\source"
DEFAULT_OUTPUT_PATH = r"C:\Users\valk_to\Desktop\output"
ICON_PATH = r"assets\camera.ico"


class IterateImages(QObject):
    finished_work = Signal()
    progress = Signal(int)
    file_count = Signal(int)
    error = Signal(str)

    def __init__(self):
        super().__init__()

    def run(self):
        try:
            total_files = self.count_files()
            self.file_count.emit(total_files)
            for i in range(1, total_files + 1):
                self.progress.emit(i)
                time.sleep(0.1)
            self.finished_work.emit()
        except Exception as e:
            self.error.emit(str(e))

    def count_files(self):
        with os.scandir(SOURCE_PATH) as entries:
            file_count = sum(1 for entry in entries if entry.is_file())

        return int(file_count)


class ImportPictures(Ui_MainWindow):
    def __init__(self, window):
        self.window = window
        self.setupUi(self.window)

        self.main_threads = {}
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
            self.output_path = QFileDialog.getExistingDirectory(self.window, caption="Choose A Folder")
        except Exception as e:
            self._show_error(str(e))

    def import_pictures(self):
        try:
            self.import_btn.setDisabled(True)
            thread = QThread()
            worker = IterateImages()
            worker.moveToThread(thread)

            thread.started.connect(worker.run)
            worker.file_count.connect(self.set_progress_maximum)
            worker.progress.connect(self.update_progress)
            worker.error.connect(self._show_error)
            worker.finished_work.connect(self.finish)

            worker.finished_work.connect(thread.quit)
            thread.finished.connect(lambda: self.cleanup_threads(thread))

            worker.finished_work.connect(worker.deleteLater)
            thread.finished.connect(thread.deleteLater)
            thread.start()
            self.main_threads[worker] = thread

        except Exception as e:
            self._show_error(str(e))

    def finish(self):
        self.import_btn.setEnabled(True)

    def cleanup_threads(self, thread: QThread):
        try:
            if thread in self.main_threads.values():
                thread.quit()
                thread.wait()
        except Exception as e:
            self._show_error(str(e))

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


def main():
    app = QApplication(sys.argv)
    app_window = QMainWindow()
    window = ImportPictures(app_window)
    window.window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
