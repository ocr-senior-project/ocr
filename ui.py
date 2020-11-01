# -*- coding: utf-8 -*-

import sys
import page
import math
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

mode = "polygon_selection"

class Ui_test:
    def setupUi(self, test):
        """ Creates layout of UI """
        test.setObjectName(_fromUtf8("test"))
        test.resize(1092, 589)
        self.mainWindow = test

        self.horizontalLayout = QtWidgets.QHBoxLayout(test)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))

        self.label = ImageLabel(self)
        self.label.setObjectName(_fromUtf8("label_2"))
        self.horizontalLayout.addWidget(self.label, stretch=5)

        self.textBrowser = QtWidgets.QTextEdit(test)
        self.textBrowser.setObjectName(_fromUtf8("textBrowser"))
        self.textBrowser.cursorPositionChanged.connect(self.highlight_line)
        self.highlighted_cursor = None
        self.horizontalLayout.addWidget(self.textBrowser, stretch=5)

        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))

        self.pageNumberHLayout = QtWidgets.QHBoxLayout()
        self.pageNumberLabel = QtWidgets.QLabel("Page:")
        self.inputPageNumber = QtWidgets.QLineEdit()
        self.inputPageNumber.setAlignment(QtCore.Qt.AlignCenter)
        self.inputPageNumber.setValidator(QtGui.QIntValidator())
        self.inputPageNumber.editingFinished.connect(self.jumpToPage)
        self.inputPageNumber.setReadOnly(True)

        self.pageNumberHLayout.addWidget(self.pageNumberLabel)
        self.pageNumberHLayout.addSpacing(10)
        self.pageNumberHLayout.addWidget(self.inputPageNumber)

        self.verticalLayout.addLayout(self.pageNumberHLayout)

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
        self.horizontalLayout.addLayout(self.verticalLayout, stretch=2)
        self.pushButton.clicked.connect(self.get_char)

        self.pushButton_7 = QtWidgets.QPushButton(test)
        self.pushButton_7.setObjectName(_fromUtf8("pushButton"))
        self.pushButton_7.clicked.connect(self.turn_highlighting_on)
        self.verticalLayout.addWidget(self.pushButton_7)

        self.pushButton_8= QtWidgets.QPushButton(test)
        self.pushButton_8.setObjectName(_fromUtf8("pushButton"))
        self.pushButton_8.clicked.connect(self.turn_polygon_selection_on)
        self.verticalLayout.addWidget(self.pushButton_8)

        self.pushButton_6 = QtWidgets.QPushButton(test)
        self.pushButton_6.setObjectName(_fromUtf8("pushButton_6"))
        self.pushButton_6.clicked.connect(self.transcribe_all_polygons)
        self.verticalLayout.addWidget(self.pushButton_6)

        self.pushButton_4 = QtWidgets.QPushButton(test)
        self.pushButton_4.setObjectName(_fromUtf8("pushButton_4"))
        self.pushButton_4.clicked.connect(self.previous_page)
        self.verticalLayout.addWidget(self.pushButton_4)

        self.pushButton_5 = QtWidgets.QPushButton(test)
        self.pushButton_5.setObjectName(_fromUtf8("pushButton_5"))
        self.pushButton_5.clicked.connect(self.next_page)
        self.verticalLayout.addWidget(self.pushButton_5)

        self.trainLinesButton = QtWidgets.QPushButton(test)
        self.trainLinesButton.clicked.connect(self.trainLines)
        self.verticalLayout.addWidget(self.trainLinesButton)

        self.retranslateUi(test)
        QtCore.QMetaObject.connectSlotsByName(test)

    def retranslateUi(self, test):
        """ Puts text on QWidgets """
        test.setWindowTitle(_translate("test", "test", None))
        self.label.setText(_translate("test", "                                               PDF Viewer                                                   ", None))
        self.pushButton_2.setText(_translate("test", "Import PDF", None))
        self.pushButton_3.setText(_translate("test", "Export PDF", None))
        self.pushButton.setText(_translate("test", "Editing Mode", None))
        self.pushButton_7.setText(_translate("test", "Highlighting Mode", None))
        self.pushButton_8.setText(_translate("test", "Polygon Selection Mode", None))
        self.pushButton_6.setText(_translate("test", "Transcribe All Polygons", None))
        self.pushButton_4.setText(_translate("test", "<- Previous Page", None))
        self.pushButton_5.setText(_translate("test", "Next Page ->", None))
        self.trainLinesButton.setText("Train")

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

        # Initialize page number layout
        self.initializePageNum()

    def initializePageNum(self):
        self.updatePageNum()
        self.inputPageNumber.setReadOnly(False)
        self.pageNumberLabel.setText(f"Page out of {len(self.imgs)}:")

    def updatePage(self):
        self.label._page = self.pages[self.page]
        self.textBrowser.setText(self.label._page._text)
        self.label.update()
        self.updatePageNum()

    def updatePageNum(self):
        self.inputPageNumber.setText(str(self.page + 1))

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
        pageNumber = int(self.inputPageNumber.text()) - 1
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
        image_name = self.label._page._selected_polygon._image_name
        # transcript = str("(" + str(p._polygon[0].x()) + ", " + str(p._polygon[0].y()) + ")")
        transcript = self.label._page.transcribePolygon(image_name)
        self.label._page._selected_polygon.set_transcription(transcript)
        self.add_transcriptions()

    def transcribe_all_polygons(self):
        """ Transcribes all polygons """
        # Add dummy info to text boxes
        for p in self.label._page._page_lines:
            image_name = p._image_name

            # transcript = str("(" + str(p._polygon[0].x()) + ", " + str(p._polygon[0].y()) + ")")
            transcript = self.label._page.transcribePolygon(image_name)
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
                fmt.setBackground(QtGui.QColor("white"))
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


class ImageLabel(QtWidgets.QLabel):
    def __init__(self, ui):
        """ Provides event support for the image label """
        super(ImageLabel, self).__init__()
        self._ui = ui
        self._page = None
        self._lines = []
        self._start_of_line = []
        self._end_of_line = []
        self.setMouseTracking(True)

    def contextMenuEvent(self, event):
        global mode
        if mode == "polygon_selection":
            contextMenu = QtWidgets.QMenu()
            delete = contextMenu.addAction("Delete")
            transcribe = contextMenu.addAction("Transcribe")
            action = contextMenu.exec_(self.mapToGlobal(event.pos()))

            point = QtCore.QPoint(event.x(), event.y())
            if self._page.pointInPolygon(point):
                self._page.selectClickedPolygon(point)
                if action == delete:
                    self._page.deleteSelectedPolygon()
                elif action == transcribe:
                    self._ui.transcribe_selected_polygon()

    def paintEvent(self, event):
        """ Paints a polygon on the pixmap after selection
            during selection of a polygon points the current line """
        global mode

        painter = QtGui.QPainter(self)
        if self._page:

            scaledPixmap = self._page._pixmap.scaled(self.rect().size(), QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation)
            drawRect = QtCore.QRect(self.rect().topLeft(), scaledPixmap.size())
            painter.drawPixmap(drawRect, scaledPixmap)

            painter.setPen(QtCore.Qt.red)

            if self._start_of_line and self._end_of_line:
                painter.drawLine(self._start_of_line, self._end_of_line)

            for start, end in self._lines:
                painter.drawLine(start, end)

            for page_line in self._page._page_lines:
                painter.drawConvexPolygon(page_line._polygon)

            if self._page._selected_polygon:
                for vertex in self._page._selected_polygon._vertices:
                    painter.drawEllipse(vertex[0]-5,vertex[1]-5,10,10)

        if mode == "highlighting":
            path = QtGui.QPainterPath()
            polyf = QtGui.QPolygonF()
            for point in self._page._polygon:
                x = float(point.x())
                y = float(point.y())
                pointf = QtCore.QPointF(x, y)
                polyf << pointf

            painter.setPen(QtCore.Qt.NoPen)
            color = QtGui.QColor(255, 255, 0, 80)
            path.addPolygon(polyf)
            painter.fillPath(path, color)

    def mousePressEvent(self, event):
        """ Collects points for the polygon and creates selection boxes """
        global mode
        point = QtCore.QPoint(event.x(), event.y())

        if mode == "polygon_selection":
            # make sure not already in a polygons
            if self._start_of_line or self._page.pointSelectsItem(point) == False:
                # removes bug where user can select a polygon draw a new one
                # and then delete the previous selection in one click
                self._page.selected_polygon = None
                if self._start_of_line:
                    self._lines.append((self._start_of_line, event.pos()))
                self._start_of_line = event.pos()
                self._page._polygon_points.append((event.x(),event.y()))
                self._page._polygon << event.pos()
            elif self._page.pointInVertexHandle(point):
                self._page._dragging_vertex = True
                self._page.selectClickedVertexHandle(point)
            else:
                self._page.selectClickedPolygon(point)
            self.update()
        if mode == "highlighting":
            for line in self._page._page_lines:
                poly = line._polygon
                if poly.containsPoint(point, 0):
                    block = line._block_number
                    textCursor = self._ui.textBrowser.textCursor()
                    textCursor.movePosition(1)
                    for _ in range(block):
                        textCursor.movePosition(12)
                    self._ui.textBrowser.setTextCursor(textCursor)
                    self._ui.highlight_line()

    def mouseMoveEvent(self, event):
        """ updates the painter and lets it draw the line from
            the last clicked point to end """
        point = event.pos()
        if self._page and self._page._dragging_vertex == True:
            self._page._selected_polygon._vertices[self._page._selected_vertex_index] = (point.x(),point.y())
            self._page._selected_polygon.updatePolygon()
        else:
            self._end_of_line = event.pos()

        self.update()

    def mouseReleaseEvent(self, event):

        if self._page._dragging_vertex:
            self._page._dragging_vertex = False
            self._page.updatePolygonCrop()


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
