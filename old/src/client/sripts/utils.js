class Utils {
    
    static async fetchHTML(url) {
        const response = await fetch(url);
        return await response.text();
    }

    static async getUserLocation() {
        const defaultData = {
            city: 'unknown',
            region: 'unknown',
            country: 'unknown'
        };
    
        try {
            const response = await fetch('http://ip-api.com/json');
            const data = await response.json();
    
            const location = {
                city: data.city || defaultData.city,
                region: data.region || defaultData.region,
                country: data.country || defaultData.country
            };
    
            return location;
        } catch (error) {
            console.error('Error getting location:', error);
            return defaultData;
        }
    }    

    static generateUserTag() {
        let randomTag = Math.random().toString(36).slice(2, 20);

        randomTag = randomTag.split('').map(char => 
            Math.random() > 0.5 ? char.toUpperCase() : char
        ).join('');

        return `user_${randomTag}`;
    }

    static getCookies() {
        if (!document.cookie) {
            return null;
        }
        
        const cookies = {};
        for (const cookie of document.cookie.split('; ')) {
            const [name, value] = cookie.split('=');
            cookies[name] = value;
        }
        return cookies;
    }
    
    static saveCookie(name, value, expires, path = '/', override = false) {
        const cookies = Utils.getCookies();

        if (override || !cookies) {
            document.cookie = `${name}=${value}; expires=${expires}; path=${path}`;
        }
    }

    static isURL(url) {
        return url.includes('https://')
    } 

    static getForeverDate() {
        const now = new Date();
        now.setFullYear(now.getFullYear() + 1000);
        
        return now.toUTCString()
    }

    static async getDataFromJson(path) {
        try {
            const response = await fetch(path);
            const data = await response.json();
            return data;
        } catch (error) {
            console.error('Error getting data from JSON:', error);
        }
    }
}

export { Utils };
