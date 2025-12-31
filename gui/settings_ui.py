# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'settingslPQjKD.ui'
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
from PySide6.QtWidgets import (QApplication, QCheckBox, QGridLayout, QGroupBox,
    QLabel, QPushButton, QSizePolicy, QSpacerItem,
    QWidget)

class Ui_Settings(object):
    def setupUi(self, Settings):
        if not Settings.objectName():
            Settings.setObjectName(u"Settings")
        Settings.resize(320, 443)
        self.gridLayout = QGridLayout(Settings)
        self.gridLayout.setObjectName(u"gridLayout")
        self.groupBox_2 = QGroupBox(Settings)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.gridLayout_2 = QGridLayout(self.groupBox_2)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.browseOutputButton = QPushButton(self.groupBox_2)
        self.browseOutputButton.setObjectName(u"browseOutputButton")

        self.gridLayout_2.addWidget(self.browseOutputButton, 0, 0, 1, 1)

        self.outputPathLabel = QLabel(self.groupBox_2)
        self.outputPathLabel.setObjectName(u"outputPathLabel")
        self.outputPathLabel.setWordWrap(True)

        self.gridLayout_2.addWidget(self.outputPathLabel, 1, 0, 1, 1)


        self.gridLayout.addWidget(self.groupBox_2, 1, 0, 1, 3)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer, 3, 0, 1, 1)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer_2, 3, 2, 1, 1)

        self.groupBox = QGroupBox(Settings)
        self.groupBox.setObjectName(u"groupBox")
        self.gridLayout_3 = QGridLayout(self.groupBox)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.jpgCheckBox = QCheckBox(self.groupBox)
        self.jpgCheckBox.setObjectName(u"jpgCheckBox")

        self.gridLayout_3.addWidget(self.jpgCheckBox, 0, 0, 1, 1)

        self.rawCheckBox = QCheckBox(self.groupBox)
        self.rawCheckBox.setObjectName(u"rawCheckBox")

        self.gridLayout_3.addWidget(self.rawCheckBox, 1, 0, 1, 1)


        self.gridLayout.addWidget(self.groupBox, 0, 0, 1, 1)

        self.saveButton = QPushButton(Settings)
        self.saveButton.setObjectName(u"saveButton")

        self.gridLayout.addWidget(self.saveButton, 3, 1, 1, 1)

        self.groupBox_3 = QGroupBox(Settings)
        self.groupBox_3.setObjectName(u"groupBox_3")
        self.gridLayout_4 = QGridLayout(self.groupBox_3)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.browseSourceButton = QPushButton(self.groupBox_3)
        self.browseSourceButton.setObjectName(u"browseSourceButton")

        self.gridLayout_4.addWidget(self.browseSourceButton, 0, 0, 1, 1)

        self.sourcePathLabel = QLabel(self.groupBox_3)
        self.sourcePathLabel.setObjectName(u"sourcePathLabel")
        self.sourcePathLabel.setWordWrap(True)

        self.gridLayout_4.addWidget(self.sourcePathLabel, 1, 0, 1, 1)


        self.gridLayout.addWidget(self.groupBox_3, 2, 0, 1, 3)


        self.retranslateUi(Settings)

        QMetaObject.connectSlotsByName(Settings)
    # setupUi

    def retranslateUi(self, Settings):
        Settings.setWindowTitle(QCoreApplication.translate("Settings", u"Settings", None))
        self.groupBox_2.setTitle(QCoreApplication.translate("Settings", u"Output Path Selection", None))
        self.browseOutputButton.setText(QCoreApplication.translate("Settings", u"Browse", None))
        self.outputPathLabel.setText(QCoreApplication.translate("Settings", u"Current Path", None))
        self.groupBox.setTitle(QCoreApplication.translate("Settings", u"Import File Type Selection", None))
        self.jpgCheckBox.setText(QCoreApplication.translate("Settings", u"JPG", None))
        self.rawCheckBox.setText(QCoreApplication.translate("Settings", u"RAW", None))
        self.saveButton.setText(QCoreApplication.translate("Settings", u"Save", None))
        self.groupBox_3.setTitle(QCoreApplication.translate("Settings", u"Source Path Selection", None))
        self.browseSourceButton.setText(QCoreApplication.translate("Settings", u"Browse", None))
        self.sourcePathLabel.setText(QCoreApplication.translate("Settings", u"Current Path", None))
    # retranslateUi

