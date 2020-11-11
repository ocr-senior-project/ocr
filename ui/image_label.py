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
