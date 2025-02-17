import { Renderers } from "./renderers.js";
import { Unrenderers } from "./unrenderers.js";
import { ImageController } from "./imageController.js";

const mainImage = document.getElementById('main-image');
const imgInput = document.getElementById('image-input');
const imageController = new ImageController(mainImage);
imageController.initPinchZoom();
imageController.initScrollZoom();


imgInput.addEventListener('change', function(event) {
    Unrenderers.removeDropArea();
    Renderers.displayImage(event.target.files[0]);
});


document.addEventListener('wheel', function(event) {
    if (event.ctrlKey) {
      event.preventDefault();
    }
}, { passive: false });


document.addEventListener('mousedown', function(event) {
    event.preventDefault();
}, { passive: false });

