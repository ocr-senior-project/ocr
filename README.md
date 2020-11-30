# Project::SCRIBE

### A Quick Statement About Bugs
Thank you for trying this application! We would like to acknowledge a few things
before we get started. This software is still in development. As such, there are
some bugs, but as far as we've tested, they shouldn't be fatal. Our goal is to
create the best application we can, and we would like your feedback. If you run
into a bug, please contact us to let us know what happened; please describe what
you were doing when you encountered the bug and what the bug looked like. Bugs
range between causing the program to count incorrectly to a full crash, and we
need all of this information to figure out what went wrong. You don't need to be
super technical. Something like "I clicked on the empty space, and the program
crashed" is perfect. Thanks for taking the time to read this and for taking a
look at this project!

### Installation
Please download and extract this project to anywhere you can easily access.
Next, please open your command line (this would be Terminal on MacOS, Command
Prompt on Windows, and something like Konsole on a Linux distro) and navigate to
the directory containing the extracted project. Make sure you are in the
directory containing this readme file. Making sure that Python 3.8 or higher is
installed, and that you have PIP, run the following command:

`pip install -r requirements.txt`

If that doesn't work, please run this command instead:

`pip3 install -r requirements.txt`

### Launching the Application
With your command line still open from installation run the following command:

`python ui.py`

To run the program in the future, please use the command line again. This
entails using the command line go into the same directory from the installation
and running the above command again.

### Using the Application
First and foremost, you will need to import a PDF. We have some custom code that
rips JPEG images from PDFs, so make sure that whatever you want to open has JPEG
images; if nothing is displayed, there are no JPEGs in the PDF. If you see your
document, then you're good to go!

You can click anywhere on the document to start drawing a polygon around a line
of text. There is no limit on the number of points you can use, so be as
accurate as you want! When you are done, click the first vertex, marked by a
circle to finish your selection. You can now left-click on the  polygon to edit
its corners, or right-click the polygon to see more functionality. You now have
the option to delete or transcribe the polygon. There's no limit on the number
of polygons you can have on one page, so you can also continue to select all the
polygons you need. Instead of having to transcribe all the polygons
individually, you can click the "Transcribe All Polygons" button in the
"Polygons" menu to transcribe every polygon on the page. The polygons, and their
transcriptions, stay with the page, so you can revisit them later if you decide
to move on.

If you save your project, you no longer need the original PDF, and you will be
able to keep all your transcriptions and polygons, as well as save the model
that you loaded to accomplish those transcriptions.

Finally, you can export your transcriptions as either a PDF or a txt file.

### Citation
If you would like to use this project in your own work, please fork from this
project.

For our part, we are citing the following paper for its researchers improvements
to OCR and their implementation in Python 2.7.

```
@inproceedings{chammas2018handwriting,
  title={Handwriting Recognition of Historical Documents with few labeled data},
  author={Chammas, Edgard and Mokbel, Chafic and Likforman-Sulem, Laurence},
  booktitle={2018 13th IAPR International Workshop on Document Analysis Systems (DAS)},
  pages={43--48},
  year={2018},
  organization={IEEE}
}
```
