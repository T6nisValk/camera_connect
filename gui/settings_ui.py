# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'settingsChwWQn.ui'
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
from PySide6.QtWidgets import (QApplication, QCheckBox, QGridLayout, QSizePolicy,
    QWidget)

class Ui_Settings(object):
    def setupUi(self, Settings):
        if not Settings.objectName():
            Settings.setObjectName(u"Settings")
        Settings.resize(168, 232)
        self.gridLayout = QGridLayout(Settings)
        self.gridLayout.setObjectName(u"gridLayout")
        self.checkBox_2 = QCheckBox(Settings)
        self.checkBox_2.setObjectName(u"checkBox_2")

        self.gridLayout.addWidget(self.checkBox_2, 0, 0, 1, 1)

        self.checkBox = QCheckBox(Settings)
        self.checkBox.setObjectName(u"checkBox")

        self.gridLayout.addWidget(self.checkBox, 1, 0, 1, 1)

        self.checkBox_3 = QCheckBox(Settings)
        self.checkBox_3.setObjectName(u"checkBox_3")

        self.gridLayout.addWidget(self.checkBox_3, 2, 0, 1, 1)

        self.checkBox_4 = QCheckBox(Settings)
        self.checkBox_4.setObjectName(u"checkBox_4")

        self.gridLayout.addWidget(self.checkBox_4, 3, 0, 1, 1)

        self.checkBox_5 = QCheckBox(Settings)
        self.checkBox_5.setObjectName(u"checkBox_5")

        self.gridLayout.addWidget(self.checkBox_5, 4, 0, 1, 1)


        self.retranslateUi(Settings)

        QMetaObject.connectSlotsByName(Settings)
    # setupUi

    def retranslateUi(self, Settings):
        Settings.setWindowTitle(QCoreApplication.translate("Settings", u"Settings", None))
        self.checkBox_2.setText(QCoreApplication.translate("Settings", u"CheckBox", None))
        self.checkBox.setText(QCoreApplication.translate("Settings", u"CheckBox", None))
        self.checkBox_3.setText(QCoreApplication.translate("Settings", u"CheckBox", None))
        self.checkBox_4.setText(QCoreApplication.translate("Settings", u"CheckBox", None))
        self.checkBox_5.setText(QCoreApplication.translate("Settings", u"CheckBox", None))
    # retranslateUi

