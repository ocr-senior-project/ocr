import numpy
from PIL import Image, ImageDraw
from PyQt5 import QtCore, QtGui, QtWidgets
import os
# import HandwritingRecognitionSystem_v2.test as test
from HandwritingRecognitionSystem_v2 import test


class Line():
    def __init__(self, polygon, points, image_name):
        self._polygon = polygon
        self._image_name = image_name
        self._vertices = points
        self._vertex_handles = None

    def set_transcription(self, transcription):
        self._transcription = transcription

    def updatePolygon(self):
        self._polygon = QtGui.QPolygon()
        for vertex in self._vertices:
            point = QtCore.QPoint(vertex[0],vertex[1])
            self._polygon << point

class Page:
    def __init__(self, image_object):
        self._image_object = image_object
        self._text = ""
        self._page_lines = []
        self._polygon_points = []
        self._polygon = QtGui.QPolygon()
        self._selected_polygon = None
        self._selected_vertex_index = None
        self._dragging_vertex = False

    def selectPolygon(self):
        """ Called when a polygon is done being selected
            Crops polygon and stops drawing lines following mouse """

        # Stop drawing lines
        self._image_object._lines = []
        self._image_object._start_of_line = []
        # saving these points so they are not corrupted by the scalePolygonPoints function
        polygon_points_unscaled = self._polygon_points.copy()

        # Crop the image, add the polygon to the image
        file_name = self.polygonCrop()
        self.transcribePolygon(file_name)
        self.addPolygon(self._polygon, polygon_points_unscaled, file_name)

    def addPolygon(self, poly, points, image_name):
        """ adds self._polygon to the page"""
        line_object = Line(poly, points, image_name)
        self._page_lines.append(line_object)

        self._polygon = QtGui.QPolygon()
        self._polygon_points = []
        self._image_object.update()

    def deletePolygon(self):
        """ deletes self._polygon from the image """
        for line_object in self._page_lines:
            if line_object._polygon == self._polygon:
                self._page_lines.remove(line_object)
        self._image_object.update()

    def scalePolygonPoints(self, im):
        """ Scale each point of polygon_points by the ratio of the original image to the
        displayed image """
        xscale = im.size[0] / self._image_object.rect().width()
        yscale = im.size[1] / self._image_object.rect().height()

        for k, v in enumerate(self._polygon_points):
            self._polygon_points[k] = (v[0] * xscale, v[1] * yscale)

    def deleteSelectedPolygon(self):
        """ deletes selected polygon upon a double click """
        self._page_lines.remove(self._selected_polygon)
        self._popup.hide()
        self._selected_polygon = None
        self._image_object.update()

    def updatePolygonCrop(self):
        """ recrops polygon when vertices positions are changed by the user"""
        self._polygon_points = self._selected_polygon._vertices.copy()
        self.polygonCrop(self._selected_polygon._image_name)
        self._polygon_points = []

    def boundingRectangle(self, polygon):
        """ Returns box=(left, upper, right, lower) bounding a polygon """
        left, upper = right, lower = polygon[0]

        for point in polygon:
            if point[0] < left:
                left = point[0]
            if point[0] > right:
                right = point[0]
            if point[1] < upper:
                upper = point[1]
            if point[1] > lower:
                lower = point[1]
        return (left, upper, right, lower)

    def writePixmaptoFile(self):
        file_to_crop = QtCore.QFile("jpg.jpg")
        file_to_crop.open(QtCore.QIODevice.WriteOnly)
        self._pixmap.save(file_to_crop, "JPG")

    def transcribePolygon(self, image_name):
        f = open("HandwritingRecognitionSystem_v2/formalsamples/list", "w")
        f.write(image_name)
        f.close()
        self._text += test.run()

    def polygonCrop(self, fname=None):
        # CITE: https://stackoverflow.com/questions/22588074/polygon-crop-clip-using-python-pil
        # read image as RGB and add alpha (transparency)

        self.writePixmaptoFile()

        im = Image.open('jpg.jpg').convert("RGBA")
        self.scalePolygonPoints(im)

        end_crop = self.boundingRectangle(self._polygon_points)

        # convert to numpy (for convenience)
        imArray = numpy.asarray(im)

        # create mask
        maskIm = Image.new('L', (imArray.shape[1], imArray.shape[0]), 0)
        ImageDraw.Draw(maskIm).polygon(self._polygon_points, outline=1, fill=1)
        mask = numpy.array(maskIm)

        # assemble new image (uint8: 0-255)
        newImArray = numpy.empty(imArray.shape, dtype='uint8')

        # colors (three first columns, RGB)
        newImArray[:,:,:3] = imArray[:,:,:3]

        # transparency (4th column)
        newImArray[:,:,3] = mask*255

        # back to Image from numpy
        newIm = Image.fromarray(newImArray, "RGBA")

        numcuts = len(self._page_lines)
        image_name = f'000033/out{numcuts}'

        if fname:
            # if filename is given
            samples_dir = "HandwritingRecognitionSystem_v2/formalsamples/Images/"
            newIm.crop(end_crop).save(f'{samples_dir}{fname}.png')
        else:
            # saving to a new file
            samples_dir = "HandwritingRecognitionSystem_v2/formalsamples/Images/000033/"
            newIm.crop(end_crop).save(f'{samples_dir}out{numcuts}.png')
        return image_name


    def selectClickedPolygon(self, position):
        for line in self._page_lines:
            poly = line._polygon
            if poly.containsPoint(position, 0):
                if self._selected_polygon == line:
                    self._popup = Polygon_Deletion_Popup(self)
                    self._popup.show()
                    #self.deleteSelectedPolygon(line)
                else:
                    self._selected_polygon = line


    def selectClickedVertexHandle(self, point):
        """ determines clicked vertex handle and sets it to self._selected_vertex"""
        if self._selected_polygon:
            for vertex in self._selected_polygon._vertices:
                if vertex[0]-5 < point.x() < vertex[0]+5 and vertex[1]-5 < point.y() < vertex[1]+5:
                    self._selected_vertex_index = self._selected_polygon._vertices.index(vertex)
                    #self._selected_vertex = vertex
        return False


    def pointSelectsItem(self, point):
        """ checks if the clicked point interacts with any lines on the page """
        if self.pointInPolygon(point) or self.pointInVertexHandle(point):
            return True
        return False


    def pointInPolygon(self, point):
        """ checks if a point is contained by any polygon on the current page"""
        for line in self._page_lines:
            poly = line._polygon
            if poly.containsPoint(point, 0):
                return True
        return False


    def pointInVertexHandle(self, point):
        if self._selected_polygon:
            for vertex in self._selected_polygon._vertices:
                if vertex[0]-5 < point.x() < vertex[0]+5 and vertex[1]-5 < point.y() < vertex[1]+5:
                    return True
        return False


class Polygon_Deletion_Popup(QtWidgets.QWidget):
    def __init__(self, Page):
        super(Polygon_Deletion_Popup, self).__init__()
        #size the popup and move to the ideal position (next to the image viewer)
        self.resize(150,300)
        #self.move(400,150)

        # store access to the ImageLabel
        self._page = Page

        #Create the question label and buttons
        self._QuestionLabel = QtWidgets.QLabel(self)
        self._QuestionLabel.setText("Are you sure you want to delete this selection?")
        self._deleteButton = QtWidgets.QPushButton(self)
        self._deleteButton.setText("Yes")
        self._stopDeletionButton = QtWidgets.QPushButton(self)
        self._stopDeletionButton.setText("No")

        #add a layout to the widget
        self._layout = QtWidgets.QVBoxLayout(self)

        #put the question text and the buttons in the layout
        self._layout.addWidget(self._QuestionLabel)
        self._layout.addWidget(self._deleteButton)
        self._layout.addWidget(self._stopDeletionButton)

        self._deleteButton.clicked.connect(self._page.deleteSelectedPolygon)
        self._stopDeletionButton.clicked.connect(self.hide)
