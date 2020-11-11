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

class PopupMenu(QtWidgets.QWidget):
    def __init__(self, ui, test, layout):
        super(PopupMenu, self).__init__()
        self._ui = ui
        self._test = test
        self._verticalLayout = layout
        self._menu_open = False

        # Menu label
        self._menuLabel = MenuLabel(self)
        self._verticalLayout.addWidget(self._menuLabel)

        # Spacer item
        self._space = QtWidgets.QSpacerItem(10, 490)
        self._verticalLayout.addSpacerItem(self._space)

        # Page number layout
        self.pageNumberHLayout = QtWidgets.QHBoxLayout()
        self._verticalLayout.addLayout(self.pageNumberHLayout)

        # List of menu widgets
        self._widgets_list = []

        # Page number widgets
        self._h_layout = []
        self.pageNumberLabel = QtWidgets.QLabel("Page:")
        self.inputPageNumber = QtWidgets.QLineEdit()
        self.inputPageNumber.setAlignment(QtCore.Qt.AlignCenter)
        self.inputPageNumber.setValidator(QtGui.QIntValidator())
        self.inputPageNumber.editingFinished.connect(self._ui.jumpToPage)
        self.inputPageNumber.setReadOnly(True)
        self._h_layout.append(self.pageNumberLabel)
        self._h_layout.append(self.inputPageNumber)
        self._widgets_list.append(self._h_layout)

        # Buttons
        self.pushButton_2 = QtWidgets.QPushButton()
        self.pushButton_2.setObjectName(("pushButton_2"))
        self.pushButton_2.clicked.connect(self._ui.get_file)
        self._widgets_list.append(self.pushButton_2)

        self.pushButton_3 = QtWidgets.QPushButton()
        self.pushButton_3.setObjectName(("pushButton_3"))
        self._widgets_list.append(self.pushButton_3)

        self.pushButton_7 = QtWidgets.QPushButton()
        self.pushButton_7.setObjectName(("pushButton"))
        self.pushButton_7.clicked.connect(self._ui.turn_highlighting_on)
        self._widgets_list.append(self.pushButton_7)

        self.pushButton_8= QtWidgets.QPushButton()
        self.pushButton_8.setObjectName(("pushButton"))
        self.pushButton_8.clicked.connect(self._ui.turn_polygon_selection_on)
        self._widgets_list.append(self.pushButton_8)

        self.pushButton_6 = QtWidgets.QPushButton()
        self.pushButton_6.setObjectName(("pushButton_6"))
        self.pushButton_6.clicked.connect(self._ui.transcribe_all_polygons)
        self._widgets_list.append(self.pushButton_6)

        self.pushButton_9 = QtWidgets.QPushButton()
        self.pushButton_9.setObjectName(("pushButton_9"))
        self.pushButton_9.clicked.connect(self._ui.trainLines)
        self._widgets_list.append(self.pushButton_9)

        self.pushButton_4 = QtWidgets.QPushButton()
        self.pushButton_4.setObjectName(("pushButton_4"))
        self.pushButton_4.clicked.connect(self._ui.previous_page)
        self._widgets_list.append(self.pushButton_4)

        self.pushButton_5 = QtWidgets.QPushButton()
        self.pushButton_5.setObjectName(("pushButton_5"))
        self.pushButton_5.clicked.connect(self._ui.next_page)
        self._widgets_list.append(self.pushButton_5)

        # retranslate
        self.pushButton_2.setText("Import PDF")
        self.pushButton_3.setText("Export PDF")
        self.pushButton_7.setText("Highlighting Mode")
        self.pushButton_8.setText("Polygon Selection Mode")
        self.pushButton_6.setText("Transcribe All Polygons")
        self.pushButton_4.setText("<- Previous Page")
        self.pushButton_5.setText("Next Page ->")
        self.pushButton_9.setText("Create Training Data")

    def show(self):
        """ Open hamburger menu """
        self._menu_open = True

        # Change spacer size
        self._space.changeSize(10, 5)

        for i in range(len(self._widgets_list)):
            if isinstance(self._widgets_list[i], list): # page number layout
                for widget in self._widgets_list[i]:
                    self.pageNumberHLayout.addWidget(widget)
            else: # button
                self._verticalLayout.addWidget(self._widgets_list[i])

    def hide(self):
        """ Close hamburger menu """
        self._menu_open = False
        # delete widgets from page number layout
        for i in reversed(range(self.pageNumberHLayout.count())):
            self.pageNumberHLayout.itemAt(i).widget().setParent(None)
        # delete buttons
        for i in reversed(range(self._verticalLayout.count())):
            if i > 2:
                self._verticalLayout.itemAt(i).widget().setParent(None)
        # Spacer
        self._space.changeSize(10, 490)
