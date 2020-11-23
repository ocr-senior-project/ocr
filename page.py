import numpy
from PIL import Image, ImageDraw
from PyQt5 import QtCore, QtGui, QtWidgets
import os
import glob
from HandwritingRecognitionSystem_v2 import test, config


class Line():
    def __init__(self, polygon, points, image_name):
        self._polygon = polygon
        self._image_name = image_name
        self._vertices = points
        self._vertex_handles = None
        self._block_number = None
        self._transcription = ""
        self._is_transcribed = False
        self._ready_for_training = False

    def set_transcription(self, transcription):
        self._transcription = transcription

    def updatePolygon(self):
        self._polygon = QtGui.QPolygon()
        for vertex in self._vertices:
            point = QtCore.QPoint(vertex[0],vertex[1])
            self._polygon << point

    def set_block_number(self, number):
        """ Sets the index of the polygon/text """
        self._block_number = number

class Page:
    def __init__(self, image_object):
        self._image_object = image_object
        self._page_lines = []
        self._polygon_points = []
        self._polygon = QtGui.QPolygon()
        self._selected_polygon = None
        self._highlighted_polygon = None
        self._selected_vertex_index = None
        self._pixmap = None
        self._dragging_vertex = False
        self._pixmap_rect = self._image_object.rect()
        self._polygon_start = None

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

        # self.transcribePolygon(file_name)
        self.addPolygon(self._polygon, polygon_points_unscaled, file_name)
        self._image_object._ui.updateTextBox()

    def p_line_key(self, poly_line):
        a = poly_line._polygon
        min_a = a[0].y()
        for point in a:
            if point.y() < min_a:
                min_a = point.y()
        return min_a

    def writeListFile(self, file_number):
        list_contents = ""
        for i in range(file_number):
            list_contents += str(i)
            if i != file_number - 1:
                list_contents += "\n"

        list_file = open("list", "w")
        list_file.write(list_contents)
        list_file.close()

    def text_to_label(self, text):

        with open("../CHAR_LIST", "rb") as f:
            chars = f.read().decode("utf-8")

        chars = chars.split('\n')
        label = ''
        for letter in text:
            if letter == ' ':
                letter = '<SPACE>'
            for ind, char in enumerate(chars):
                if letter == char:
                    label += str(ind) + ' '
        return label

    def trainLines(self):
        self.saveLines()
        os.chdir(self._image_object._ui.model)
        for line in self._page_lines:
            line._is_transcribed = True
            os.chdir("Text/")
            #number of files in the directory
            file_number = len(glob.glob('*'))
            text_file = open("%d.txt" % file_number, "w")
            text_file.write(line._transcription)
            text_file.close()

            os.chdir("..")
            os.chdir("Labels/")
            label_file = open("%d.tru" % file_number, "w")
            label_file.write(self.text_to_label(line._transcription))
            label_file.close()

            os.chdir("..")
            os.chdir("Images/")
            self._polygon_points = line._vertices.copy()
            self.polygonCrop(f"{file_number}")
            os.chdir("..")

        self.writeListFile(file_number + 1)

        os.chdir(self._image_object._ui.pathToHandwritingSystem)
        return file_number + 1

    def saveLines(self):
        text = self._image_object._ui.textBrowser.toPlainText()
        text_lines = text.split("\n")
        if len(self._page_lines) == 0:
            return
        elif len(text_lines) > len(self._page_lines):
            self._image_object._ui.textBrowser.undo()
            print('\a')
        else:
            line_number = 0
            for line in self._page_lines:
                if text_lines[line_number] == "":
                    line._transcription = ""
                    line._is_transcribed = False
                    line._ready_for_training = False
                if text_lines[line_number] != line._transcription:
                    line._transcription = text_lines[line_number]
                    line._ready_for_training = True
                    line._is_transcribed = False
                line_number = line_number + 1
        self._image_object.update()

    def sortLines(self):
        """ Sorts polygons by position, updating index """
        self._page_lines.sort(key=self.p_line_key)
        for i in range(len(self._page_lines)):
            self._page_lines[i].set_block_number(i)

    def addPolygon(self, poly, points, image_name):
        """ adds self._polygon to the page"""
        line_object = Line(poly, points, image_name)
        self._page_lines.append(line_object)
        self.sortLines()

        self._polygon = QtGui.QPolygon()
        self._polygon_points = []
        self._image_object.update()

    def scalePolygonPoints(self, im):
        """ Scale each point of polygon_points by the ratio of the original image to the
            displayed image """
        xscale = im.size[0] / self._pixmap_rect.width()
        yscale = im.size[1] / self._pixmap_rect.height()

        for k, v in enumerate(self._polygon_points):
            self._polygon_points[k] = (v[0] * xscale, v[1] * yscale)

    def deleteSelectedPolygon(self):
        """ deletes selected polygon upon a double click """
        self._page_lines.remove(self._selected_polygon)
        self._selected_polygon = None
        self._highlighted_polygon = None
        self.sortLines()

        self._image_object.update()
        self._image_object._ui.updateTextBox()

    def updatePolygonCrop(self):
        """ recrops polygon when vertices positions are changed by the user"""
        self._polygon_points = self._selected_polygon._vertices.copy()
        file_path = "HandwritingRecognitionSystem_v2/formalsamples/Images/"+self._selected_polygon._image_name
        self.polygonCrop(file_path)
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
        # return test.run(self._image_object._ui.model)
        return test.run()

    def polygonCrop(self, fname=None, fullpath=None):
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
            newIm.crop(end_crop).save(f'{fname}.png')
        else:
            # saving to a new file
            samples_dir = "HandwritingRecognitionSystem_v2/formalsamples/Images/000033/"
            newIm.crop(end_crop).save(f'{samples_dir}out{numcuts}.png')

        return image_name

    def selectClickedPolygon(self, position):
        for line in self._page_lines:
            poly = line._polygon
            if poly.containsPoint(position, 0):
                self._selected_polygon = line

    def selectClickedVertexHandle(self, point):
        """ determines clicked vertex handle and sets it to self._selected_vertex"""
        if self._selected_polygon:
            for vertex in self._selected_polygon._vertices:
                if vertex[0]-5 < point.x() < vertex[0]+5 and vertex[1]-5 < point.y() < vertex[1]+5:
                    self._selected_vertex_index = self._selected_polygon._vertices.index(vertex)
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
