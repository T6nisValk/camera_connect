"""Program to import pictures from a camera and organize them into folders by capture date."""

from gui.ui_main import Ui_MainWindow
import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QMessageBox
from PySide6.QtCore import Signal, QThread, QObject
from PySide6.QtGui import QIcon
import wmi
import os
import shutil
import datetime

PICTURES_PATH = r"E:\DCIM"
OUTPUT = r"C:\Users\tnsva\Pictures\Raw"
ICON_PATH = r"assets\camera.ico"


class USBWorker(QObject):
    device_found = Signal(object)  # emits device info tuple or None

    def __init__(self):
        super().__init__()
        self._running = True

    def stop(self):
        self._running = False

    def run(self):
        c = wmi.WMI()
        previous_device = None
        device = None
        for disk in c.Win32_DiskDrive():
            if "USB" not in disk.PNPDeviceID:
                continue
            # Check for Sony camera
            if "Sony" in disk.Model:
                label = disk.Model
                # Find drive letter
                for partition in disk.associators("Win32_DiskDriveToDiskPartition"):
                    for logical_disk in partition.associators("Win32_LogicalDiskToPartition"):
                        letter = logical_disk.DeviceID
                        device = (letter, f"Sony Camera: {label}")
                        break
            else:
                for partition in disk.associators("Win32_DiskDriveToDiskPartition"):
                    for logical_disk in partition.associators("Win32_LogicalDiskToPartition"):
                        letter = logical_disk.DeviceID
                        label = logical_disk.VolumeName or "No Label"
                        device = (letter, label)
                        break
        self.device_found.emit(device)
        previous_device = device
        while self._running:
            device = None
            for disk in c.Win32_DiskDrive():
                if "USB" not in disk.PNPDeviceID:
                    continue
                if "Sony" in disk.Model:
                    label = disk.Model
                    for partition in disk.associators("Win32_DiskDriveToDiskPartition"):
                        for logical_disk in partition.associators("Win32_LogicalDiskToPartition"):
                            letter = logical_disk.DeviceID
                            device = (letter, f"Sony Camera: {label}")
                            break
                else:
                    for partition in disk.associators("Win32_DiskDriveToDiskPartition"):
                        for logical_disk in partition.associators("Win32_LogicalDiskToPartition"):
                            letter = logical_disk.DeviceID
                            label = logical_disk.VolumeName or "No Label"
                            device = (letter, label)
                            break
            if device != previous_device:
                self.device_found.emit(device)
                previous_device = device
            QThread.msleep(2000)


class ImportPictures(Ui_MainWindow):
    def __init__(self, window):
        self.window = window
        self.setupUi(self.window)

        self.window.setWindowTitle("Simple Importer")
        self.window.setWindowIcon(QIcon(self.get_absolute_path(ICON_PATH)))
        self.import_btn.clicked.connect(self.import_pictures)

        self.progress_bar.setMinimum(0)
        self.progress_bar.setMaximum(100)
        self.progress_bar.setValue(0)

        # Start USB flash drive listener in worker thread
        self._usb_thread = QThread()
        self._usb_worker = USBWorker()
        self._usb_worker.moveToThread(self._usb_thread)
        self._usb_worker.device_found.connect(self.on_device_found)

        self._usb_thread.started.connect(self._usb_worker.run)
        self._usb_thread.start()

    def on_device_found(self, device):
        if device:
            letter, label = device
            self._set_drive_text(f"Connected Drive: {letter} ({label})")
        else:
            self._set_drive_text("No USB drive connected")

    def import_pictures(self):
        if os.path.exists(PICTURES_PATH) & os.path.exists(OUTPUT):
            picture_files = []

            # Collect all picture file paths first
            for folder in os.scandir(PICTURES_PATH):
                for picture in os.scandir(folder.path):
                    if picture.is_file():
                        picture_files.append(picture.path)

            total = len(picture_files)
            if total == 0:
                self._show_info("Nothing to import.")
                self.progress_bar.setValue(0)
                return

            self.progress_bar.setMaximum(total)
            self.progress_bar.setValue(0)

            imported_count = 0
            for picture_path in picture_files:
                creation_date = datetime.datetime.fromtimestamp(os.path.getmtime(picture_path)).date()
                self._create_new_folder(creation_date)
                new_output = os.path.join(OUTPUT, str(creation_date))

                try:
                    shutil.move(picture_path, new_output)
                    imported_count += 1
                except Exception as e:
                    self._show_warning(f"Could not move {picture_path}:\n{e}")

                self.progress_bar.setValue(imported_count)
                QApplication.processEvents()  # Force UI to update

            self._show_info(f"{imported_count} pictures imported.")
        else:
            self._show_error("OUTPUT or PICTURE PATH Error.")

    # -- Helper Functions --
    def get_absolute_path(self, relative_path):
        """Get absolute path to resource, works for dev and for PyInstaller."""
        try:
            base_path = sys._MEIPASS
        except AttributeError:
            base_path = os.path.abspath(".")
        return os.path.join(base_path, relative_path)

    def _create_new_folder(self, date):
        if not os.path.exists(f"{OUTPUT}/{date}"):
            os.mkdir(os.path.join(OUTPUT, f"{date}"))

    def _set_drive_text(self, text):
        self.drive_info_lbl.setText(text)

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
