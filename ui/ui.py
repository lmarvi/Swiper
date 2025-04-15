# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'PermutadorKlgeyH.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *



class Ui_MainWindow(object):
    ############ UI para 1080p ################
    def setupUi1080(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1275, 875)
        MainWindow.setMinimumSize(QSize(1275, 875))
        MainWindow.setMaximumSize(QSize(1275, 875))
        font = QFont()
        font.setFamily(u"Microsoft Sans Serif")
        font.setPointSize(10)
        MainWindow.setFont(font)
        icon = QIcon()
        icon.addFile(u"img/Logo.png", QSize(), QIcon.Normal, QIcon.Off)
        MainWindow.setWindowIcon(icon)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayoutWidget = QWidget(self.centralwidget)
        self.verticalLayoutWidget.setObjectName(u"verticalLayoutWidget")
        self.verticalLayoutWidget.setGeometry(QRect(20, 20, 261, 61))
        self.verticalLayoutBestileLogo = QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayoutBestileLogo.setObjectName(u"verticalLayoutBestileLogo")
        self.verticalLayoutBestileLogo.setContentsMargins(0, 0, 0, 0)
        self.frameLogo = QFrame(self.verticalLayoutWidget)
        self.frameLogo.setObjectName(u"frameLogo")
        self.frameLogo.setFrameShape(QFrame.NoFrame)
        self.logobestile = QLabel(self.frameLogo)
        self.logobestile.setObjectName(u"logobestile")
        self.logobestile.setGeometry(QRect(10, 14, 241, 31))
        self.logobestile.setPixmap(QPixmap(u"img/Logo_Bestile_sin_ceramicas_negro.png"))
        self.logobestile.setScaledContents(True)

        self.verticalLayoutBestileLogo.addWidget(self.frameLogo)

        self.verticalLayoutWidget_2 = QWidget(self.centralwidget)
        self.verticalLayoutWidget_2.setObjectName(u"verticalLayoutWidget_2")
        self.verticalLayoutWidget_2.setGeometry(QRect(0, 140, 2061, 51))
        self.verticalLayoutEdicionEsquemas = QVBoxLayout(self.verticalLayoutWidget_2)
        self.verticalLayoutEdicionEsquemas.setSpacing(6)
        self.verticalLayoutEdicionEsquemas.setObjectName(u"verticalLayoutEdicionEsquemas")
        self.verticalLayoutEdicionEsquemas.setContentsMargins(0, 0, 0, 0)
        self.frame = QFrame(self.verticalLayoutWidget_2)
        self.frame.setObjectName(u"frame")
        self.frame.setStyleSheet(u"QFrame{\n"
                                "border-style: solid;\n"
                                "border-width: 1px;\n"
                                "border-color: rgb(250, 250, 250);\n"
                                "background-color: rgb(250,250,250);\n"
                                "color: rgb(245, 245, 245);\n"
                                "}\n"
                                "\n"
                                "")
        self.frame.setFrameShape(QFrame.NoFrame)
        self.bt_add = QPushButton(self.frame)
        self.bt_add.setObjectName(u"bt_add")
        self.bt_add.setGeometry(QRect(210, 10, 181, 31))
        self.bt_add.setFont(font)
        self.bt_del = QPushButton(self.frame)
        self.bt_del.setObjectName(u"bt_del")
        self.bt_del.setGeometry(QRect(550, 10, 181, 31))
        self.bt_del.setFont(font)
        self.bt_edit = QPushButton(self.frame)
        self.bt_edit.setObjectName(u"bt_edit")
        self.bt_edit.setGeometry(QRect(880, 10, 181, 31))
        self.bt_edit.setFont(font)

        self.verticalLayoutEdicionEsquemas.addWidget(self.frame)

        self.verticalLayoutWidget_3 = QWidget(self.centralwidget)
        self.verticalLayoutWidget_3.setObjectName(u"verticalLayoutWidget_3")
        self.verticalLayoutWidget_3.setGeometry(QRect(380, 20, 521, 61))
        self.verticalLayoutTitulo = QVBoxLayout(self.verticalLayoutWidget_3)
        self.verticalLayoutTitulo.setObjectName(u"verticalLayoutTitulo")
        self.verticalLayoutTitulo.setContentsMargins(0, 0, 0, 0)
        self.frame_4 = QFrame(self.verticalLayoutWidget_3)
        self.frame_4.setObjectName(u"frame_4")
        self.frame_4.setStyleSheet(u"QFrame {\n"
                                "border -style: solid;\n"
                                "background-color: rgb(250, 250, 250);\n"
                                "border-radius: 10px;\n"
                                "\n"
                                "}")
        self.frame_4.setFrameShape(QFrame.NoFrame)
        self.et_titulo = QLabel(self.frame_4)
        self.et_titulo.setObjectName(u"et_titulo")
        self.et_titulo.setGeometry(QRect(90, 10, 411, 41))
        font1 = QFont()
        font1.setFamily(u"Cambria")
        font1.setPointSize(24)
        font1.setBold(True)
        font1.setItalic(False)
        self.et_titulo.setFont(font1)
        self.logoApp = QLabel(self.frame_4)
        self.logoApp.setObjectName(u"logoApp")
        self.logoApp.setGeometry(QRect(30, 15, 31, 31))
        self.logoApp.setPixmap(QPixmap(u"img/Logo.png"))
        self.logoApp.setScaledContents(True)

        self.verticalLayoutTitulo.addWidget(self.frame_4)

        self.verticalLayoutWidget_4 = QWidget(self.centralwidget)
        self.verticalLayoutWidget_4.setObjectName(u"verticalLayoutWidget_4")
        self.verticalLayoutWidget_4.setGeometry(QRect(20, 220, 611, 631))
        self.verticalLayoutEsquemas = QVBoxLayout(self.verticalLayoutWidget_4)
        self.verticalLayoutEsquemas.setObjectName(u"verticalLayoutEsquemas")
        self.verticalLayoutEsquemas.setContentsMargins(0, 0, 0, 0)
        self.frame_2 = QFrame(self.verticalLayoutWidget_4)
        self.frame_2.setObjectName(u"frame_2")
        self.frame_2.setFrameShape(QFrame.NoFrame)
        self.label = QLabel(self.frame_2)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(270, 20, 101, 16))
        self.list_schemes = QListView(self.frame_2)
        self.list_schemes.setObjectName(u"list_schemes")
        self.list_schemes.setGeometry(QRect(40, 50, 531, 551))
        self.list_schemes.setFrameShape(QFrame.Panel)

        self.verticalLayoutEsquemas.addWidget(self.frame_2)

        self.verticalLayoutWidget_5 = QWidget(self.centralwidget)
        self.verticalLayoutWidget_5.setObjectName(u"verticalLayoutWidget_5")
        self.verticalLayoutWidget_5.setGeometry(QRect(660, 220, 591, 631))
        self.verticalLayoutProcesado = QVBoxLayout(self.verticalLayoutWidget_5)
        self.verticalLayoutProcesado.setObjectName(u"verticalLayoutProcesado")
        self.verticalLayoutProcesado.setContentsMargins(0, 0, 0, 0)
        self.frame_3 = QFrame(self.verticalLayoutWidget_5)
        self.frame_3.setObjectName(u"frame_3")
        self.frame_3.setFrameShape(QFrame.NoFrame)
        self.label_2 = QLabel(self.frame_3)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(280, 20, 121, 16))
        self.bt_select = QPushButton(self.frame_3)
        self.bt_select.setObjectName(u"bt_select")
        self.bt_select.setGeometry(QRect(40, 80, 201, 31))
        self.bt_select.setFont(font)
        self.bt_output = QPushButton(self.frame_3)
        self.bt_output.setObjectName(u"bt_output")
        self.bt_output.setGeometry(QRect(40, 480, 201, 31))
        self.label_3 = QLabel(self.frame_3)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setGeometry(QRect(40, 50, 71, 16))
        self.label_4 = QLabel(self.frame_3)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setGeometry(QRect(40, 450, 71, 16))
        self.bt_proc = QPushButton(self.frame_3)
        self.bt_proc.setObjectName(u"bt_proc")
        self.bt_proc.setGeometry(QRect(250, 580, 121, 31))
        self.caja_ruta = QLineEdit(self.frame_3)
        self.caja_ruta.setObjectName(u"caja_ruta")
        self.caja_ruta.setEnabled(False)
        self.caja_ruta.setGeometry(QRect(40, 530, 851, 31))
        self.list_designs = QListView(self.frame_3)
        self.list_designs.setObjectName(u"list_designs")
        self.list_designs.setGeometry(QRect(40, 120, 511, 311))
        self.list_designs.setFrameShape(QFrame.Panel)
        self.bt_delDesigns = QPushButton(self.frame_3)
        self.bt_delDesigns.setObjectName(u"bt_delDesigns")
        self.bt_delDesigns.setGeometry(QRect(310, 80, 201, 31))
        self.bt_delDesigns.setFont(font)

        self.verticalLayoutProcesado.addWidget(self.frame_3)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Permutador de Canales", None))
        self.logobestile.setText("")
        self.bt_add.setText(QCoreApplication.translate("MainWindow", u"Añadir esquema", None))
        self.bt_del.setText(QCoreApplication.translate("MainWindow", u"Eliminar esquema", None))
        self.bt_edit.setText(QCoreApplication.translate("MainWindow", u"Editar esquema", None))
        self.et_titulo.setText(QCoreApplication.translate("MainWindow", u"PERMUTADOR DE CANALES", None))
        self.logoApp.setText("")
        self.label.setText(QCoreApplication.translate("MainWindow", u"Esquemas:", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"Procesado:", None))
        self.bt_select.setText(QCoreApplication.translate("MainWindow", u"Seleccionar archivos", None))
        self.bt_output.setText(QCoreApplication.translate("MainWindow", u"Seleccionar carpeta", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"Entrada:", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"Salida:", None))
        self.bt_proc.setText(QCoreApplication.translate("MainWindow", u"Procesar", None))
        self.bt_delDesigns.setText(QCoreApplication.translate("MainWindow", u"Eliminar archivos", None))
    # retranslateUi


    ############ UI para 4k ################

    def setupUi4k(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(2040, 1400)
        MainWindow.setMinimumSize(QSize(2040, 1400))
        MainWindow.setMaximumSize(QSize(2040, 1400))
        font = QFont()
        font.setFamily(u"Microsoft Sans Serif")
        font.setPointSize(10)
        MainWindow.setFont(font)
        icon = QIcon()
        icon.addFile(u"img/Logo.png", QSize(), QIcon.Normal, QIcon.Off)
        MainWindow.setWindowIcon(icon)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayoutWidget = QWidget(self.centralwidget)
        self.verticalLayoutWidget.setObjectName(u"verticalLayoutWidget")
        self.verticalLayoutWidget.setGeometry(QRect(20, 20, 401, 71))
        self.verticalLayoutBestileLogo = QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayoutBestileLogo.setObjectName(u"verticalLayoutBestileLogo")
        self.verticalLayoutBestileLogo.setContentsMargins(0, 0, 0, 0)
        self.frameLogo = QFrame(self.verticalLayoutWidget)
        self.frameLogo.setObjectName(u"frameLogo")
        self.frameLogo.setFrameShape(QFrame.NoFrame)
        self.logobestile = QLabel(self.frameLogo)
        self.logobestile.setObjectName(u"logobestile")
        self.logobestile.setGeometry(QRect(10, 9, 361, 51))
        self.logobestile.setPixmap(QPixmap(u"img/Logo_Bestile_sin_ceramicas_negro.png"))
        self.logobestile.setScaledContents(True)

        self.verticalLayoutBestileLogo.addWidget(self.frameLogo)

        self.verticalLayoutWidget_2 = QWidget(self.centralwidget)
        self.verticalLayoutWidget_2.setObjectName(u"verticalLayoutWidget_2")
        self.verticalLayoutWidget_2.setGeometry(QRect(0, 140, 2061, 51))
        self.verticalLayoutEdicionEsquemas = QVBoxLayout(self.verticalLayoutWidget_2)
        self.verticalLayoutEdicionEsquemas.setObjectName(u"verticalLayoutEdicionEsquemas")
        self.verticalLayoutEdicionEsquemas.setContentsMargins(0, 0, 0, 0)
        self.frame = QFrame(self.verticalLayoutWidget_2)
        self.frame.setObjectName(u"frame")
        self.frame.setStyleSheet(u"QFrame{\n"
                                "border-style: solid;\n"
                                "border-width: 1px;\n"
                                "border-color: rgb(250, 250, 250);\n"
                                "background-color: rgb(250,250,250);\n"
                                "color: rgb(245, 245, 245);\n"
                                "}\n"
                                "\n"
                                "")
        self.frame.setFrameShape(QFrame.NoFrame)
        self.bt_add = QPushButton(self.frame)
        self.bt_add.setObjectName(u"bt_add")
        self.bt_add.setGeometry(QRect(540, 10, 181, 31))
        self.bt_add.setFont(font)
        self.bt_del = QPushButton(self.frame)
        self.bt_del.setObjectName(u"bt_del")
        self.bt_del.setGeometry(QRect(950, 10, 181, 31))
        self.bt_del.setFont(font)
        self.bt_edit = QPushButton(self.frame)
        self.bt_edit.setObjectName(u"bt_edit")
        self.bt_edit.setGeometry(QRect(1350, 10, 181, 31))
        self.bt_edit.setFont(font)

        self.verticalLayoutEdicionEsquemas.addWidget(self.frame)

        self.verticalLayoutWidget_3 = QWidget(self.centralwidget)
        self.verticalLayoutWidget_3.setObjectName(u"verticalLayoutWidget_3")
        self.verticalLayoutWidget_3.setGeometry(QRect(670, 20, 721, 71))
        self.verticalLayoutTitulo = QVBoxLayout(self.verticalLayoutWidget_3)
        self.verticalLayoutTitulo.setObjectName(u"verticalLayoutTitulo")
        self.verticalLayoutTitulo.setContentsMargins(0, 0, 0, 0)
        self.frame_4 = QFrame(self.verticalLayoutWidget_3)
        self.frame_4.setObjectName(u"frame_4")
        self.frame_4.setStyleSheet(u"QFrame {\n"
                                "border -style: solid;\n"
                                "background-color: rgb(250, 250, 250);\n"
                                "border-radius: 10px;\n"
                                "\n"
                                "}")
        self.frame_4.setFrameShape(QFrame.NoFrame)
        self.et_titulo = QLabel(self.frame_4)
        self.et_titulo.setObjectName(u"et_titulo")
        self.et_titulo.setGeometry(QRect(90, 10, 641, 51))
        font1 = QFont()
        font1.setFamily(u"Cambria")
        font1.setPointSize(24)
        font1.setBold(True)
        font1.setItalic(False)
        font1.setWeight(75)
        self.et_titulo.setFont(font1)
        self.logoApp = QLabel(self.frame_4)
        self.logoApp.setObjectName(u"logoApp")
        self.logoApp.setGeometry(QRect(30, 20, 31, 31))
        self.logoApp.setPixmap(QPixmap(u"img/Logo.png"))
        self.logoApp.setScaledContents(True)

        self.verticalLayoutTitulo.addWidget(self.frame_4)

        self.verticalLayoutWidget_4 = QWidget(self.centralwidget)
        self.verticalLayoutWidget_4.setObjectName(u"verticalLayoutWidget_4")
        self.verticalLayoutWidget_4.setGeometry(QRect(20, 220, 981, 1161))
        self.verticalLayoutEsquemas = QVBoxLayout(self.verticalLayoutWidget_4)
        self.verticalLayoutEsquemas.setObjectName(u"verticalLayoutEsquemas")
        self.verticalLayoutEsquemas.setContentsMargins(0, 0, 0, 0)
        self.frame_2 = QFrame(self.verticalLayoutWidget_4)
        self.frame_2.setObjectName(u"frame_2")
        self.frame_2.setFrameShape(QFrame.NoFrame)
        self.label = QLabel(self.frame_2)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(460, 20, 101, 16))
        self.list_schemes = QListView(self.frame_2)
        self.list_schemes.setObjectName(u"list_schemes")
        self.list_schemes.setGeometry(QRect(110, 50, 761, 1051))
        self.list_schemes.setFrameShape(QFrame.Panel)

        self.verticalLayoutEsquemas.addWidget(self.frame_2)

        self.verticalLayoutWidget_5 = QWidget(self.centralwidget)
        self.verticalLayoutWidget_5.setObjectName(u"verticalLayoutWidget_5")
        self.verticalLayoutWidget_5.setGeometry(QRect(1060, 220, 951, 1161))
        self.verticalLayoutProcesado = QVBoxLayout(self.verticalLayoutWidget_5)
        self.verticalLayoutProcesado.setObjectName(u"verticalLayoutProcesado")
        self.verticalLayoutProcesado.setContentsMargins(0, 0, 0, 0)
        self.frame_3 = QFrame(self.verticalLayoutWidget_5)
        self.frame_3.setObjectName(u"frame_3")
        self.frame_3.setFrameShape(QFrame.NoFrame)
        self.label_2 = QLabel(self.frame_3)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(450, 20, 121, 16))
        self.bt_select = QPushButton(self.frame_3)
        self.bt_select.setObjectName(u"bt_select")
        self.bt_select.setGeometry(QRect(50, 80, 201, 31))
        self.bt_select.setFont(font)
        self.bt_output = QPushButton(self.frame_3)
        self.bt_output.setObjectName(u"bt_output")
        self.bt_output.setGeometry(QRect(50, 900, 201, 31))
        self.label_3 = QLabel(self.frame_3)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setGeometry(QRect(50, 50, 71, 16))
        self.label_4 = QLabel(self.frame_3)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setGeometry(QRect(50, 870, 71, 16))
        self.bt_proc = QPushButton(self.frame_3)
        self.bt_proc.setObjectName(u"bt_proc")
        self.bt_proc.setGeometry(QRect(430, 1040, 121, 31))
        self.caja_ruta = QLineEdit(self.frame_3)
        self.caja_ruta.setObjectName(u"caja_ruta")
        self.caja_ruta.setEnabled(False)
        self.caja_ruta.setGeometry(QRect(50, 950, 851, 31))
        self.list_designs = QListView(self.frame_3)
        self.list_designs.setObjectName(u"list_designs")
        self.list_designs.setGeometry(QRect(50, 140, 851, 681))
        self.list_designs.setFrameShape(QFrame.Panel)
        self.bt_delDesigns = QPushButton(self.frame_3)
        self.bt_delDesigns.setObjectName(u"bt_delDesigns")
        self.bt_delDesigns.setGeometry(QRect(310, 80, 201, 31))
        self.bt_delDesigns.setFont(font)

        self.verticalLayoutProcesado.addWidget(self.frame_3)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi
    