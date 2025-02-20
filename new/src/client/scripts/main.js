import { Renderers } from "./renderers.js";
import { Unrenderers } from "./unrenderers.js";
import { ImageController } from "./imageController.js";

const imageElement = document.getElementById('main-image');
const imageInput = document.getElementById('image-input');
const imageBox = document.getElementById('image-box');

const imageController = new ImageController(imageBox, imageElement);
imageController.initEvents();


imageInput.addEventListener('change', function(event) {
    Unrenderers.removeDropArea();
    imageController.loadImage(event.target.files[0]);
});


document.addEventListener('wheel', function(event) {
    if (event.ctrlKey) {
      event.preventDefault();
    }
}, { passive: false });


document.addEventListener('mousedown', function(event) {
    event.preventDefault();
}, { passive: false });

