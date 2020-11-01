
import numpy
from PIL import Image, ImageDraw
from PyQt5 import QtCore, QtGui, QtWidgets
import os
# import HandwritingRecognitionSystem_v2.test as test
from HandwritingRecognitionSystem_v2 import test

class Page:
    def __init__(self, image_object):
        self._image_object = image_object
        self._text = ""
        self._polygons = []
        self._polygon_points = []
        self._polygon = QtGui.QPolygon()

    def selectPolygon(self):
        """ Called when a polygon is done being selected
            Crops polygon and stops drawing lines following mouse """

        # Stop drawing lines
        self._image_object._lines = []
        self._image_object._start_of_line = []

        # Crop the image, add the polygon to the image
        file_name = self.polygonCrop()
        self.transcribePolygon(file_name)
        self.addPolygon()

    def addPolygon(self):
        """ adds self._polygon to the page"""
        self._polygons.append(self._polygon)
        self._polygon = QtGui.QPolygon()
        self._polygon_points = []
        self._image_object.update()

    def deletePolygon(self):
        """ deletes self._polygon from the image """
        self._polygons.remove(self._polygon)
        self._image_object.update()

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
        self._text += test.run()

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
        numcuts = len(self._polygons)

        # crop to the bounding rectangle
        samples_dir = "HandwritingRecognitionSystem_v2/formalsamples/Images/"
        image_name = f'000033/out0'
        newIm.crop(end_crop).save(f'{samples_dir}{image_name}.png')
        return image_name
