# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'game.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(884, 552)
        self.btn_new_game = QtWidgets.QPushButton(Form)
        self.btn_new_game.setGeometry(QtCore.QRect(180, 460, 131, 51))
        self.btn_new_game.setObjectName("btn_new_game")
        self.btn_exit = QtWidgets.QPushButton(Form)
        self.btn_exit.setGeometry(QtCore.QRect(590, 460, 131, 51))
        self.btn_exit.setObjectName("btn_exit")
        self.label = QtWidgets.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(170, 0, 181, 101))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(25)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(Form)
        self.label_2.setGeometry(QtCore.QRect(610, 30, 101, 51))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(25)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Морской бой"))
        self.btn_new_game.setText(_translate("Form", "Новая игра"))
        self.btn_exit.setText(_translate("Form", "Выход"))
        self.label.setText(_translate("Form", "Компьютер"))
        self.label_2.setText(_translate("Form", "Игрок"))
