from PySide6.QtCore import Signal, QObject
import shutil
import os
import datetime
import traceback


class IterateImages(QObject):
    finished_work = Signal()
    progress = Signal(int)
    file_count = Signal(int)
    error = Signal(str)

    def __init__(self, output_path, source_path):
        super().__init__()
        self.output_path = output_path
        self.source_path = source_path

    def run(self):
        try:
            self.count_files()
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
            self.make_directories([creation_date_folder, jpg_folder, raw_folder])
            self.move_image(image, raw_folder, jpg_folder)
            processed += 1
            self.progress.emit(processed)

    def move_image(self, image: os.DirEntry, raw_folder: os.path, jpg_folder: os.path):
        if image.name.lower().endswith(("jpg", "jpeg")):
            shutil.copy(image.path, jpg_folder)
        elif image.name.lower().endswith("arw"):
            shutil.copy(image.path, raw_folder)

    def make_directories(self, paths: list):
        for path in paths:
            os.makedirs(path, exist_ok=True)

    def count_files(self):
        with os.scandir(self.source_path) as entries:
            file_count = sum(1 for entry in entries if entry.is_file())
        self.file_count.emit(file_count)
