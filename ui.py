# -*- coding: utf-8 -*-
import sys
import os
import page
import math
import psutil
import time
from multiprocessing import Process
import json
from PyQt5 import QtCore, QtGui, QtWidgets
from file_manipulation.pdf import pdf_processing as pp
from HandwritingRecognitionSystem_v2 import train
from shutil import copyfile, rmtree

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


class Ui_test:
    def setupUi(self, MainWindow):
        """ Creates layout of UI """
        # Main Widget
        test = QtWidgets.QWidget(MainWindow)
        MainWindow.setWindowTitle("SCRIBE")
        MainWindow.setCentralWidget(test)

        test.setObjectName(_fromUtf8("test"))
        MainWindow.resize(1092, 589)
        self.model = "HandwritingRecognitionSystem_v2/MATRICULAmodel"

        self.process = QtCore.QProcess(test)
        self._pid = -1

        self.mainWindow = test

        self.pathToHandwritingSystem = os.getcwd()

        # Horizontal layout
        self.horizontalLayout = QtWidgets.QHBoxLayout(test)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))

        # Menu bar
        self.menuBar = QtWidgets.QMenuBar(test)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 1000, 21))

        self.fileMenu = self.menuBar.addMenu('&File') # Alt + F to open
        self.import_f = self.fileMenu.addAction('Import File')
        self.import_f.triggered.connect(self.get_file)
        self.export_f = self.fileMenu.addAction('Export File')
        self.export_f.triggered.connect(self.export_file)

        self.load_save = self.fileMenu.addAction('Load project')
        self.load_save.triggered.connect(self.load_from_json)
        self.save_proj = self.fileMenu.addAction('Save project')
        self.save_proj.triggered.connect(MainWindow.save)

        self.viewMenu = self.menuBar.addMenu('&View') # Alt + V to open
        self.polygon_layer = self.viewMenu.addAction('Turn Polygon Layer Off')
        self.highlighting = self.viewMenu.addAction('Turn Highlighting Off')
        self.highlighting.triggered.connect(self.toggle_highlighting)

        self.polygonMenu = self.menuBar.addMenu('&Polygons') # Alt + P to open
        self.transcribe = self.polygonMenu.addAction('Transcribe All Polygons')
        self.transcribe.triggered.connect(self.transcribe_all_polygons)
        self.train = self.polygonMenu.addAction('Train Lines from Scratch')
        self.train.triggered.connect(self.trainLines)
        self.continue_train = self.polygonMenu.addAction('Continue Training Existing Model')
        self.continue_train.triggered.connect(self.continueTraining)
        self.stop_train = self.polygonMenu.addAction('Stop Training')
        self.stop_train.triggered.connect(self.stopTraining)
        self.stop_train.setDisabled(True)

        MainWindow.setMenuBar(self.menuBar)

        # Image label
        self.label = ImageLabel(self)
        self.label.setObjectName(_fromUtf8("label_2"))
        self.horizontalLayout.addWidget(self.label, stretch=5)
        self.polygon_layer.triggered.connect(self.label.toggle_polygon_layer)

        # Text box
        self.textBrowser = QtWidgets.QTextEdit()
        self.textBrowser.setObjectName(_fromUtf8("textBrowser"))
        self.textBrowser.cursorPositionChanged.connect(self.highlight)
        self.textBrowser.textChanged.connect(self.saveText)
        self.highlighted_cursor = None
        self.highlighter_on = True
        self.horizontalLayout.addWidget(self.textBrowser, stretch=5)

        # save the filename
        self.fname = None

        # initialize attributes for later use
        self.page = 0
        self.pages = []
        self.textCursor = None

        # Page change stuff
        self.page_layout = QtWidgets.QVBoxLayout()
        self._h_layout = QtWidgets.QHBoxLayout()
        self.pageNumberLabel = QtWidgets.QLabel("Page ")
        self.inputPageNumber = QtWidgets.QLineEdit()
        self.inputPageNumber.setAlignment(QtCore.Qt.AlignCenter)
        self.inputPageNumber.setValidator(QtGui.QIntValidator())
        self.inputPageNumber.editingFinished.connect(self.jumpToPage)
        self.inputPageNumber.setReadOnly(True)
        self._h_layout.addWidget(self.pageNumberLabel)
        self._h_layout.addWidget(self.inputPageNumber)
        self.page_layout.addLayout(self._h_layout)

        self.prev_next_page_layout = QtWidgets.QHBoxLayout()
        self.previous_page_button = QtWidgets.QPushButton()
        self.previous_page_button.setObjectName(_fromUtf8("previous_page_button"))
        self.previous_page_button.clicked.connect(self.previous_page)
        self.prev_next_page_layout.addWidget(self.previous_page_button)
        self.next_page_button = QtWidgets.QPushButton()
        self.next_page_button.setObjectName(_fromUtf8("next_page_button"))
        self.next_page_button.clicked.connect(self.next_page)
        self.prev_next_page_layout.addWidget(self.next_page_button)
        self.page_layout.addLayout(self.prev_next_page_layout)
        self.horizontalLayout.addLayout(self.page_layout)

        # Put text on widgets
        self.retranslateUi(test)
        QtCore.QMetaObject.connectSlotsByName(test)

    def retranslateUi(self, test):
        """ Puts text on QWidgets """
        test.setWindowTitle(_translate("test", "test", None))
        self.previous_page_button.setText(_translate("test", "←", None))
        self.next_page_button.setText(_translate("test", "→", None))

    def export_file(self):
        text = self.textBrowser.toPlainText()
        file = open('out.txt','w')
        file.write(text)

    def get_file(self):
        """ Gets the embedded jpgs from a pdf """

        self.fname = QtWidgets.QFileDialog.getOpenFileName(test, 'Open file','c:\\\\',"Image files (*.jpg *.pdf)")[0]

        # Return if no file name is given
        if not self.fname:
            return

        # clear the list of pages and the current page
        self.page = 0
        self.pages = []

        # Returns a list of all of the pixmaps of the pdf
        imgs = pp.get_pdf_contents(self.fname)

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
        self.inputPageNumber.setReadOnly(False)
        self.pageNumberLabel.setText(f"Page out of {len(self.pages)}:")

    def updatePage(self):
        self.label._page = self.pages[self.page]

        self.label.resizePolygonsToPixmap()
        self.updatePageNum()
        self.updatePolygonFiles()
        self.updateTextBox()

    def updatePageNum(self):
        self.inputPageNumber.setText(str(self.page + 1))

    def updatePolygonFiles(self):
        """ updates the polygon crop files in the HandwritingRecognitionSystem to the current page's page lines"""
        for line in self.label._page._page_lines:
            file_path = "HandwritingRecognitionSystem_v2/formalsamples/Images/"+line._image_name
            self.label._page._polygon_points = line._vertices.copy()
            self.label._page.polygonCrop(file_path)
            self.label._page._polygon_points = []

    def next_page(self):
        """ Next page button """
        if hasattr(self, "page") and self.page < len(self.pages) - 1:
            # change the page index and update the page
            self.page += 1
            self.updatePage()
        else:
            print('\a')

    def previous_page(self):
        """ Previous page button """
        if hasattr(self, "page") and self.page > 0:
            self.page -= 1
            self.updatePage()
        else:
            print('\a')

    def trainLines(self, continue_training=False):
        """ train on selected polygons """
        # only train if the page is loaded
        if self.label._page:
            self.model = QtWidgets.QFileDialog.getExistingDirectory()

            # Return if no file name is given
            if not self.model:
                return

            if not continue_training:
                rmtree(f"{self.model}/Text")
                rmtree(f"{self.model}/Images")
                rmtree(f"{self.model}/Labels")

            if not os.path.isdir(f"{self.model}/Text/"):
                os.mkdir(f"{self.model}/Text/")
            if not os.path.isdir(f"{self.model}/Images/"):
                os.mkdir(f"{self.model}/Images/")
            if not os.path.isdir(f"{self.model}/Labels/"):
                os.mkdir(f"{self.model}/Labels/")
            copyfile('HandwritingRecognitionSystem_v2/UImodel/CHAR_LIST', f"{self.model}/CHAR_LIST")


            # change button text and disconnect from trainLines
            self.train.setDisabled(True)
            self.continue_train.setDisabled(True)
            self.stop_train.setDisabled(False)

            # start training process
            file_number = self.label._page.trainLines()
            self.process = Process(
                target=train.run,
                args=(
                    file_number,
                    self.model,
                    continue_training,
                    )
                )
            self.process.start()

    def continueTraining(self):
        """ pick a model to continue training from for selected polygons """
        self.trainLines(True)

    def stopTraining(self):
        # change button text and disconnect from stopTraining function
        self.train.setDisabled(False)
        self.continue_train.setDisabled(False)
        self.stop_train.setDisabled(True)

        # kill the training process
        self.process.terminate()
        self.process.join()

    def jumpToPage(self):
        pageNumber = int(self.inputPageNumber.text()) - 1
        if pageNumber < 0:
            pageNumber  = 0
        elif pageNumber >= len(self.pages):
            pageNumber = len(self.pages) - 1

        # change the page index and object
        self.page = pageNumber
        self.updatePage()

    def add_transcriptions(self):
        """ Prints transcriptions onto the text box """
        self.highlighter_on = False
        self.textBrowser.clear()
        poly_lines = self.label._page._page_lines
        for p in poly_lines:
            if p._transcription:
                self.textBrowser.append(p._transcription)
        self.highlighter_on = True

        # rehighlight previously highlighted line
        if self.label._page._highlighted_polygon:
            index = self.label._page._highlighted_polygon._block_number
            self.move_cursor(index)
            self.highlight_line()

    def transcribe_selected_polygon(self):
        """ Transcribes one polygon """
        p = self.label._page._selected_polygon
        transcript = self.label._page.transcribePolygon(p._image_name)

        p.set_transcription(transcript)
        p._is_transcribed = True
        self.updateTextBox()

    def transcribe_all_polygons(self):
        """ Transcribes all polygons """
        if not self.label._page:
            return

        for p in self.label._page._page_lines:
            if not p._is_transcribed and not p._ready_for_training:
                transcript = self.label._page.transcribePolygon(p._image_name)
                p.set_transcription(transcript)
                p._is_transcribed = True
        self.updateTextBox()

    def toggle_highlighting(self):
        if self.highlighter_on:
            self.highlighter_on = False
            self.highlighting.setText('Turn Highlighting On')
            # clear highlighted text
            if self.highlighted_cursor:
                old_cursor = self.textBrowser.textCursor()
                fmt = QtGui.QTextBlockFormat()
                fmt.setBackground(QtGui.QColor("white"))
                self.highlighted_cursor.setBlockFormat(fmt)
                self.textBrowser.setTextCursor(old_cursor)
                self.highlighted_cursor = None
                self.label._page._highlighted_polygon = None
        else:
            self.highlighter_on = True
            self.highlighting.setText('Turn Highlighting Off')

        self.label.update()

    def move_cursor(self, line):
        """ Moves cursor to given line """
        textCursor = self.textBrowser.textCursor()
        textCursor.movePosition(1)
        for _ in range(line):
            textCursor.movePosition(12)
        self.textBrowser.setTextCursor(textCursor)

    def highlight_line(self):
        """ Highlights line where cursor currently is """
        if self.highlighter_on and self.label._page._selected_polygon and self.label._page._selected_polygon._transcription:
            fmt = QtGui.QTextBlockFormat()

            # clear prevosly highlighted block, if any
            if self.highlighted_cursor:
                fmt.setBackground(QtGui.QColor("white"))
                self.highlighted_cursor.setBlockFormat(fmt)

            # highlight block cursor is currently on
            self.highlighted_cursor = self.textBrowser.textCursor()
            fmt.setBackground(QtGui.QColor("yellow"))
            self.highlighted_cursor.setBlockFormat(fmt)

    def highlight(self):
        """ Highlights line where cursor is and the corresponding polygon.
        Called when cursor position changes. """

        if self.highlighter_on:
            index = self.textBrowser.textCursor().blockNumber()

            # select and highlight corresponding polygon
            for item in self.label._page._page_lines:
                if item._block_number == index:
                    self.label._page._highlighted_polygon = item
                    self.label._page._selected_polygon = item
                    self.label.update()

            # highlight line
            self.highlight_line()

    def updateTextBox(self):
        if self.label._page:
            text = ""
            for line in self.label._page._page_lines:
                text = text + line._transcription + "\n"
            # chops of final newline
            text = text[:-1]
            self.textBrowser.setText(text)

    def saveText(self):
        if self.label._page:
            self.label._page.saveLines()
        else:
            self.textBrowser.undo()
            print('\a')

    def selectModel(self):
        """allows user to select the model they want to use"""
        self.model = QtWidgets.QFileDialog.getExistingDirectory()

    # load all the lines from the json file
    def _load_lines(self, new_page, lines):
        # loop through all the lines in the page
        for i in range(len(lines)):
            # make a new line object
            new_line = page.Line(None, lines[i]["points"], f"out{i}.png")

            # backwards compatibility
            try:
                # set the _is_transcribed and _ready_for_training attributes
                new_line._is_transcribed = lines[i]['transcribed']
                new_line._ready_for_training = lines[i]['training']
            except:
                pass

            # make the polygon for the line
            new_line.updatePolygon()

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

            # restore the lines from of the page
            self._load_lines(new_page, pages[i]["lines"])

            # add the page to the current project
            self.pages.append(new_page)

    # load the project from a json file
    def load_from_json(self):
        # get the file to load from
        fname = QtWidgets.QFileDialog.getOpenFileName(test, 'Open file','c:\\\\',"Image files (*.json *.prj)")

        # Return if no file name is given
        if not fname[0]:
            return

        # set the filename
        self.fname = fname[0]

        # clear the list of pages and the current page
        self.page = 0
        self.pages = []

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

        # add the transcriptions
        self.updateTextBox()


class ImageLabel(QtWidgets.QLabel):
    def __init__(self, ui):
        """ Provides event support for the image label """
        super(ImageLabel, self).__init__()
        self._ui = ui
        self._page = None
        self._lines = []
        self._start_of_line = []
        self._end_of_line = []
        self._polygon_layer = True
        self.setMouseTracking(True)

    def toggle_polygon_layer(self):
        if self._polygon_layer:
            self._polygon_layer = False
            self._ui.polygon_layer.setText('Turn Polygon Layer On')
        else:
            self._polygon_layer = True
            self._ui.polygon_layer.setText('Turn Polygon Layer Off')
        self.update()

    def contextMenuEvent(self, event):
        """ Right click menu """
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
        painter = QtGui.QPainter(self)

        if self._page:
            scaledPixmap = self._page._pixmap.scaled(self.rect().size(), QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation)
            self._page._pixmap_rect = QtCore.QRect(self.rect().topLeft(), scaledPixmap.size())
            painter.drawPixmap(self._page._pixmap_rect, scaledPixmap)

            painter.setPen(QtCore.Qt.red)

            if self._polygon_layer:
                if self._page._polygon_start:
                    # draw ellipse for first point in polygon
                    painter.drawEllipse(self._page._polygon_start[0]-5,self._page._polygon_start[1]-5,10,10)

                if  self._start_of_line and self._end_of_line:
                    painter.drawLine(self._start_of_line, self._end_of_line)

                for start, end in self._lines:
                    painter.drawLine(start, end)

                for page_line in self._page._page_lines:
                    if page_line._is_transcribed:
                        painter.setPen(QtCore.Qt.green)
                    elif page_line._ready_for_training:
                        painter.setPen(QtCore.Qt.yellow)
                    else:
                        painter.setPen(QtCore.Qt.red)
                    painter.drawConvexPolygon(page_line._polygon)

            painter.setPen(QtCore.Qt.red)

            if self._page._selected_polygon:
                if self._polygon_layer:
                    # Show vertices
                    for vertex in self._page._selected_polygon._vertices:
                        painter.drawEllipse(vertex[0]-5,vertex[1]-5,10,10)

            # highlight polygon
            if self._ui.highlighter_on and self._page._highlighted_polygon:
                path = QtGui.QPainterPath()
                polyf = QtGui.QPolygonF()
                for point in self._page._highlighted_polygon._polygon:
                    x = float(point.x())
                    y = float(point.y())
                    pointf = QtCore.QPointF(x, y)
                    polyf << pointf

                painter.setPen(QtCore.Qt.NoPen)
                color = QtGui.QColor(255, 255, 0, 80)
                path.addPolygon(polyf)
                painter.fillPath(path, color)

    def resizeEvent(self, event):
        """ scale polygons based on the image size during window resizing """
        if not self._page:
            return

        self.resizePolygonsToPixmap()

    def resizePolygonsToPixmap(self):
        scaledPixmap = self._page._pixmap.scaled(self.rect().size(), QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation)
        new_pixmap_rect = QtCore.QRect(self.rect().topLeft(), scaledPixmap.size())

        scale_x = new_pixmap_rect.size().width() / self._page._pixmap_rect.size().width()
        scale_y = new_pixmap_rect.size().height() / self._page._pixmap_rect.size().height()

        for page_line in self._page._page_lines:
            for i, point in enumerate(page_line._vertices):
                page_line._vertices[i] = (point[0] * scale_x, point[1] * scale_y)
            page_line.updatePolygon()

        self._page._pixmap_rect = new_pixmap_rect
        self.update()


    def mousePressEvent(self, event):
        """ Collects points for the polygon and creates selection boxes """
        if not self._page:
            return

        point = QtCore.QPoint(event.x(), event.y())

        # make sure not already in polygons
        if self._polygon_layer and (self._start_of_line or self._page.pointSelectsItem(point) == False):
            # removes bug where user can select a polygon draw a new one
            # and then delete the previous selection in one click
            if (self._page._polygon_start and
                self._page._polygon_start[0]-5 < point.x() < self._page._polygon_start[0]+5 and
                self._page._polygon_start[1]-5 < point.y() < self._page._polygon_start[1]+5):
                # close the polygon
                self._page.selectPolygon()
                self._page._selected_polygon = None
                self._page._polygon_start = None

            else:
                self._page._selected_polygon = None

                if self._start_of_line:
                    self._lines.append((self._start_of_line, event.pos()))
                else:
                    # first point in polygon
                    self._page._polygon_start = event.x(),event.y()
                self._start_of_line = event.pos()
                self._page._polygon_points.append((event.x(),event.y()))
                self._page._polygon << event.pos()

        elif self._polygon_layer and self._page.pointInVertexHandle(point):
            self._page._dragging_vertex = True
            self._page.selectClickedVertexHandle(point)

        else:
            # select clicked polygon
            self._page.selectClickedPolygon(point)

            # highlight if selected polygon has been transcribed
            if self._page._selected_polygon._transcription and self._ui.highlighter_on:
                self._page._highlighted_polygon = self._page._selected_polygon

                if self._ui.highlighted_cursor and self._ui.highlighted_cursor.blockNumber == self._page._selected_polygon._block_number:
                    # unhighlight when clicking a highlighted polygon
                    pass
                else:
                    # move cursor to corresponding line
                    self._ui.move_cursor(self._page._selected_polygon._block_number)

                    # highlight line
                    self._ui.highlight_line()

        self.update()

    def mouseMoveEvent(self, event):
        """ updates the painter and lets it draw the line from
            the last clicked point to end """
        if not self._page:
            return
        point = event.pos()
        if self._page and self._page._dragging_vertex == True:
            self._page._selected_polygon._vertices[self._page._selected_vertex_index] = (point.x(),point.y())
            self._page._selected_polygon.updatePolygon()
        else:
            self._end_of_line = event.pos()

        self.update()

    def mouseReleaseEvent(self, event):
        if not self._page:
            return

        if self._page._dragging_vertex:
            self._page._dragging_vertex = False
            self._page.updatePolygonCrop()


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        """ Calls the UI immediately and provides event support """
        super(MainWindow, self).__init__()
        self.ui = Ui_test()
        self.ui.setupUi(self)

    def keyPressEvent(self, event):
        """ Called when a key is pressed """
        if event.key() == QtCore.Qt.Key_Escape and len(self.ui.label._page._polygon_points) > 0:
            # Delete polygon user is currently making
            self.ui.label._page._selected_polygon = None
            self.ui.label._page._polygon_start = None
            self.ui.label._lines = []
            self.ui.label._start_of_line = []
            self.ui.label._page._polygon = QtGui.QPolygon()
            self.ui.label._page._polygon_points = []
            self.ui.label.update()

    # create a dictionary containing all the information needed to reconstruct
    # a single line on a page
    def _save_line(self, line):
        # create a dictionary for the information in the line
        current_line = {}

        current_line['points'] = line._vertices
        current_line['transcribed'] = line._is_transcribed
        current_line['training'] = line._ready_for_training
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
    def save(self):
        # get a nice filename
        fname = self.ui.fname

        # format the filename nicely
        if fname == None:
            fname = ""
        else:
            fname = "".join(fname.split('.')[:-1])

        # get the file to save to
        fname = QtWidgets.QFileDialog.getSaveFileName(test, 'Save file',f'c:\\\\{fname}.json',"Image files (*.json *.prj)")

        # Return if no file name is given
        if not fname[0]:
            return

        try:
            self.fname = fname[0]

            # open a file to save
            save_file = open(fname[0], "w")

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

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    test = None
    Window = MainWindow()
    Window.show()
    sys.exit(app.exec_())
