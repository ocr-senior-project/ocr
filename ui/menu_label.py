import numpy
import os
import glob
import sys
import math
from ui.page import *
from ui.popup_menu import *
from ui.menu_label import *
from ui.image_label import *
from PyQt5 import QtCore, QtGui, QtWidgets

mode = ""

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtWidgets.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtWidgets.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtWidgets.QApplication.translate(context, text, disambig)

class MenuLabel(QtWidgets.QLabel):
    def __init__(self, menu):
        """ Provides event support for the menu label """
        super(MenuLabel, self).__init__()
        self._menu = menu
        self.setText("≡")
        self.setFont(QtGui.QFont("Times", 30, QtGui.QFont.Bold))
        self.setFixedSize(30, 30)

    def mousePressEvent(self, event):
        if self._menu._menu_open:
            self._menu.hide()
        else:
            self._menu.show()
