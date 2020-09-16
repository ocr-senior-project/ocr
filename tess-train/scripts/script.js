/* =============================================================================
Auth: Nate Koike
Desc: a tool to help make training data with for tesseract-ocr
Date: 16 September 2020
============================================================================= */

// there is only one file in the directory. this is basically test code
const src = "images/780.png";

// the amount of padding on the left and top of the canvas
const pad = 10;

// the desired outline thickness
const outline = 2;

// get control of the canvas and the context
let cvs = document.getElementById("canvas"),
  ctx = cvs.getContext("2d");

// create image
let img = new Image();
img.src = "images/780.png";

// the first x and y coords that are clicked
let firstX, firstY;

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
  firstX = event.pageX - pad;
  firstY = event.pageY - pad;
}

function muFunc(event) {
  let x = event.pageX;
  let y = event.pageY;

  // the first x needs to be on the left
  if (firstX > x) {
    let swap = x;
    x = firstX;
    firstX = swap;
  }

  // the first y needs to be on the bottom
  if (firstY < y) {
    let swap = y;
    y = firstY;
    firstY = swap;
  }

  console.log(firstX, firstY, x, y);

  // draw a rectangle
  ctx.beginPath;
  // left boundary
  ctx.rect(
    firstX - outline,
    firstY - outline,
    outline,
    y - firstY - pad + outline
  );

  // top boundary
  ctx.rect(
    firstX - outline,
    firstY - outline,
    x - firstX - pad + outline,
    outline
  );

  // right boundary
  ctx.rect(x - pad, firstY - outline, outline, y - firstY - pad + outline);

  // bottom boundary
  ctx.rect(
    firstX - outline,
    y - pad - outline,
    x - firstX - pad + outline,
    outline
  );
  ctx.fill();
  ctx.closePath;
}

function init() {
  // load the image
  loadImage();

  // call mdFunc on mouse down
  cvs.addEventListener("mousedown", mdFunc);

  // log the coordinates to the console on mouse up
  cvs.addEventListener("mouseup", muFunc);
}

init();
