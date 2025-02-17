
class Unrenderers {

    
    static async removeDropArea() {
        const dropArea = document.getElementById('drop-area');
        dropArea.style.display = `None`;
    }

    static async removeImageBox() {
        const imageBox = document.getElementById('image-box');
        imageBox.style.display = `None`;
    }
}

export { Unrenderers };
