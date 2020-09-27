# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'test.ui'
#
# Created: Thu Sep 10 20:52:52 2020
#      by: PyQt4 UI code generator 4.10.1
#
# WARNING! All changes made in this file will be lost!

import sys
from pdf2image import convert_from_path, convert_from_bytes
from PIL import Image
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QRubberBand
from PyQt5.QtCore import QRect, QSize

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
    baseheight = 640
    img = Image.open(image)
    hpercent = (baseheight / float(img.size[1]))
    wsize = int((float(img.size[0]) * float(hpercent)))
    img = img.resize((wsize, baseheight), Image.ANTIALIAS)
    img.save(image)


class Ui_test:
    def setupUi(self, test):
        test.setObjectName(_fromUtf8("test"))
        test.resize(1092, 589)
        self.horizontalLayout = QtWidgets.QHBoxLayout(test)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.label = QtWidgets.QLabel(test)
        self.label.setObjectName(_fromUtf8("label_2"))
        self.horizontalLayout.addWidget(self.label)

        self.textBrowser = QtWidgets.QTextEdit(test)
        self.textBrowser.setObjectName(_fromUtf8("textBrowser"))
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
        self.pushButton.clicked.connect(self.get_char)
        self.verticalLayout.addWidget(self.pushButton)
        self.horizontalLayout.addLayout(self.verticalLayout)

        self.retranslateUi(test)
        QtCore.QMetaObject.connectSlotsByName(test)


    def retranslateUi(self, test):
        test.setWindowTitle(_translate("test", "test", None))
        self.label.setText(_translate("test", "                                               PDF Viewer                                                   ", None))
        self.pushButton_2.setText(_translate("test", "Import PDF", None))
        self.pushButton_3.setText(_translate("test", "Export PDF", None))
        self.pushButton.setText(_translate("test", "Select Character", None))

    def get_char(self):
        self.textCursor = self.textBrowser.textCursor()
        selected = self.textCursor.selectionStart()
        text = self.textBrowser.toPlainText()
        print(text[selected])


    def get_file(self):
        fname = QtWidgets.QFileDialog.getOpenFileName(test, 'Open file','c:\\',"Image files (*.jpeg *.pdf)")
        #dir = QtWidgets.QFileDialog.getExistingDirectory()
        #print(dir)
        if not fname[0]:
            return
        images = convert_from_path(fname[0])
        images[0].save('out.jpg','JPEG')
        resized = resize_image('out.jpg')
        self.label.setPixmap(QtGui.QPixmap('out.jpg'))


class MyLabel(QtWidgets.QWidget):
    def __init__(self):
        super(MyLabel, self).__init__()
        self.ui = Ui_test()
        self.ui.setupUi(self)
        self.rubberBand = 0
        # self.setMouseTracking(True)

    def mousePressEvent(self, event):
        self.origin = event.pos()
        if not self.rubberBand:
            self.rubberBand = QRubberBand(QRubberBand.Rectangle, self)
        self.rubberBand.setGeometry(QRect(self.origin, QSize()))
        self.rubberBand.show()

    def mouseMoveEvent(self, event):
        self.rubberBand.setGeometry(QRect(self.origin, event.pos()).normalized())

    def mouseReleaseEvent(self, event):
        self.rubberBand.hide()
        print(self.origin, event.pos())


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    test = MyLabel()
    test.show()
    sys.exit(app.exec_())
