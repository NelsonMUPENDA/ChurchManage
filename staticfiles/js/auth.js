/**
 * Auth Module - Gestion de l'authentification
 * Remplace le AuthProvider React par un module JavaScript natif
 */

(function() {
    'use strict';

    // État de l'authentification
    const AuthState = {
        user: null,
        loading: true,
        isAuthenticated: false
    };

    // Écouteurs d'événements
    const listeners = new Set();

    function subscribe(callback) {
        listeners.add(callback);
        return () => listeners.delete(callback);
    }

    function notifyListeners() {
        listeners.forEach(callback => {
            try {
                callback({ ...AuthState });
            } catch (e) {
                console.error('Auth listener error:', e);
            }
        });
    }

    function setState(newState) {
        Object.assign(AuthState, newState);
        notifyListeners();
    }

    // Récupérer les infos utilisateur
    async function refreshMe() {
        const token = window.API.TokenStorage.getAccess();
        if (!token) {
            setState({ user: null, isAuthenticated: false, loading: false });
            return null;
        }

        try {
            const me = await window.API.apiMe();
            setState({ user: me, isAuthenticated: true, loading: false });
            return me;
        } catch (error) {
            window.API.TokenStorage.clear();
            setState({ user: null, isAuthenticated: false, loading: false });
            return null;
        }
    }

    // Connexion
    async function login({ username, password }) {
        try {
            const tokens = await window.API.apiLogin(username, password);
            await refreshMe();
            return true;
        } catch (error) {
            throw error;
        }
    }

    // Déconnexion
    function logout() {
        window.API.TokenStorage.clear();
        setState({ user: null, isAuthenticated: false, loading: false });
        window.location.href = '/login/';
    }

    // Récupérer le rôle utilisateur
    function getUserRole() {
        const user = AuthState.user;
        if (!user) return null;
        
        if (user.is_superuser) return 'super_admin';
        if (user.is_staff) return 'admin';
        return user.role;
    }

    // Vérifications de rôle
    function isAdmin() {
        const role = getUserRole();
        return role === 'admin' || role === 'super_admin';
    }

    function isTreasurer() {
        const role = getUserRole();
        return role === 'treasurer' || role === 'financial_head';
    }

    function isSecretary() {
        const role = getUserRole();
        const deptName = (AuthState.user?.department_name || '').toLowerCase();
        const isProtocolDeptHead = role === 'department_head' && 
            (deptName.includes('protoc') || deptName.includes('protocol'));
        return role === 'secretary' || role === 'protocol_head' || isProtocolDeptHead;
    }

    function isLogisticsHead() {
        const role = getUserRole();
        const deptName = (AuthState.user?.department_name || '').toLowerCase();
        const isProtocolDeptHead = role === 'department_head' && 
            (deptName.includes('protoc') || deptName.includes('protocol'));
        return (role === 'logistics_head' || 
            (role === 'department_head' && deptName.includes('logist'))) && 
            !isProtocolDeptHead;
    }

    function isEvangelismHead() {
        const role = getUserRole();
        const deptName = (AuthState.user?.department_name || '').toLowerCase();
        return role === 'evangelism_head' || 
            (role === 'department_head' && (deptName.includes('evang') || deptName.includes('évang')));
    }

    // Déterminer la page d'accueil selon le rôle
    function getHomePath() {
        if (isAdmin()) return '/dashboard/';
        if (isSecretary()) return '/diaconat/?tab=pointage';
        if (isLogisticsHead()) return '/diaconat/?tab=logistique';
        if (isTreasurer()) return '/finances/';
        if (isEvangelismHead()) return '/evangelisation/';
        return '/events/';
    }

    // Initialisation
    async function init() {
        await refreshMe();
    }

    // Export global
    window.Auth = {
        state: AuthState,
        subscribe,
        login,
        logout,
        refreshMe,
        getUserRole,
        isAdmin,
        isTreasurer,
        isSecretary,
        isLogisticsHead,
        isEvangelismHead,
        getHomePath,
        init
    };

    // Auto-initialisation
    document.addEventListener('DOMContentLoaded', init);
})();
