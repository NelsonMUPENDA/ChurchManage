// api.js - Client API centralisé
const API = {
    baseURL: '',
    
    getAuthHeaders(method = 'GET') {
        const token = localStorage.getItem('token');
        const headers = {
            'Content-Type': 'application/json'
        };
        
        // CSRF token uniquement pour les méthodes non sûres
        const unsafeMethods = ['POST', 'PUT', 'PATCH', 'DELETE'];
        if (unsafeMethods.includes(method.toUpperCase())) {
            const csrfToken = this.getCSRFToken();
            if (csrfToken) {
                headers['X-CSRFToken'] = csrfToken;
            }
        }
        
        if (token) {
            headers['Authorization'] = `Token ${token}`;
        }
        return headers;
    },
    
    getCSRFToken() {
        const name = 'csrftoken';
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue || '';
    },
    
    async request(endpoint, options = {}) {
        const url = endpoint.startsWith('http') ? endpoint : `${this.baseURL}${endpoint}`;
        const method = options.method || 'GET';
        const defaultOptions = {
            headers: this.getAuthHeaders(method),
            credentials: 'same-origin'
        };
        
        const response = await fetch(url, { ...defaultOptions, ...options });
        
        if (!response.ok) {
            const error = await response.json().catch(() => ({}));
            throw new Error(error.detail || error.message || `HTTP ${response.status}`);
        }
        
        if (response.status === 204) return null;
        return response.json();
    },
    
    api: {
        get: (endpoint, params = {}) => {
            const queryString = new URLSearchParams(params).toString();
            const url = queryString ? `${endpoint}?${queryString}` : endpoint;
            return API.request(url, { method: 'GET' });
        },
        
        post: (endpoint, data) => {
            return API.request(endpoint, {
                method: 'POST',
                body: JSON.stringify(data)
            });
        },
        
        patch: (endpoint, data) => {
            return API.request(endpoint, {
                method: 'PATCH',
                body: JSON.stringify(data)
            });
        },
        
        put: (endpoint, data) => {
            return API.request(endpoint, {
                method: 'PUT',
                body: JSON.stringify(data)
            });
        },
        
        delete: (endpoint) => {
            return API.request(endpoint, { method: 'DELETE' });
        }
    }
};
