# -*- coding: utf-8 -*-

import sys
import numpy
from PIL import Image, ImageDraw
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

def resize_image(image):
    """ Resizes a jpg image to fit on screen """
    baseheight = 640
    img = Image.open(image)
    hpercent = (baseheight / float(img.size[1]))
    wsize = int((float(img.size[0]) * float(hpercent)))
    img = img.resize((wsize, baseheight), Image.ANTIALIAS)
    img.save(image)

class Ui_test:
    def setupUi(self, test):
        """ Creates layout of UI """
        test.setObjectName(_fromUtf8("test"))
        test.resize(1092, 589)
        self.horizontalLayout = QtWidgets.QHBoxLayout(test)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.label = ImageLabel(self)
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

        self.pushButton_4 = QtWidgets.QPushButton(test)
        self.pushButton_4.setObjectName(_fromUtf8("pushButton_4"))
        self.pushButton_4.clicked.connect(self.previous_page)
        self.verticalLayout.addWidget(self.pushButton_4)

        self.pushButton_5 = QtWidgets.QPushButton(test)
        self.pushButton_5.setObjectName(_fromUtf8("pushButton_5"))
        self.pushButton_5.clicked.connect(self.next_page)
        self.verticalLayout.addWidget(self.pushButton_5)

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

        # An integer of the page currently displayed
        self.page = 0

        # Return if no file name is given
        if not fname[self.page]:
            return

        # A list of page objects
        self.pages = []

        # Returns a list of all of the pixmaps of the pdf
        self.imgs = pp.get_pdf_contents(fname[self.page])

        # Make the appropriate number of pages and assign them pixmaps
        for pixmap in self.imgs:
            self.pages.append(Page())
            self.pages[-1].pixmap = pixmap

        # Set the displayed pixmap to be the pixmap of the current page object
        self.label.pixmap = self.pages[self.page].pixmap
        self.label.update()

    def next_page(self):
        """ Next page button """
        if self.page < len(self.imgs) - 1:
            self.pages[self.page].text = self.textBrowser.toPlainText()
            self.pages[self.page].polygons = self.label.polygons
            self.page += 1
            if len(self.pages)-1 < self.page:
                self.pages.append(Page())
            self.textBrowser.setText(self.pages[self.page].text)
            self.label.polygons = self.pages[self.page].polygons

            # Set the displayed pixmap to be the pixmap of the current page object
            self.label.pixmap = self.pages[self.page].pixmap
            self.label.update()
            # self.label.setPixmap(QtGui.QPixmap(self.imgs[self.page]))

    def previous_page(self):
        """ Previous page button """
        if self.page > 0:
            self.pages[self.page].text = self.textBrowser.toPlainText()
            self.pages[self.page].polygons = self.label.polygons
            self.page -= 1
            self.textBrowser.setText(self.pages[self.page].text)
            self.label.polygons = self.pages[self.page].polygons
            
            # Set the displayed pixmap to be the pixmap of the current page object
            self.label.pixmap = self.pages[self.page].pixmap
            self.label.update()
            # self.label.setPixmap(QtGui.QPixmap(self.imgs[self.page]))


class Page():
    def __init__(self):
        super(Page, self).__init__()
        self.text = ""
        self.polygons = []
        self.pixmap = None


class ImageLabel(QtWidgets.QLabel):
    def __init__(self, ui):
        """ Provides event support for the image label """
        # CITE: # https://doc.qt.io/qtforpython/PySide2/QtWidgets/QRubberBand.html
        super(ImageLabel, self).__init__()
        self.ui = ui
        self.rubberBand = 0
        self.line = 0
        self.lines = []
        self.polygonPoints = []
        self.polygon = QtGui.QPolygon()
        self.polygons = []
        self.released = False
        self.pixmap = []
        self.origin = []
        self.end = []
        self.scale = 1
        self.setMouseTracking(True)

    def paintEvent(self, event):
        """ Paints a polygon on the pixmap after selection
            during selection of a polygon points the current line """
        painter = QtGui.QPainter(self)
        if self.pixmap:
            # self.pixmap = self.pixmap.scaled(2000, 2000, QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation)

            painter.drawPixmap(self.rect(), self.pixmap)
            painter.setPen(QtCore.Qt.red)
            if self.origin and self.end:
                painter.drawLine(self.origin, self.end)
            for start, end in self.lines:
                painter.drawLine(start, end)
            for poly in self.polygons:
                painter.drawConvexPolygon(poly)
                
    def mousePressEvent(self, event):
        """ Collects points for the polygon and creates selection boxes """
        if self.origin:
            self.lines.append((self.origin, event.pos()))
        self.origin = event.pos()
        self.polygonPoints.append((event.x(),event.y()))
        self.polygon << event.pos()

    def mouseMoveEvent(self, event):
        """ updates the painter and lets it draw the line from
            the last clicked point to end """
        self.end = event.pos()
        self.update()

    def mouseReleaseEvent(self, event):
        self.update()

    def selectPolygon(self):
        """ Called when a polygon is done being selected
            Crops polygon and stops drawing lines following mouse """
        self.released = True
        self.lines = []
        self.origin = []
        self.update()
        self.polygonCrop()
        self.polygonPoints = []
        self.polygons.append(self.polygon)
        self.polygon = QtGui.QPolygon()

    def polygonCrop(self):
        # CITE: https://stackoverflow.com/questions/22588074/polygon-crop-clip-using-python-pil
        # read image as RGB and add alpha (transparency)
        im = Image.open(self.ui.imgs[self.ui.page]).convert("RGBA")

        xscale = im.size[0] / self.rect().width()
        yscale = im.size[1] / self.rect().height()

        for k, v in enumerate(self.polygonPoints):
            self.polygonPoints[k] = (v[0] * xscale, v[1] * yscale)

        # convert to numpy (for convenience)
        imArray = numpy.asarray(im)

        # create mask
        maskIm = Image.new('L', (imArray.shape[1], imArray.shape[0]), 0)
        ImageDraw.Draw(maskIm).polygon(self.polygonPoints, outline=1, fill=1)
        mask = numpy.array(maskIm)

        # assemble new image (uint8: 0-255)
        newImArray = numpy.empty(imArray.shape, dtype='uint8')

        # colors (three first columns, RGB)
        newImArray[:,:,:3] = imArray[:,:,:3]

        # transparency (4th column)
        newImArray[:,:,3] = mask*255

        # back to Image from numpy
        newIm = Image.fromarray(newImArray, "RGBA")
        numcuts = len(self.polygons)
        newIm.save(f'out{numcuts}.png')

class MainWidget(QtWidgets.QWidget):
    def __init__(self):
        """ Calls the UI immediately and provides event support """
        super(MainWidget, self).__init__()
        self.ui = Ui_test()
        self.ui.setupUi(self)

    def keyPressEvent(self, event):
        """ Called when a key is pressed """
        if event.key() == QtCore.Qt.Key_Escape and self.ui.label.polygonPoints != []:
            self.ui.label.selectPolygon()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    test = MainWidget()
    test.show()
    sys.exit(app.exec_())
