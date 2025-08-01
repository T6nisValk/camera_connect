# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'mainBahPGi.ui'
##
## Created by: Qt User Interface Compiler version 6.9.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QGridLayout, QLabel, QMainWindow,
    QPushButton, QSizePolicy, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(314, 172)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayout = QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.directory_lbl = QLabel(self.centralwidget)
        self.directory_lbl.setObjectName(u"directory_lbl")
        self.directory_lbl.setWordWrap(True)

        self.gridLayout.addWidget(self.directory_lbl, 1, 0, 1, 1)

        self.import_btn = QPushButton(self.centralwidget)
        self.import_btn.setObjectName(u"import_btn")

        self.gridLayout.addWidget(self.import_btn, 3, 0, 1, 1)

        self.set_dir_btn = QPushButton(self.centralwidget)
        self.set_dir_btn.setObjectName(u"set_dir_btn")

        self.gridLayout.addWidget(self.set_dir_btn, 2, 0, 1, 1)

        self.drive_info_lbl = QLabel(self.centralwidget)
        self.drive_info_lbl.setObjectName(u"drive_info_lbl")

        self.gridLayout.addWidget(self.drive_info_lbl, 0, 0, 1, 1)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.directory_lbl.setText(QCoreApplication.translate("MainWindow", u"DIRECTORY", None))
        self.import_btn.setText(QCoreApplication.translate("MainWindow", u"Import", None))
        self.set_dir_btn.setText(QCoreApplication.translate("MainWindow", u"Set Output Directory", None))
        self.drive_info_lbl.setText("")
    # retranslateUi

