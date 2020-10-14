# -*- coding: utf-8 -*-

import sys
import page
from PyQt5 import QtCore, QtGui, QtWidgets
from file_manipulation.pdf import pdf_processing as pp

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


def p_line_key(p_line):
    a = p_line._polygon
    min_a = 999999999
    for point in a:
        if point.y() < min_a:
            min_a = point.y()
    return min_a

class Ui_test:
    def setupUi(self, test):
        """ Creates layout of UI """
        test.setObjectName(_fromUtf8("test"))
        test.resize(1092, 589)
        self.horizontalLayout = QtWidgets.QHBoxLayout(test)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.label = ImageLabel()
        self.label.setObjectName(_fromUtf8("label_2"))
        self.horizontalLayout.addWidget(self.label)

        self.textBrowser = QtWidgets.QTextEdit(test)
        self.textBrowser.setObjectName(_fromUtf8("textBrowser"))
        self.textBrowser.copyAvailable.connect(self.get_char)
        self.horizontalLayout.addWidget(self.textBrowser)

        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))

        self.pushButton_2 = QtWidgets.QPushButton(test)
        self.pushButton_2.setObjectName(_fromUtf8("pushButton_2"))
        self.pushButton_2.clicked.connect(self.get_file)
        self.verticalLayout.addWidget(self.pushButton_2)

        self.pushButton_3 = QtWidgets.QPushButton(test)
        self.pushButton_3.setObjectName(_fromUtf8("pushButton_3"))
        self.verticalLayout.addWidget(self.pushButton_3)

        self.pushButton = QtWidgets.QPushButton(test)
        self.pushButton.setObjectName(_fromUtf8("pushButton"))
        self.verticalLayout.addWidget(self.pushButton)
        self.horizontalLayout.addLayout(self.verticalLayout)
        #self.pushButton.clicked.connect(self.get_char)

        self.pushButton_4 = QtWidgets.QPushButton(test)
        self.pushButton_4.setObjectName(_fromUtf8("pushButton_4"))
        self.pushButton_4.clicked.connect(self.previous_page)
        self.verticalLayout.addWidget(self.pushButton_4)

        self.pushButton_5 = QtWidgets.QPushButton(test)
        self.pushButton_5.setObjectName(_fromUtf8("pushButton_5"))
        self.pushButton_5.clicked.connect(self.next_page)
        self.verticalLayout.addWidget(self.pushButton_5)

        self.pushButton_6 = QtWidgets.QPushButton(test)
        self.pushButton_6.setObjectName(_fromUtf8("pushButton_6"))
        self.pushButton_6.clicked.connect(self.transcribe_polygons)
        self.verticalLayout.addWidget(self.pushButton_6)

        self.pushButton_7 = QtWidgets.QPushButton(test)
        self.pushButton_7.setObjectName(_fromUtf8("pushButton"))
        self.pushButton_7.clicked.connect(self.get_polygon)
        self.verticalLayout.addWidget(self.pushButton_7)

        self.retranslateUi(test)
        QtCore.QMetaObject.connectSlotsByName(test)

    def retranslateUi(self, test):
        """ Puts text on QWidgets """
        test.setWindowTitle(_translate("test", "test", None))
        self.label.setText(_translate("test", "                                               PDF Viewer                                                   ", None))
        self.pushButton_2.setText(_translate("test", "Import PDF", None))
        self.pushButton_3.setText(_translate("test", "Export PDF", None))
        self.pushButton.setText(_translate("test", "Editing Mode", None))
        self.pushButton_4.setText(_translate("test", "<- Previous Page", None))
        self.pushButton_5.setText(_translate("test", "Next Page ->", None))
        self.pushButton_6.setText(_translate("test", "Transcribe Polygons", None))
        self.pushButton_7.setText(_translate("test", "Line/Polygon Matching", None))

    def export_file(self):
        text = self.textBrowser.toPlainText()
        file = open('out.txt','w')
        file.write(text)

    def get_char(self):
        """ Outputs highlighted character in text box """
        self.textCursor = self.textBrowser.textCursor()
        if self.textCursor.hasSelection() == True:
            selected = self.textCursor.selectionStart()
            text = self.textBrowser.toPlainText()
            if selected <= len(text)-1:
                print(text[selected])

    def get_file(self):
        """ Gets the embedded jpg from a pdf """
        fname = QtWidgets.QFileDialog.getOpenFileName(test, 'Open file','c:\\\\',"Image files (*.jpg *.pdf)")
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

    def next_page(self):
        """ Next page button """
        if self.page < len(self.imgs) - 1:
            # save the text on text browser to the page object
            self.label._page._text = self.textBrowser.toPlainText()
            # change the page index and object
            self.page += 1
            self.label._page = self.pages[self.page]
            self.textBrowser.setText(self.label._page._text)
            self.label.update()

    def previous_page(self):
        """ Previous page button """
        if self.page > 0:
            self.label._page._text = self.textBrowser.toPlainText()
            self.page -= 1
            self.label._page = self.pages[self.page]
            self.textBrowser.setText(self.label._page._text)
            self.label.update()

    def transcribe_polygons(self):
        # sort polygons
        #poly_lines = self.pages[self.page]._page_lines[:]
        poly_lines = self.label._page._page_lines[:]
        poly_lines.sort(key=p_line_key)

        # Add dummy info to text boxes
        for p in poly_lines:
            p.set_transcription("(" + str(p._polygon[0].x()) + ", " + str(p._polygon[0].y()) + ")")
            self.textBrowser.append(p._transcription)

        # Remove polygons from image

    def get_polygon(self):
        self.textCursor = self.textBrowser.textCursor()
        if self.textCursor.hasSelection() == True:
            start = self.textCursor.selectionStart()
            end = self.textCursor.selectionEnd()
            text = self.textBrowser.toPlainText()
            selection = text[start:end]
            for line in self.pages[self.page]._page_lines:
                if line._transcription == selection:
                    self.selected_polygon = line.polygon

        else:
            pass

class ImageLabel(QtWidgets.QLabel):
    def __init__(self):
        """ Provides event support for the image label """
        # CITE: # https://doc.qt.io/qtforpython/PySide2/QtWidgets/QRubberBand.html
        super(ImageLabel, self).__init__()
        self._page = None
        self._lines = []
        self._start_of_line = []
        self._end_of_line = []
        self.setMouseTracking(True)

    def paintEvent(self, event):
        """ Paints a polygon on the pixmap after selection
            during selection of a polygon points the current line """
        painter = QtGui.QPainter(self)
        if self._page:
            painter.drawPixmap(self.rect(), self._page._pixmap)
            painter.setPen(QtCore.Qt.red)
            if self._start_of_line and self._end_of_line:
                painter.drawLine(self._start_of_line, self._end_of_line)
            for start, end in self._lines:
                painter.drawLine(start, end)
            for page_line in self._page._page_lines:
                poly = page_line._polygon
                painter.drawConvexPolygon(poly)

    def mousePressEvent(self, event):
        """ Collects points for the polygon and creates selection boxes """
        if self._start_of_line:
            self._lines.append((self._start_of_line, event.pos()))
        self._start_of_line = event.pos()
        self._page._polygon_points.append((event.x(),event.y()))
        self._page._polygon << event.pos()

    def mouseMoveEvent(self, event):
        """ updates the painter and lets it draw the line from
            the last clicked point to end """
        self._end_of_line = event.pos()
        self.update()


class MainWidget(QtWidgets.QWidget):
    def __init__(self):
        """ Calls the UI immediately and provides event support """
        super(MainWidget, self).__init__()
        self.ui = Ui_test()
        self.ui.setupUi(self)

    def keyPressEvent(self, event):
        """ Called when a key is pressed """
        if event.key() == QtCore.Qt.Key_Escape and len(self.ui.label._page._polygon_points) > 2:
            self.ui.label._page.selectPolygon()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    test = MainWidget()
    test.show()
    sys.exit(app.exec_())
