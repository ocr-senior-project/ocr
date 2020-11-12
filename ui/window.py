# -*- coding: utf-8 -*-

import sys
import math
import ui.page as page
from ui.popup_menu import *
from ui.menu_label import *
from ui.image_label import *
from file_manipulation.pdf import pdf_processing as pp
from PyQt5 import QtCore, QtGui, QtWidgets

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

mode = "polygon_selection"

class Ui_test:
    def setupUi(self, test):
        """ Creates layout of UI """
        test.setObjectName(_fromUtf8("test"))
        test.resize(1092, 589)
        self.mainWindow = test

        # Horizontal layout
        self.horizontalLayout = QtWidgets.QHBoxLayout(test)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))

        # Hamburger menu layout
        self.menuVLayout = QtWidgets.QVBoxLayout()
        self.horizontalLayout.addLayout(self.menuVLayout, 2)
        self.popupMenu = PopupMenu(self, test, self.menuVLayout)

        # Image label
        self.label = ImageLabel(self)
        self.label.setObjectName(_fromUtf8("label_2"))
        self.horizontalLayout.addWidget(self.label, stretch=5)

        # Text box
        self.textBrowser = QtWidgets.QTextEdit(test)
        self.textBrowser.setObjectName(_fromUtf8("textBrowser"))
        self.textBrowser.cursorPositionChanged.connect(self.highlight_line)
        self.highlighted_cursor = None
        self.horizontalLayout.addWidget(self.textBrowser, stretch=5)

        # store the filename
        self.fname = None

        self.retranslateUi(test)
        QtCore.QMetaObject.connectSlotsByName(test)

    def retranslateUi(self, test):
        """ Puts text on QWidgets """
        test.setWindowTitle(_translate("test", "test", None))
        self.label.setText(_translate("test", "                                               PDF Viewer                                                   ", None))

    def export_file(self):
        text = self.textBrowser.toPlainText()
        file = open('out.txt','w')
        file.write(text)

    def get_file(self):
        """ Gets the embedded jpg from a pdf """

        fname = QtWidgets.QFileDialog.getOpenFileName(self.mainWindow, 'Open file','c:\\\\',"Image files (*.jpg *.pdf)")

        # Return if no file name is given
        if not fname[0]:
            return

        # Initialize a page index and a list of page objects
        self.page = 0
        self.pages = []

        # Returns a list of all of the pixmaps of the pdf
        self.imgs = pp.get_pdf_contents(fname[self.page])

        # Make the appropriate number of pages and assign them pixmaps
        for pixmap in self.imgs:
            self.pages.append(page.Page(self.label))
            self.pages[-1]._pixmap = pixmap

        self.label._page = self.pages[self.page]
        self.label.update()

        # Initialize page number layout
        self.initializePageNum()

    def initializePageNum(self):
        self.updatePageNum()
        self.popupMenu.inputPageNumber.setReadOnly(False)
        self.popupMenu.pageNumberLabel.setText(f"Page out of {len(self.imgs)}:")

    def updatePage(self):
        self.label._page = self.pages[self.page]
        self.textBrowser.setText(self.label._page._text)
        self.label.update()
        self.updatePageNum()

    def updatePageNum(self):
        self.popupMenu.inputPageNumber.setText(str(self.page + 1))

    def next_page(self):
        """ Next page button """
        if self.page < len(self.imgs) - 1:
            # save the text on text browser to the page object
            self.label._page._text = self.textBrowser.toPlainText()

            # change the page index and object
            self.page += 1
            self.updatePage()

    def previous_page(self):
        """ Previous page button """
        if self.page > 0:
            self.label._page._text = self.textBrowser.toPlainText()
            self.page -= 1
            self.updatePage()

    def trainLines(self):
        if self.label._page:
            self.label._page.trainLines()

    def jumpToPage(self):
        pageNumber = int(self.popupMenu.inputPageNumber.text()) - 1
        if pageNumber < 0:
            pageNumber  = 0
        elif pageNumber >= len(self.imgs):
            pageNumber = len(self.imgs) - 1

        # save the text on text browser to the page object
        self.label._page._text = self.textBrowser.toPlainText()

        # change the page index and object
        self.page = pageNumber
        self.updatePage()

    def turn_highlighting_on(self):
        global mode
        mode = "highlighting"

    def turn_polygon_selection_on(self):
        global mode
        mode = "polygon_selection"
        self.label._page._polygon = QtGui.QPolygon()
        self.label._page._polygon_points = []

    def add_transcriptions(self):
        """ Prints transcriptions onto the text box """
        self.textBrowser.clear()
        poly_lines = self.label._page._page_lines
        for p in poly_lines:
            if p._transcription:
                self.textBrowser.append(p._transcription)

    def transcribe_selected_polygon(self):
        """ Transcribes one polygon """
        p = self.label._page._selected_polygon

        transcript = self.label._page.transcribePolygon(p._image_name)
        self.label._page._selected_polygon.set_transcription(transcript)

        self.add_transcriptions()

    def transcribe_all_polygons(self):
        """ Transcribes all polygons """
        # Add dummy info to text boxes
        for p in self.label._page._page_lines:
            transcript = self.label._page.transcribePolygon(p._image_name)
            p.set_transcription(transcript)

        self.add_transcriptions()

    def highlight_line(self):
        global mode
        if mode == "highlighting":
            new_cursor_position = self.textBrowser.textCursor()
            fmt = QtGui.QTextBlockFormat()

            # clear prevosly highlighted block, if any
            if self.highlighted_cursor:
                self.textCursor = self.highlighted_cursor
                fmt.setBackground(QtGui.QColor(0, 0, 0, 255))
                self.textCursor.setBlockFormat(fmt)

            # highlight block cursor is currently on
            self.textCursor = new_cursor_position
            self.highlighted_cursor = self.textCursor
            fmt.setBackground(QtGui.QColor("yellow"))
            self.textCursor.setBlockFormat(fmt)

            # highlight polygon
            index = self.textCursor.blockNumber()
            for item in self.label._page._page_lines:
                if item._block_number == index:
                    self.label._page._polygon = item._polygon
                    self.label.update()
