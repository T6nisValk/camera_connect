"""Program to import pictures from a camera and organize them into folders by capture date."""

from gui.ui_main import Ui_MainWindow
import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QMessageBox, QFileDialog
from PySide6.QtCore import Signal, QThread, QObject
from PySide6.QtGui import QIcon
import os
import shutil
import datetime

SOURCE_PATH = r"C:\Users\valk_to\Desktop\source"
DEFAULT_OUTPUT_PATH = r"C:\Users\valk_to\Desktop\output"
ICON_PATH = r"assets\camera.ico"


class IterateImages(QObject):
    finished_work = Signal()
    progress = Signal(int)
    file_count = Signal(int)

    def __init__(self, output_path):
        super().__init__()
        self.output_path = output_path

    def run(self):
        total_files = self.count_files()
        self.file_count.emit(total_files)
        processed = 0
        for image in os.scandir(SOURCE_PATH):
            c_time = os.path.getmtime(image.path)
            creation_date = datetime.datetime.fromtimestamp(c_time).strftime(r"%Y-%m-%d")
            creation_date_folder = f"{self.output_path}/{creation_date}"
            jpg_folder = f"{creation_date_folder}/JPG"
            raw_folder = f"{creation_date_folder}/RAW"
            self.make_directories([creation_date_folder, jpg_folder, raw_folder])
            self.move_image(image, raw_folder, jpg_folder)
            processed += 1
            self.progress.emit(processed)
        self.finished_work.emit()

    def move_image(self, image: os.DirEntry, raw_folder: os.path, jpg_folder: os.path):
        if image.name.lower().endswith(("jpg", "jpeg")):
            shutil.copy(image.path, jpg_folder)
        elif image.name.lower().endswith("arw"):
            shutil.copy(image.path, raw_folder)

    def make_directories(self, paths: list):
        for path in paths:
            os.makedirs(path, exist_ok=True)

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
            self.output_path = QFileDialog.getExistingDirectory(
                self.window, caption="Choose A Folder", dir=self.output_path
            )
            print(self.output_path)
        except Exception as e:
            self._show_error(str(e))

    def import_pictures(self):
        try:
            self.progress_bar.resetFormat()
            self.import_btn.setDisabled(True)
            thread = QThread()
            worker = IterateImages(self.output_path)
            worker.moveToThread(thread)

            thread.started.connect(worker.run)
            worker.file_count.connect(self.set_progress_maximum)
            worker.progress.connect(self.update_progress)
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
            if thread.isRunning():
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
