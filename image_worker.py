from PySide6.QtCore import Signal, QObject, Qt
import shutil
import os
import datetime
import traceback

RAW_FILES = (".arw",)
JPG_FILES = (".jpg", ".jpeg")


class IterateImages(QObject):
    finished_work = Signal()
    progress = Signal(int)
    file_count = Signal(int)
    error = Signal(str)

    def __init__(self, output_path, source_path, check_states: dict):
        super().__init__()
        self.output_path = output_path
        self.source_path = source_path
        self.jpg_check, self.raw_check = check_states.values()

    def run(self):
        try:
            self.check_states_before_counting(self.jpg_check, self.raw_check)
            self.process_images()
            self.finished_work.emit()
        except Exception:
            self.error.emit(traceback.format_exc())
            self.finished_work.emit()

    def process_images(self):
        processed = 0
        for image in os.scandir(self.source_path):
            c_time = os.path.getmtime(image.path)
            creation_date = datetime.datetime.fromtimestamp(c_time).strftime(r"%Y-%m-%d")
            creation_date_folder = f"{self.output_path}/{creation_date}"
            jpg_folder = f"{creation_date_folder}/JPG"
            raw_folder = f"{creation_date_folder}/RAW"

            copied = False

            # --- Decide which folders to create ---
            if self.jpg_check == Qt.CheckState.Checked and self.raw_check == Qt.CheckState.Checked:
                self.make_directories([creation_date_folder, jpg_folder, raw_folder])
                copied = self.move_image(image, raw_folder=raw_folder, jpg_folder=jpg_folder)

            elif self.jpg_check == Qt.CheckState.Checked:
                self.make_directories([creation_date_folder, jpg_folder])
                copied = self.move_image(image, jpg_folder=jpg_folder)

            elif self.raw_check == Qt.CheckState.Checked:
                self.make_directories([creation_date_folder, raw_folder])
                copied = self.move_image(image, raw_folder=raw_folder)

            # Only count if something was copied
            if copied:
                processed += 1
                self.progress.emit(processed)

    def move_image(self, image: os.DirEntry, raw_folder: str = None, jpg_folder: str = None) -> bool:
        copied = False
        if raw_folder and image.name.lower().endswith(".arw"):
            shutil.copy(image.path, raw_folder)
            copied = True

        if jpg_folder and image.name.lower().endswith((".jpg", ".jpeg")):
            shutil.copy(image.path, jpg_folder)
            copied = True

        return copied

    def make_directories(self, paths: list):
        for path in paths:
            os.makedirs(path, exist_ok=True)

    def check_states_before_counting(self, jpg_check: Qt.CheckState, raw_check: Qt.CheckState):
        if jpg_check == Qt.CheckState.Checked and self.raw_check == Qt.CheckState.Checked:
            suffix = RAW_FILES + JPG_FILES
            self.count_files(suffix)
        elif jpg_check == Qt.CheckState.Checked:
            self.count_files(JPG_FILES)
        elif raw_check == Qt.CheckState.Checked:
            self.count_files(RAW_FILES)

    def count_files(self, suffix: set):
        with os.scandir(self.source_path) as entries:
            file_count = sum(1 for entry in entries if entry.is_file() and entry.name.lower().endswith(suffix))
        if file_count <= 0:
            self.error.emit("Nothing to import.")
            self.finished_work.emit()
        else:
            self.file_count.emit(file_count)
