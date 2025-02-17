import { Utils } from './utils.js';

class Renderers {
    
    static async videoCards(videoData) {
        const container = document.getElementById('video-cards-box');
        container.innerHTML = '';

        const templateHTML = await Utils.fetchHTML('video-card.html');

        for (const data of videoData) {
            const parser = new DOMParser();
            const doc = parser.parseFromString(templateHTML, 'text/html');
            const videoCard = doc.body.firstChild.cloneNode(true);

            videoCard.querySelector('.video-thumbnail').src = data.thumbnail;
            videoCard.querySelector('.duration-time').textContent = data.duration;
            videoCard.querySelector('.video-title-box p').textContent = data.title;
            videoCard.querySelector('.video-stats-box p')
                .textContent = `${data.channel_name} • ${data.view_count}`;

            if (['<not-allowed>', '<not-valid>'].includes(data.error_code)) {
                const addCartBtn = videoCard.querySelector('.add-cart-btn');
                addCartBtn.disabled = true;
            }

            container.appendChild(videoCard);
        }
    }

    static async loadingVideoCards(numberOfCards) {
        const container = document.getElementById('video-cards-box');
        container.innerHTML = '';

        const templateHTML = await Utils.fetchHTML('loading-video-card.html');

        for (let i = 0; i < numberOfCards; i++) {
            const parser = new DOMParser();
            const doc = parser.parseFromString(templateHTML, 'text/html');
            const loadingVideoCard = doc.body.firstChild.cloneNode(true);

            container.appendChild(loadingVideoCard);
        }
    }

    static cartMenu() {
        const cartMenuElement = document.getElementById('cart-menu');
        cartMenuElement.style.right = '0'
    }

    static filterDropdownMenu() {
        const dropdownMenu = document.getElementById('filter-dropdown-menu');
        const menuBtn = document.getElementById('filter-menu-btn');
        const menuBtnPosition = menuBtn.getBoundingClientRect();

        menuBtn.classList.add('open');
        dropdownMenu.style.display = 'block'
        dropdownMenu.style.top = `${menuBtnPosition.bottom + 2 + window.scrollY}px`;
        dropdownMenu.style.left = `${menuBtnPosition.right - 140}px`;
        dropdownMenu.style.opacity = '1';
    }

    static loadingScreen() {
        const loadingScreenElement = document.getElementById('loading-screen');
    
        loadingScreenElement.style.display = 'block'
        loadingScreenElement.style.opacity = '1';    
    }

    static errorWarning(message) {
        const errorWarningElement = document.getElementById('error-warning');
        const errorWarningMessage = document.querySelector('#error-warning > p');

        errorWarningMessage.textContent = message
        errorWarningElement.style.top = '20px'
    }

    static successWarning(message) {
        const successWarningElement = document.getElementById('success-warning');
        const successWarningMessage = document.querySelector('#success-warning > p');

        successWarningMessage.textContent = message
        successWarningElement.style.top = '20px'
    }

}

export { Renderers };
