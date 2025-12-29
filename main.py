from camera_connect import ImportPictures
from PySide6.QtWidgets import QApplication, QMainWindow
import sys


def main():
    app = QApplication(sys.argv)
    app_window = QMainWindow()
    app_window.main = ImportPictures(app_window)
    app_window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
