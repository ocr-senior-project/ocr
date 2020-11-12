# Project::SCRIBE

### A Quick Statement About Bugs
Thank you for trying this application! We would like to acknowledge a few things
before we get started. This software is very much in the "beta" phase of its
development. As such, there are some number of bugs that we are working to fix,
and almost everything about this application can change between now and the
initial release. Our goal is to create the best application we can, and we would
like your feedback. If you run into a bug, please contact us to let us know what
happened; please describe what you were doing when you encountered the bug and
what the bug looked like. Bugs range between causing the program to count
incorrectly to a full crash, and we need all of this information to figure out
what went wrong. You don't need to be super technical. Something like "I clicked
on the empty space, and the program crashed" (this is a real bug that we are
working on) is perfect. Thanks for taking the time to read this and for taking a
look at this project!

### Installation
Unfortunately, as of right now, installation is a bit of an involved process.

First, download
this repo. There are two main methods for this: downloading a zipped file and
cloning. To download this project as a zipped file, press the green "Code"
button and then "Download ZIP." You should then extract the files by opening the
zipped file and place them somewhere you can remember, like on your desktop. If
you choose to clone this repo instead, you need to install git for your command
line, then run the following command:
`git clone https://github.com/ocr-senior-project/ocr.git`

Next, you need to make sure you have Python installed. Because Python 3.9 was
released very recently, it might not have some things we need, so please install
Python 3.8. Head to the [Python website](https://www.python.org), go to
"Downloads," then scroll down and select the latest version of Python 3.8 (this
should be 3.8.6). Scroll down to the "Files" section, and download and run the
64-bit installer for your operating system.

Finally, you will need to install some packages. Currently, we only have an
executable for MacOS, but the command is relatively simple. If you're using
MacOS, just double click the "SCRIBE" file; it should update or install all the
packages we need and launch the app. If you're on Windows, you can right-click
the "install.py" file and choose to open it with Python; this should install all
the packages you need. Linux users will need to navigate to the directory with
the command line and run the following command: `python install.py`

This Linux installation is general purpose, and will work on every operating
system, if you feel so inclined to use the command line.

### Launching the Application
Mac users have this easy. Simply run the "SCRIBE" file, and the application
should start. Windows users will need to right-click the "ui.py" file and open
it with Python. Linux users will need to navigate to the directory with
the command line and run the following command: `python ui.py`

This Linux solution is general purpose, and will work on every operating system,
if you feel so inclined to use the command line.

### Using the Application
We currently have a hamburger menu, but are looking at changing it in the near
future. For now, please click the hamburger icon to show all of the features at
your disposal.

Before doing anything else, you will need to import a PDF. We have some custom
code that rips JPEG images from PDFs, so make sure that whatever you want to
open has JPEG images; if nothing is displayed, there are no JPEGs in the PDF. If
you see your document, then you're good to go!

You can click anywhere on the document to start drawing a polygon around a line
of text. There is no limit on the number of points you can use, so be as
accurate as you want! When you are done, press the `ESC` key to finish your
selection (this is a temporary feature, and we are working to clean this up).
You can now left-click on the  polygon to edit its corners, or right-click the
polygon to see more functionality. You now have the option to delete or
transcribe the polygon. There's no limit on the number of polygons you can have
on one page, so you can also continue to select all the polygons you need.
Instead of having to transcribe all the polygons individually, you can click the
"Transcribe All Polygons" button to transcribe every polygon on the page.
The polygons, and their transcriptions, stay with the page, so you can revisit
them later if you decide to move on.

Currently, the application has no way to save your progress (though we are
currently working on implementing this feature as you read this), and you will
have to start over every time you open the application.

### Citation
If you would like to use this project in your own work, please fork from this
project.

For our part. We are citing the following paper for its researchers improvements
to OCR and their implementation in Python 2.7.

@inproceedings{chammas2018handwriting,
  title={Handwriting Recognition of Historical Documents with few labeled data},
  author={Chammas, Edgard and Mokbel, Chafic and Likforman-Sulem, Laurence},
  booktitle={2018 13th IAPR International Workshop on Document Analysis Systems (DAS)},
  pages={43--48},
  year={2018},
  organization={IEEE}
}
