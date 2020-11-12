import sys
import math
import pickle
from ui.window import *
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

    # save the main widget
    def save(self):
        try:
            pickle.dump(self, open(self.ui.fname + ".sav", "wb"))
        except:
            pass

    # overload the closeEvent function
    def closeEvent(self, event):
        # save the current project
        self.save()
        print("SJSJSDJLSJDLSJD")

        event.accept()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    test = MainWidget()
    test.show()
    sys.exit(app.exec_())
    test.exit()
