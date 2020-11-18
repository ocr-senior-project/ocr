# -*- coding: utf-8 -*-

import sys
import page
import math
import json
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
    def setupUi(self, test, fname=None):
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

        # save the filename
        self.fname = fname

        # initialize attributes for later use
        self.page = 0
        self.pages = []
        self.textCursor = None

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
        """ Gets the embedded jpgs from a pdf """

        fname = QtWidgets.QFileDialog.getOpenFileName(test, 'Open file','c:\\\\',"Image files (*.jpg *.pdf)")

        # Return if no file name is given
        if not fname[0]:
            return

        # save the filename
        self.fname = fname[0]

        # Returns a list of all of the pixmaps of the pdf
        imgs = pp.get_pdf_contents(fname[self.page])

        # Make the appropriate number of pages and assign them pixmaps
        for pixmap in imgs:
            self.pages.append(page.Page(self.label))
            self.pages[-1]._pixmap = pixmap

        self.label._page = self.pages[self.page]
        self.label.update()

        # Initialize page number layout
        self.initializePageNum()

    def initializePageNum(self):
        self.updatePageNum()
        self.popupMenu.inputPageNumber.setReadOnly(False)
        self.popupMenu.pageNumberLabel.setText(f"Page out of {len(self.pages)}:")

    def updatePage(self):
        self.label._page = self.pages[self.page]
        self.textBrowser.setText(self.label._page._text)
        self.label.update()
        self.updatePageNum()

    def updatePageNum(self):
        self.popupMenu.inputPageNumber.setText(str(self.page + 1))

    def next_page(self):
        """ Next page button """
        if self.page < len(self.pages) - 1:
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
        elif pageNumber >= len(self.pages):
            pageNumber = len(self.pages) - 1

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
        """ writes transcriptions into the text box """
        self.textBrowser.clear()
        for p in self.label._page._page_lines:
            if p._transcription:
                self.textBrowser.append(p._transcription)

    def transcribe_selected_polygon(self):
        """ Transcribes one polygon """
        p = self.label._page._selected_polygon

        transcript = self.label._page.transcribePolygon(p._image_name)
        p.set_transcription(transcript)

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

    # # load all the lines from the json file
    # def _load_lines(self, new_page, lines):
    #     # loop through all the lines in the page
    #     for i in range(len(lines)):
    #         # make a new line object
    #         new_line = page.Line(None, lines[i]["points"], f"out{i}.png")
    #
    #         # set the block number for proper rendering order
    #         new_line._block_number = lines[i]["block"]
    #
    #         # set the transcription
    #         new_line._transcription = lines[i]["transcription"]
    #
    #         # append the line object
    #         new_page._page_lines.append(new_line)

    # load all the lines from the json file
    def _load_lines(self, saved):
        # loop through all the lines in the page
        for i in range(len(lines)):
            # make a new line object
            new_line = page.Line(None, lines[i]["points"], f"out{i}.png")

            # set the block number for proper rendering order
            new_line._block_number = lines[i]["block"]

            # set the transcription
            new_line._transcription = lines[i]["transcription"]

            # append the line object
            new_page._page_lines.append(new_line)

    # load all the pages from the json file
    def _load_pages(self, pages):
        # loop through all the pages
        for i in range(len(pages)):
            # make a new page
            new_page = page.Page(self.label)

            # save the pixmap to the disk
            with open("jpg.jpg", "wb") as file:
                file.write(pages[i]["pixmap"].encode("Latin-1"))

            # restore the old pixmap
            new_page._pixmap = QtGui.QPixmap("jpg.jpg")

            # # restore the lines from of the page
            # self._load_lines(new_page, pages[i]["lines"])

            # add the page to the current project
            self.pages.append(new_page)

    # load the project from a json file
    def load_from_json(self):
        # get the file to load from
        fname = QtWidgets.QFileDialog.getOpenFileName(test, 'Open file','c:\\\\',"Image files (*.json *.prj)")

        # Return if no file name is given
        if not fname[0]:
            return

        # create a convenient way to access the saved information
        saved = None

        # load the json file as dictionary
        with open(fname[0], "r") as file:
            saved = json.loads(file.read())

        # restore the window size
        self.mainWindow.resize(saved["window"][0], saved["window"][1])

        # load all the pages
        self._load_pages(saved["pages"])

        # set the page number to the saved page number
        self.page = saved['index']

        self.label._page = self.pages[self.page]
        self.label.update()

        # Initialize page number layout
        self.initializePageNum()

        # load the lines on each page
        self._load_lines(saved["pages"])

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

        self.pushButton_10 = QtWidgets.QPushButton()
        self.pushButton_10.setObjectName(_fromUtf8("pushButton_10"))
        self.pushButton_10.clicked.connect(self._ui.load_from_json)
        self._widgets_list.append(self.pushButton_10)

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
        self.pushButton_10.setText(_translate("test", "Load Saved Project", None))
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

    # create a dictionary containing all the information needed to reconstruct
    # a single line on a page
    def _save_line(self, line):
        # create a dictionary for the information in the line
        current_line = {}

        current_line['points'] = line._vertices
        current_line['block'] = line._block_number
        current_line['transcription'] = line._transcription

        return current_line

    # create a dictionary containing all the information needed to reconstruct
    # a single page of a document
    def _save_page(self, page):
        # create a dictionary for the information in each page
        current_page = {}

        # create a list to hold all the lines
        lines = []

        # for every line on the page
        for i in range(len(page._page_lines)):
            # add the line to the dictionary of lines
            lines.append(self._save_line(page._page_lines[i]))

        # write the pixmap to a file
        page.writePixmaptoFile()

        # save the pixmap image data of the page into the dictionary
        current_page['pixmap'] = pp.read_binary("jpg.jpg")

        # save the lines of the document
        current_page['lines'] = lines

        return current_page

    # save the project
    # TODO: allow the user to pick the filename to which they save their project
    def save(self, fname="save"):
        # DEBUGGING CODE
        return

        try:
            # open a file to save
            save_file = open(fname + ".json", "w")

            # create a dictionary to hold all of the binaries
            project = {}

            # get the window size for the project to load polygons properly
            project['window'] = [self.size().width(), self.size().height()]

            # save the current page number
            project["index"] = self.ui.page

            # store all the pages in a list
            pages = []

            # for every page in the document
            for i in range(len(self.ui.pages)):
                # add the page to the dictionary of pages
                pages.append(self._save_page(self.ui.pages[i]))

            # save the pages to the project
            project['pages'] = pages

            # save the project
            save_file.write(json.dumps(project))

        except Exception as err:
            print("there was an error\n")
            print(err)

    # overload the closeEvent function
    def closeEvent(self, event):
        # save the current project
        self.save()
        event.accept()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    test = MainWidget()
    test.show()
    sys.exit(app.exec_())
