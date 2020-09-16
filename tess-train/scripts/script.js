/* =============================================================================
Auth: Nate Koike
Desc: a tool to help make training data with for tesseract-ocr
Date: 16 September 2020
============================================================================= */

// there is only one file in the directory. this is basically test code
const src = "images/780.png";

var cvs = document.getElementById("canvas");
var ctx = cvs.getContext("2d");

// create image
var img = new Image();
img.src = "images/780.png";

// the first x and y coords that are clicked
var firstX;
var firstY;

// load an image
function loadImage() {
  // create a function to draw an image on the canvas and dynamically resize the
  // canvas to fit
  let draw = () => {
    // dynamically change the height and width of the canvas
    cvs.width = img.width;
    cvs.height = img.height;

    // put the image on the canvas
    ctx.drawImage(img, 0, 0);
  };

  // load image first
  img.addEventListener("load", draw, false);

  // draw the image to the canvas
  draw();
}

// log the coords to the console
function mdFunc(event) {
  firstX = event.pageX;
  firstY = event.pageY;

  // create a rectangle
  ctx.beginPath;
}

// call mdFunc on mouse down
cvs.addEventListener("mousedown", mdFunc);

// log the coordinates to the console on mouse up
cvs.addEventListener("mouseup", event => {
  console.log(firstX, firstY, event.pageX, event.pageY);
});

loadImage();
