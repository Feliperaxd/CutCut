
class Renderers {

    
    static async displayImage(image) {
        const imageElement = document.getElementById('main-image');
        const imageBox = document.getElementById('image-box');
        const imageUrl = URL.createObjectURL(image);
        
        imageBox.style.display = `Flex`;
        imageElement.src = imageUrl;
    }

}

export { Renderers };
