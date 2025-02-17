import { HttpService } from './HTTPService.js';
import { Renderers } from './renderers.js';
import { Utils } from './utils.js';


class RequestHandler {
    
    static async search(userTag, query, maxResults) {

        if (!query.trim()) {
            console.log('Search query is empty!');
            return;
        }
        
        maxResults = Math.min(Math.max(parseInt(maxResults), 1), 100);
        const numberOfCards = Utils.isURL(query) ? 1 : maxResults;
        Renderers.loadingVideoCards(numberOfCards);

        const requestData = await HttpService.request(
            `user/${userTag}/search`, 'GET', { query, maxResults }
        );
        Renderers.videoCards(requestData.results);
    }

    static async getUserData(userTag) {
        const userData = await HttpService.request(
            `/user/${userTag}/data`, 'GET' 
        );
        return userData;
    }

    static async saveUserData(tag, city, region, country) {
        const response = await HttpService.request(
            `/user/${tag}/data`, 
            'POST', 
            {
                city: city,
                region: region,
                country: country
            }
        )
        return response.isSaved;
    }

    static async heartbeat(userTag) {
        const response = await HttpService.request(
            `/user/${userTag}/heartbeat`, 'PATCH'
        )
        return response;
    }

    static async saveAccess(userTag) {
        const response = await HttpService.request(
            `/user/${userTag}/heartbeat`, 'POST'
        )
        return response;
    }
}

export { RequestHandler };
