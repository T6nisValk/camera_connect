# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'mainLRQBWy.ui'
##
## Created by: Qt User Interface Compiler version 6.10.1
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
from PySide6.QtWidgets import (QApplication, QCheckBox, QGridLayout, QMainWindow,
    QProgressBar, QPushButton, QSizePolicy, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(336, 120)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setMinimumSize(QSize(336, 120))
        MainWindow.setMaximumSize(QSize(336, 120))
        MainWindow.setStyleSheet(u"QProgressBar {\n"
"	min-height: 15px;\n"
"	border : 1px solid rgb(0, 0, 0);\n"
"	border-radius: 6px;\n"
"	text-align: center;\n"
"	font-size: 12px;\n"
"	font-weight: 600;\n"
"	color: #FFFFFF;\n"
"	padding: 0;\n"
"}\n"
"QProgressBar::chunk{\n"
"	border-radius: 6px;\n"
"	margin: 0;\n"
"}\n"
"QProgressBar[finished=\"true\"]::chunk {\n"
"    background-color: #3caa3c;\n"
"}")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayout = QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.jpg_checkbox = QCheckBox(self.centralwidget)
        self.jpg_checkbox.setObjectName(u"jpg_checkbox")

        self.gridLayout.addWidget(self.jpg_checkbox, 1, 0, 1, 1)

        self.import_btn = QPushButton(self.centralwidget)
        self.import_btn.setObjectName(u"import_btn")

        self.gridLayout.addWidget(self.import_btn, 3, 2, 1, 1)

        self.new_output_btn = QPushButton(self.centralwidget)
        self.new_output_btn.setObjectName(u"new_output_btn")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.new_output_btn.sizePolicy().hasHeightForWidth())
        self.new_output_btn.setSizePolicy(sizePolicy1)

        self.gridLayout.addWidget(self.new_output_btn, 3, 3, 1, 1)

        self.raw_checkbox = QCheckBox(self.centralwidget)
        self.raw_checkbox.setObjectName(u"raw_checkbox")

        self.gridLayout.addWidget(self.raw_checkbox, 1, 1, 1, 1)

        self.import_and_delete_btn = QPushButton(self.centralwidget)
        self.import_and_delete_btn.setObjectName(u"import_and_delete_btn")

        self.gridLayout.addWidget(self.import_and_delete_btn, 3, 0, 1, 2)

        self.progress_bar = QProgressBar(self.centralwidget)
        self.progress_bar.setObjectName(u"progress_bar")
        self.progress_bar.setValue(0)

        self.gridLayout.addWidget(self.progress_bar, 0, 0, 1, 4)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.jpg_checkbox.setText(QCoreApplication.translate("MainWindow", u"JPEG", None))
        self.import_btn.setText(QCoreApplication.translate("MainWindow", u"Import", None))
        self.new_output_btn.setText(QCoreApplication.translate("MainWindow", u"New Output", None))
        self.raw_checkbox.setText(QCoreApplication.translate("MainWindow", u"RAW", None))
        self.import_and_delete_btn.setText(QCoreApplication.translate("MainWindow", u"Import and Delete", None))
    # retranslateUi

