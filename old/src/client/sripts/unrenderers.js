class Unrenderers {

    static cartMenu() {
        const cartMenuElement = document.getElementById('cart-menu');
        cartMenuElement.style.right = '-50vw'
    }

    static filterDropdownMenu() {
        const menuBtn = document.getElementById('filter-menu-btn');
        const dropdownMenu = document.getElementById('filter-dropdown-menu');
        
        menuBtn.classList.remove('open');
        dropdownMenu.style.opacity = '0';
        setTimeout(() => {
            dropdownMenu.style.display = 'none';
        }, 500);
    }

    static loadingScreen() {
        const loadingScreenElement = document.getElementById('loading-screen');
    
        loadingScreenElement.style.opacity = '0';    
        setTimeout(() => {
            loadingScreenElement.style.display = 'none';
        }, 500); 
    }
    
    static errorWarning() {
        const errorWarningElement = document.getElementById('error-warning');

        errorWarningElement.style.display = 'none'
        errorWarningElement.style.top = '20px'
    }

    static successWarning() {
        const successWarningElement = document.getElementById('error-warning');

        successWarningElement.style.display = 'none'
        successWarningElement.style.top = '20px'
    }
}

export { Unrenderers };
