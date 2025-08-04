"""Program to import pictures from a camera and organize them into folders by capture date."""

from gui.ui_main import Ui_MainWindow
import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QMessageBox, QFileDialog
from PySide6.QtCore import Signal, QThread, QObject
import wmi

camera_path = r"E:\DCIM"
output = r"C:\Users\tnsva\Pictures\Raw"


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

        self.window.setWindowTitle("Import Pictures")

        self.set_dir_btn.clicked.connect(self.set_directory)
        self.import_btn.clicked.connect(self.import_pictures)

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
        self._show_info("Nothing here yet.")

    def set_directory(self):
        file_location = QFileDialog.getExistingDirectory(caption="Choose dir")
        self._set_label_text(f"{file_location}")

    # -- Helper Functions --
    def _set_drive_text(self, text):
        self.drive_info_lbl.setText(text)

    def _set_label_text(self, text):
        self.directory_lbl.setText(text)

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
