// auth.js - Gestion de l'authentification
const Auth = {
    state: {
        isAuthenticated: false,
        user: null,
        token: null
    },
    
    init() {
        const token = localStorage.getItem('token');
        const user = localStorage.getItem('user');
        if (token && user) {
            this.state.token = token;
            this.state.user = JSON.parse(user);
            this.state.isAuthenticated = true;
        }
    },
    
    async login(username, password) {
        try {
            const response = await fetch('/api/auth/login/', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ username, password })
            });
            
            if (!response.ok) throw new Error('Login failed');
            
            const data = await response.json();
            this.state.token = data.token;
            this.state.user = data.user;
            this.state.isAuthenticated = true;
            
            localStorage.setItem('token', data.token);
            localStorage.setItem('user', JSON.stringify(data.user));
            
            return data;
        } catch (error) {
            console.error('Login error:', error);
            throw error;
        }
    },
    
    async refreshMe() {
        try {
            // Essayer de récupérer l'utilisateur actuel via session
            const response = await fetch('/api/auth/me/', {
                credentials: 'same-origin',
                headers: { 'X-CSRFToken': this.getCSRFToken() }
            });
            
            if (response.ok) {
                const user = await response.json();
                this.state.user = user;
                this.state.isAuthenticated = true;
                localStorage.setItem('user', JSON.stringify(user));
                return user;
            } else if (response.status === 403 || response.status === 401) {
                // Non authentifié
                this.state.isAuthenticated = false;
            }
        } catch (error) {
            console.log('Auth check error:', error);
        }
        return null;
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
        return cookieValue;
    },
    
    logout() {
        this.state.token = null;
        this.state.user = null;
        this.state.isAuthenticated = false;
        localStorage.removeItem('token');
        localStorage.removeItem('user');
        window.location.href = '/login/';
    },
    
    isAdmin() {
        if (!this.state.user) return false;
        const adminRoles = ['super_admin', 'admin', 'pastor', 'administrator'];
        return adminRoles.includes(this.state.user.role);
    },
    
    getUser() {
        return this.state.user;
    }
};

// Initialiser au chargement
Auth.init();
