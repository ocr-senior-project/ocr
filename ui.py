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
        self.pushButton_2.setObjectName(_fromUtf8("pushButton_2"))
        self.pushButton_2.clicked.connect(self._ui.get_file)
        self._widgets_list.append(self.pushButton_2)

        self.pushButton_3 = QtWidgets.QPushButton()
        self.pushButton_3.setObjectName(_fromUtf8("pushButton_3"))
        self._widgets_list.append(self.pushButton_3)

        self.pushButton_7 = QtWidgets.QPushButton()
        self.pushButton_7.setObjectName(_fromUtf8("pushButton"))
        self.pushButton_7.clicked.connect(self._ui.turn_highlighting_on)
        self._widgets_list.append(self.pushButton_7)

        self.pushButton_8= QtWidgets.QPushButton()
        self.pushButton_8.setObjectName(_fromUtf8("pushButton"))
        self.pushButton_8.clicked.connect(self._ui.turn_polygon_selection_on)
        self._widgets_list.append(self.pushButton_8)

        self.pushButton_6 = QtWidgets.QPushButton()
        self.pushButton_6.setObjectName(_fromUtf8("pushButton_6"))
        self.pushButton_6.clicked.connect(self._ui.transcribe_all_polygons)
        self._widgets_list.append(self.pushButton_6)

        self.pushButton_9 = QtWidgets.QPushButton()
        self.pushButton_9.setObjectName(_fromUtf8("pushButton_9"))
        self.pushButton_9.clicked.connect(self._ui.trainLines)
        self._widgets_list.append(self.pushButton_9)

        self.pushButton_4 = QtWidgets.QPushButton()
        self.pushButton_4.setObjectName(_fromUtf8("pushButton_4"))
        self.pushButton_4.clicked.connect(self._ui.previous_page)
        self._widgets_list.append(self.pushButton_4)

        self.pushButton_5 = QtWidgets.QPushButton()
        self.pushButton_5.setObjectName(_fromUtf8("pushButton_5"))
        self.pushButton_5.clicked.connect(self._ui.next_page)
        self._widgets_list.append(self.pushButton_5)

        # retranslate
        self.pushButton_2.setText(_translate("test", "Import PDF", None))
        self.pushButton_3.setText(_translate("test", "Export PDF", None))
        self.pushButton_7.setText(_translate("test", "Highlighting Mode", None))
        self.pushButton_8.setText(_translate("test", "Polygon Selection Mode", None))
        self.pushButton_6.setText(_translate("test", "Transcribe All Polygons", None))
        self.pushButton_4.setText(_translate("test", "<- Previous Page", None))
        self.pushButton_5.setText(_translate("test", "Next Page ->", None))
        self.pushButton_9.setText(_translate("test", "Create Training Data", None))

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
