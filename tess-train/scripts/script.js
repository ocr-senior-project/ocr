/* =============================================================================
Auth: Nate Koike
Desc: a tool to help make training data with for tesseract-ocr
Date: 16 September 2020
============================================================================= */

// there is only one file in the directory. this is basically test code
const src = "images/p9_r1.png";

// the amount of padding on the left and top of the canvas
const pad = 10;

// the desired outline thickness
const outline = 2;

// get control of the canvas and the context
let cvs = document.getElementById("canvas"),
  ctx = cvs.getContext("2d");

// create image
let img = new Image();
img.src = src;

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
  ctx.clearRect(0, 0, cvs.width, cvs.height); // get rid of everything on the canvas
  loadImage(); // reload the image
  firstX = event.pageX;
  firstY = event.pageY;
}

function muFunc(event) {
  let x = event.pageX;
  let y = event.pageY;

  // the first y needs to be on the bottom
  if (firstY < y) {
    let swap = y;
    y = firstY;
    firstY = swap;
  }

  // the first x needs to be on the left
  if (firstX > x) {
    let swap = x;
    x = firstX;
    firstX = swap;
  }

  console.log("Tesseract training boundary box coordinates:");
  console.log(firstX, firstY, x, y, "0");

  // find the absolute distance between the mouse down and mouse up locations
  let distX = Math.abs(firstX - x),
    distY = Math.abs(firstY - y);

  // draw a rectangle
  ctx.beginPath;
  // draw the vertical lines
  // left boundary
  ctx.rect(firstX - outline - pad, y - pad, outline, distY + 2 * outline);

  // right boundary
  ctx.rect(x - pad, y - pad, outline, distY + 2 * outline);

  // draw the horizontal lines
  // top boundary
  ctx.rect(
    firstX - pad - outline,
    y - pad - outline,
    distX + 2 * outline,
    outline
  );

  // bottom boundary
  ctx.rect(
    firstX - pad - outline,
    firstY - pad + outline,
    distX + 2 * outline,
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
