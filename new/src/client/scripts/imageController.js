class ImageController {
    constructor(image, scale = 1, minScale = 0.25, maxScale = 5, stepScale = 0.1) {
        this.image = image;
        this.scale = scale;
        this.minScale = minScale;
        this.maxScale = maxScale;
        this.stepScale = stepScale;
        this.isDragging = false;
        this.position = { x: 0, y: 0 };
        this.touches = [];
    }

    initScrollZoom() {
        document.addEventListener('wheel', (event) => {
            if (event.ctrlKey || event.metaKey) {
                this.handleZoom(event);
            }
        });
    }

    initPinchZoom() {
        document.addEventListener('touchstart', (event) => this.handleTouchStart(event), { passive: false });
        document.addEventListener('touchmove', (event) => this.handleTouchMove(event), { passive: false });
        document.addEventListener('touchend', () => this.handleTouchEnd());
    }

    zoomIn() {
        this.scale = this.clampScale(this.scale + this.stepScale);
        this.applyTransform();
    }

    zoomOut() {
        this.scale = this.clampScale(this.scale - this.stepScale);
        this.applyTransform();
    }

    clampScale(scale) {
        return Math.min(Math.max(scale, this.minScale), this.maxScale);
    }

    applyTransform() {
        this.image.style.transform = `scale(${this.scale})`;
    }

    handleZoom(event) {
        event.preventDefault();
        if (event.deltaY < 0) {
            this.zoomIn();
        } else {
            this.zoomOut();
        }
    }

    handleTouchStart(event) {
        if (event.touches.length === 2) {
            this.touches = [...event.touches];
        }
    }

    handleTouchMove(event) {
        if (event.touches.length === 2) {
            event.preventDefault();
            const newTouches = [...event.touches];
            const oldDistance = this.getDistance(this.touches[0], this.touches[1]);
            const newDistance = this.getDistance(newTouches[0], newTouches[1]);

            if (newDistance > oldDistance) {
                this.zoomIn();
            } else if (newDistance < oldDistance) {
                this.zoomOut();
            }

            this.touches = newTouches;
        }
    }
melhorar idsooooo
    handleTouchEnd() {
        this.touches = [];
    }

    getDistance(touch1, touch2) {
        const dx = touch2.clientX - touch1.clientX;
        const dy = touch2.clientY - touch1.clientY;
        return Math.sqrt(dx * dx + dy * dy);
    }
}

export { ImageController };
