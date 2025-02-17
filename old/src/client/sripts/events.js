import { HttpService } from './HTTPService.js';
import { Paths } from './paths.js';
import { Renderers } from './renderers.js';
import { RequestHandler } from './requestHandles.js';
import { Unrenderers } from './unrenderers.js';
import { Utils } from './utils.js';



// -- Elements --
const searchInput = document.getElementById('search-input');
const searchBtn = document.getElementById('search-btn');
const openCartMenuBtn = document.getElementById('open-cart-menu-btn');
const closeCartMenuBtn = document.getElementById('close-cart-menu-btn');
const filterMenuBtn = document.getElementById('filter-menu-btn');
const filterDropdownMenu = document.getElementById('filter-dropdown-menu');

// -- Functions -- 
async function setupPage() {
    let itsAllOk = false;

    Utils.saveCookie(
        'userTag', Utils.generateUserTag(), Utils.getForeverDate()
    );
    const userTag = Utils.getCookies().userTag;

    const timeout = setTimeout(() => {
        if (!itsAllOk) {
            Renderers.errorWarning(
                'Internal Server Error: Please refresh your page or try again later!'
            );
        }
    }, 8000);
    
    const configData = await Utils.getDataFromJson(Paths.CONFIG + 'config.json');
    const heartbeat = setInterval(() => {
        RequestHandler.heartbeat(userTag)
    }, configData.heartbeatInterval * 1000);

    try {
        const userLocation = await Utils.getUserLocation();
        const userData = await RequestHandler.getUserData(userTag);
        console.log(userData)
        if (!userData) {
            itsAllOk = await RequestHandler.saveUserData(
                userTag, userLocation.city, userLocation.region, userLocation.country
            );
        } else {
            itsAllOk = true;
        }

        if (itsAllOk) {
            clearTimeout(timeout);
            setTimeout(Unrenderers.loadingScreen, 1000);
            Unrenderers.errorWarning();
        }
    } catch (error) {
        console.error('Error in UserDetector:', error);
        Renderers.errorWarning(
            'An unexpected error occurred. Please try again later.'
        );
    }

    RequestHandler.saveAccess(userTag);
}


function performSearch() {
    const userTag = Utils.getCookies().userTag;
    const searchQuery = searchInput.value;
    const maxResultsFilter = document.getElementById('max-results-filter').value;

    RequestHandler.search(
        userTag,
        searchQuery,
        maxResultsFilter
    );
}

function openCartMenu() {
    Renderers.cartMenu();
}

function closeCartMenu() {
    Unrenderers.cartMenu();
}

function toggleFilterMenu() {
    if (filterMenuBtn.classList.contains('open')) {
        Unrenderers.filterDropdownMenu();
    } else {
        Renderers.filterDropdownMenu();
    }
}

function closeMenuOnClickOutside(event) {
    if (!filterMenuBtn.contains(event.target) && !filterDropdownMenu.contains(event.target)) {
        Unrenderers.filterDropdownMenu();
    }
}

function executeOnEnter(event) {
    if (event.key === 'Enter') {
        event.preventDefault();
        Unrenderers.filterDropdownMenu();
        performSearch();
    }
}

function closeMenuOnScroll() {
    Unrenderers.cartMenu();
    Unrenderers.filterDropdownMenu();
}

// -- Event Listeners --
document.addEventListener('DOMContentLoaded', setupPage);
document.addEventListener('scroll', closeMenuOnScroll);
document.addEventListener('keydown', executeOnEnter);
document.addEventListener('click', closeMenuOnClickOutside);

searchBtn.addEventListener('click', performSearch);
openCartMenuBtn.addEventListener('click', openCartMenu);
closeCartMenuBtn.addEventListener('click', closeCartMenu);
filterMenuBtn.addEventListener('click', toggleFilterMenu);
