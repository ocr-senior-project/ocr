import numpy
from PIL import Image, ImageDraw
from PyQt5 import QtCore, QtGui, QtWidgets
import os


class Line():
    def __init__(self, polygon, image_name):
        self._polygon = polygon
        self._image_name = image_name

    def set_transcription(self, transcription):
        self._transcription = transcription

class Page:
    def __init__(self, image_object):
        self._image_object = image_object
        self._text = ""
        self._page_lines = []
        self._polygon_points = []
        self._polygon = QtGui.QPolygon()
        self._selected_polygon = None

    def selectPolygon(self):
        """ Called when a polygon is done being selected
            Crops polygon and stops drawing lines following mouse """

        # Stop drawing lines
        self._image_object._lines = []
        self._image_object._start_of_line = []

        # Crop the image, add the polygon to the image
        file_name = self.polygonCrop()
        self.addPolygon(self._polygon, file_name)

    def addPolygon(self, poly, image_name):
        """ adds self._polygon to the page"""
        line_object = Line(poly, image_name)
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

    def deleteSelectedPolygon(self, line):
        """ deletes selected polygon upon a double click """
        self._page_lines.remove(line)

    def scalePolygonPoints(self, im):
        """ Scale each point of polygon_points by the ratio of the original image to the
            displayed image """
        xscale = im.size[0] / self._image_object.rect().width()
        yscale = im.size[1] / self._image_object.rect().height()

        for k, v in enumerate(self._polygon_points):
            self._polygon_points[k] = (v[0] * xscale, v[1] * yscale)

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
        #os.system("cd HandwritingRecognitionSystem_v2; python test.py; cd -") # cd doesn't work here
        os.chdir('HandwritingRecognitionSystem_v2')
        os.system('python test.py')
        os.chdir('..')
        f = open("HandwritingRecognitionSystem_v2/decoded.txt", "r")
        return f.read()


    def polygonCrop(self):
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

        # crop to the bounding rectangle
        samples_dir = "HandwritingRecognitionSystem_v2/formalsamples/Images/000033/"
        image_name = f'000033/out{numcuts}'
        newIm.crop(end_crop).save(f'{samples_dir}out{numcuts}.png')
        return image_name


    def selectClickedPolygon(self, position):
        for line in self._page_lines:
            poly = line._polygon
            if poly.containsPoint(position, 0):
                if self._selected_polygon == line:
                    #self._popup = Polygon_Deletion_Popup(self._image_object)
                    #self._popup.show()
                    self.deleteSelectedPolygon(line)
                else:
                    print(poly)
                    self._selected_polygon = line

    def pointInPolygon(self, point):
        """ checks if a point is contained by any polygon on the current page"""
        for line in self._page_lines:
            poly = line._polygon
            if poly.containsPoint(point, 0):
                return True
        return False


class Polygon_Deletion_Popup(QtWidgets.QWidget):
    def __init__(self, ImageLabel):
        super(Polygon_Confirmation_Popup, self).__init__()
        #size the popup and move to the ideal position (next to the image viewer)
        self.resize(150,300)
        self.move(400,150)

        # store access to the ImageLabel
        self.ImageLabel = ImageLabel

        #Create the question label and buttons
        self._QuestionLabel = QtWidgets.QLabel(self)
        self._QuestionLabel.setText(_translate("self","Are you sure you want to delete this selection?", None))
        self._deleteButton = QtWidgets.QPushButton(self)
        self._deleteButton.setText(_translate("self","Yes", None))
        self._stopDeletionButton = QtWidgets.QPushButton(self)
        self._stopDeletionButton.setText(_translate("self","No",None))

        #add a layout to the widget
        self._layout = QtWidgets.QVBoxLayout(self)

        #put the question text and the buttons in the layout
        self._layout.addWidget(self._QuestionLabel)
        self._layout.addWidget(self._deleteButton)
        self._layout.addWidget(self._stopDeletionButton)

        #self._deleteButton.clicked.connect(self.ImageLabel._)
        #self._stopDeletionButton.clicked.connect(self.hide)
