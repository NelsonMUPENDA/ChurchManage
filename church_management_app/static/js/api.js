/**
 * API Client - Remplacement d'Axios par fetch()
 * Gère les appels API vers le backend Django avec authentification JWT
 */

console.log('🚀 api.js starting execution...');

const DEFAULT_API_BASE_URL = 'http://localhost:8000';

// Détection automatique de l'URL de l'API
function getBaseUrl() {
    // Vérifier si une variable globale API_BASE_URL existe (définie via template)
    const envUrl = (typeof window.API_BASE_URL !== 'undefined') ? window.API_BASE_URL : null;
    const detectedHost = window.location.hostname !== 'localhost' 
        ? `http://${window.location.hostname}:8000` 
        : DEFAULT_API_BASE_URL;
    return envUrl || detectedHost;
}

const API_BASE_URL = getBaseUrl();

// Stockage des tokens
const TOKEN_KEYS = {
    access: 'cpd_access_token',
    refresh: 'cpd_refresh_token'
};

const TokenStorage = {
    getAccess() {
        return localStorage.getItem(TOKEN_KEYS.access);
    },
    getRefresh() {
        return localStorage.getItem(TOKEN_KEYS.refresh);
    },
    set({ access, refresh }) {
        if (access) localStorage.setItem(TOKEN_KEYS.access, access);
        if (refresh) localStorage.setItem(TOKEN_KEYS.refresh, refresh);
    },
    clear() {
        localStorage.removeItem(TOKEN_KEYS.access);
        localStorage.removeItem(TOKEN_KEYS.refresh);
    }
};

// Gestion du rafraîchissement de token
let isRefreshing = false;
let refreshSubscribers = [];

function subscribeTokenRefresh(callback) {
    refreshSubscribers.push(callback);
}

function onTokenRefreshed(newToken) {
    refreshSubscribers.forEach(cb => cb(newToken));
    refreshSubscribers = [];
}

async function refreshAccessToken() {
    const refresh = TokenStorage.getRefresh();
    if (!refresh) {
        TokenStorage.clear();
        throw new Error('No refresh token');
    }

    try {
        const response = await fetch(`${API_BASE_URL}/api/auth/token/refresh/`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ refresh })
        });

        if (!response.ok) throw new Error('Refresh failed');

        const data = await response.json();
        TokenStorage.set({ access: data.access, refresh });
        return data.access;
    } catch (error) {
        TokenStorage.clear();
        throw error;
    }
}

// Fonction fetch avec gestion JWT
async function apiFetch(url, options = {}) {
    const fullUrl = url.startsWith('http') ? url : `${API_BASE_URL}${url}`;
    
    // Headers par défaut
    const headers = {
        'Content-Type': 'application/json',
        ...options.headers
    };

    // Ajout du token d'accès
    const token = TokenStorage.getAccess();
    if (token) {
        headers.Authorization = `Bearer ${token}`;
    }

    // Gestion du CSRF pour les requêtes non-GET
    if (options.method && options.method !== 'GET') {
        const csrfToken = getCsrfToken();
        if (csrfToken) {
            headers['X-CSRFToken'] = csrfToken;
        }
    }

    try {
        let response = await fetch(fullUrl, {
            ...options,
            headers
        });

        // Gestion du 401 - Token expiré
        if (response.status === 401 && !options._retry) {
            if (isRefreshing) {
                // Attendre que le rafraîchissement soit terminé
                const newToken = await new Promise((resolve, reject) => {
                    subscribeTokenRefresh(token => {
                        if (token) resolve(token);
                        else reject(new Error('Refresh failed'));
                    });
                });
                
                headers.Authorization = `Bearer ${newToken}`;
                response = await fetch(fullUrl, {
                    ...options,
                    headers,
                    _retry: true
                });
            } else {
                isRefreshing = true;
                try {
                    const newToken = await refreshAccessToken();
                    onTokenRefreshed(newToken);
                    
                    headers.Authorization = `Bearer ${newToken}`;
                    response = await fetch(fullUrl, {
                        ...options,
                        headers,
                        _retry: true
                    });
                } catch (refreshError) {
                    onTokenRefreshed(null);
                    window.location.href = '/login.html';
                    throw refreshError;
                } finally {
                    isRefreshing = false;
                }
            }
        }

        if (!response.ok) {
            const error = new Error(`HTTP ${response.status}`);
            error.response = response;
            try {
                error.data = await response.json();
            } catch {
                error.data = null;
            }
            throw error;
        }

        // Retourner null pour les 204 No Content
        if (response.status === 204) {
            return null;
        }

        return await response.json();
    } catch (error) {
        if (!error.response && error.message === 'Failed to fetch') {
            const networkError = new Error('Network Error');
            networkError.code = 'ERR_NETWORK';
            throw networkError;
        }
        throw error;
    }
}

// Récupération du token CSRF Django
function getCsrfToken() {
    const name = 'csrftoken';
    const cookies = document.cookie.split(';');
    for (let cookie of cookies) {
        const [cookieName, cookieValue] = cookie.trim().split('=');
        if (cookieName === name) {
            return decodeURIComponent(cookieValue);
        }
    }
    return null;
}

// Méthodes HTTP simplifiées
const api = {
    get: (url, params = {}) => {
        const queryString = new URLSearchParams(params).toString();
        const fullUrl = queryString ? `${url}?${queryString}` : url;
        return apiFetch(fullUrl, { method: 'GET' });
    },
    
    post: (url, data) => apiFetch(url, {
        method: 'POST',
        body: JSON.stringify(data)
    }),
    
    put: (url, data) => apiFetch(url, {
        method: 'PUT',
        body: JSON.stringify(data)
    }),
    
    patch: (url, data) => apiFetch(url, {
        method: 'PATCH',
        body: JSON.stringify(data)
    }),
    
    delete: (url) => apiFetch(url, { method: 'DELETE' })
};

// Authentification
async function apiLogin(username, password) {
    const response = await fetch(`${API_BASE_URL}/api/auth/token/`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username, password })
    });

    if (!response.ok) {
        const error = new Error('Login failed');
        error.response = response;
        try {
            error.data = await response.json();
        } catch {
            error.data = null;
        }
        throw error;
    }

    const data = await response.json();
    TokenStorage.set(data);
    return data;
}

async function apiMe() {
    return api.get('/api/me/');
}

// Export global
window.API = {
    baseUrl: API_BASE_URL,
    api,
    apiLogin,
    apiMe,
    TokenStorage
};

console.log('✅ api.js loaded, window.API:', window.API);
