class HttpService {

    static async request(endpoint, method, requestBody = null) {
        try {
            const url = this.buildUrl(endpoint, method, requestBody);
            const options = this.buildOptions(method, requestBody);
            
            const response = await fetch(url, options);
    
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
    
            return await response.json();

        } catch (error) {
            console.error('Error while fetching data:', error);
        }
    }

    static buildUrl(endpoint, method, requestBody) {
        let url = `http://127.0.0.1:5000/${endpoint}`;

        if (method === 'GET' && requestBody) {
            const queryParams = new URLSearchParams(requestBody).toString();
            url += `?${queryParams}`;
        }

        return url;
    }

    static buildOptions(method, requestBody) {
        const options = {
            method: method,
            headers: { 'Content-Type': 'application/json' }
        };

        if (method !== 'GET' && requestBody) {
            options.body = JSON.stringify(requestBody);
        }

        return options;
    }
}

export { HttpService };
