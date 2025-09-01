"""Program to import pictures from a camera and organize them into folders by capture date."""

from gui.ui_main import Ui_MainWindow
from image_worker import IterateImages
from paths import DEFAULT_OUTPUT_PATH, ICON_PATH, SOURCE_PATH
import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QMessageBox, QFileDialog
from PySide6.QtCore import QThread
from PySide6.QtGui import QIcon
import os
import traceback


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
        except Exception:
            self._show_error(traceback.format_exc())

    def import_pictures(self):
        try:
            self.progress_bar.resetFormat()
            self.import_btn.setDisabled(True)
            thread = QThread()
            worker = IterateImages(self.output_path, SOURCE_PATH)

            # worker.moveToThread(thread)

            thread.started.connect(worker.run)
            worker.finished_work.connect(self.finish)
            worker.progress.connect(self.update_progress)
            worker.file_count.connect(self.set_progress_maximum)
            worker.error.connect(self.on_error)

            worker.finished_work.connect(thread.quit)
            thread.finished.connect(lambda: self.cleanup_threads(thread, worker))

            thread.finished.connect(thread.deleteLater)
            worker.finished_work.connect(worker.deleteLater)

            thread.start()
            self.main_threads[worker] = thread

        except Exception:
            self._show_error(traceback.format_exc())

    def on_error(self, error: str):
        self._show_error(error)

    def finish(self):
        self.import_btn.setEnabled(True)

    def cleanup_threads(self, thread: QThread, worker: IterateImages):
        try:
            if thread in self.main_threads.values():
                thread.wait()
                del self.main_threads[worker]
        except Exception:
            self._show_error(traceback.format_exc())

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
