class ImageController {
    
    constructor(box, element, url = undefined, scale = 1, minScale = 0.25, maxScale = 5, stepScale = 0.1) {
        this.element = element;
        this.box = box;
        this.url = url;
        this.scale = scale;
        this.minScale = minScale;
        this.maxScale = maxScale;
        this.stepScale = stepScale;
        this.position = { x: 0, y: 0 };
        this.isDragging = false;
        this.touches = [];
    }

    initEvents() {
        document.addEventListener('wheel', (event) => this.wheelMove(event), { passive: false });
        document.addEventListener('mousedown', (event) => this.mouseDown(event), { passive: false });
        document.addEventListener('touchstart', (event) => this.touchStart(event), { passive: false });
        document.addEventListener('touchmove', (event) => this.touchMove(event), { passive: false });
        document.addEventListener('touchend', () => this.touchEnd());
    }

    loadImage(image) {
        this.url = URL.createObjectURL(image);
        
        this.box.style.display = `flex`;
        this.element.src = this.url;


        const boxSize = this.getSize(this.box);
        const elementSize = this.getSize(this.element);

        this.element.onload = () => { NAO TA FUNCIONANDO E PRECISA DO GET SIZE TO FIT
            this.position = {
                x: (boxSize.width - elementSize.width) / 2,
                y: (boxSize.height - elementSize.height) / 2
            };
            this.applyPosition(this.position.x, this.position.y);
        };
    }

    getSizeToFit(currentSize, maxSize) {
        const scale = Math.min(
            maxSize.width / currentSize.width, 
            maxSize.height / currentSize.height
        );

        return {
            width: currentSize.width * scale,
            height: currentSize.height * scale
        };
    }

    getSize(element) {
        return { 
            width: parseFloat(getComputedStyle(element).width),
            height: parseFloat(getComputedStyle(element).height)
        };
    }

    zoomIn() {
        this.scale += this.stepScale;
        this.applyScale(this.scale);
    }

    zoomOut() {
        this.scale -= this.stepScale;
        this.applyScale(this.scale);
    }

    clampScale(scale) {
        return Math.min(Math.max(scale, this.minScale), this.maxScale);
    }

    applyScale(scale) {
        this.scale = this.clampScale(scale);
        this.element.style.transform = `scale(${this.scale})`;
    }

    applyPosition(x, y) {
        this.position = { x, y };
        this.element.style.left = `${this.position.x}px`;
        this.element.style.top = `${this.position.y}px`;
    }

    handleZoom(event) {
        if (event.deltaY < 0) {
            this.zoomIn();
        } else {
            this.zoomOut();
        }
    }

    moveY(value) {

    }

    moveX(value) {

    }

    handleMovement(event) {
        
    }

    mouseDown(event) {
        if (event === 1) {
            event.preventDefault();
            this.handleMovement(event);
        }
    }

    wheelMove(event) {
        if (event.ctrlKey || event.metaKey) {
            event.preventDefault();
            this.handleZoom(event);
        }
    }

    touchStart(event) {
        if (event.touches.length === 2) {
            this.touches = [...event.touches];
        }
    }

    touchMove(event) {
        if (event.touches.length === 2) {
            event.preventDefault();
            const newTouches = [...event.touches];
            const oldDistance = this.getTouchDistance(this.touches[0], this.touches[1]);
            const newDistance = this.getTouchDistance(newTouches[0], newTouches[1]);

            if (newDistance > oldDistance) {
                this.zoomIn();
            } else if (newDistance < oldDistance) {
                this.zoomOut();
            }

            this.touches = newTouches;
        }
    }

    touchEnd() {
        this.touches = [];
    }

    getTouchDistance(touch1, touch2) {
        const dx = touch2.clientX - touch1.clientX;
        const dy = touch2.clientY - touch1.clientY;
        return Math.sqrt(dx * dx + dy * dy);
    }
}

export { ImageController };
