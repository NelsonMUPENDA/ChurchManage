/**
 * Utils Module - Fonctions utilitaires communes
 */

(function() {
    'use strict';

    // Formatage des dates
    function formatDate(date, options = {}) {
        const d = new Date(date);
        if (isNaN(d.getTime())) return '—';
        
        const opts = {
            year: 'numeric',
            month: 'long',
            day: 'numeric',
            ...options
        };
        return new Intl.DateTimeFormat('fr-FR', opts).format(d);
    }

    function formatDateShort(date) {
        const d = new Date(date);
        if (isNaN(d.getTime())) return '—';
        return new Intl.DateTimeFormat('fr-FR', { 
            day: '2-digit', 
            month: 'short', 
            year: 'numeric' 
        }).format(d);
    }

    function formatDateTime(date) {
        const d = new Date(date);
        if (isNaN(d.getTime())) return '—';
        return new Intl.DateTimeFormat('fr-FR', { 
            day: '2-digit', 
            month: 'short', 
            year: 'numeric',
            hour: '2-digit',
            minute: '2-digit'
        }).format(d);
    }

    // Time ago
    function timeAgo(iso) {
        if (!iso) return '';
        const dt = new Date(iso);
        if (isNaN(dt.getTime())) return '';
        
        const diffMs = Date.now() - dt.getTime();
        const sec = Math.max(0, Math.floor(diffMs / 1000));
        
        if (sec < 60) return "À l'instant";
        const min = Math.floor(sec / 60);
        if (min < 60) return `Il y a ${min} min`;
        const hr = Math.floor(min / 60);
        if (hr < 24) return `Il y a ${hr} heures`;
        const day = Math.floor(hr / 24);
        return `Il y a ${day} jours`;
    }

    // Formatage des nombres
    function formatNumber(num, decimals = 0) {
        const n = Number(num);
        if (isNaN(n)) return '—';
        return new Intl.NumberFormat('fr-FR', {
            minimumFractionDigits: decimals,
            maximumFractionDigits: decimals
        }).format(n);
    }

    function formatCurrency(amount, currency = 'CDF') {
        const n = Number(amount);
        if (isNaN(n)) return '—';
        return `${currency} ${formatNumber(n, 2)}`;
    }

    // Échappement HTML
    function escapeHtml(text) {
        if (!text) return '';
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }

    // Gestion des paramètres URL
    function getUrlParams() {
        const params = new URLSearchParams(window.location.search);
        const result = {};
        for (const [key, value] of params) {
            result[key] = value;
        }
        return result;
    }

    function setUrlParam(key, value) {
        const url = new URL(window.location);
        if (value === null || value === undefined) {
            url.searchParams.delete(key);
        } else {
            url.searchParams.set(key, value);
        }
        window.history.pushState({}, '', url);
    }

    // Debounce
    function debounce(fn, delay) {
        let timeoutId;
        return function(...args) {
            clearTimeout(timeoutId);
            timeoutId = setTimeout(() => fn.apply(this, args), delay);
        };
    }

    // Throttle
    function throttle(fn, limit) {
        let inThrottle;
        return function(...args) {
            if (!inThrottle) {
                fn.apply(this, args);
                inThrottle = true;
                setTimeout(() => inThrottle = false, limit);
            }
        };
    }

    // Validation
    function isValidEmail(email) {
        return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
    }

    function isValidPhone(phone) {
        return /^[\d\s\+\-\(\)]{8,}$/.test(phone);
    }

    // Stockage local avec fallback
    const Storage = {
        get(key, defaultValue = null) {
            try {
                const item = localStorage.getItem(key);
                return item ? JSON.parse(item) : defaultValue;
            } catch {
                return defaultValue;
            }
        },
        set(key, value) {
            try {
                localStorage.setItem(key, JSON.stringify(value));
                return true;
            } catch {
                return false;
            }
        },
        remove(key) {
            try {
                localStorage.removeItem(key);
                return true;
            } catch {
                return false;
            }
        }
    };

    // Gestion du thème
    const Theme = {
        get() {
            const saved = Storage.get('cpd_theme');
            if (saved) return saved;
            return window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
        },
        set(theme) {
            Storage.set('cpd_theme', theme);
            document.documentElement.setAttribute('data-bs-theme', theme);
            if (theme === 'dark') {
                document.body.classList.add('dark');
            } else {
                document.body.classList.remove('dark');
            }
        },
        toggle() {
            const current = this.get();
            const next = current === 'dark' ? 'light' : 'dark';
            this.set(next);
            return next;
        },
        init() {
            this.set(this.get());
        }
    };

    // Export global
    window.Utils = {
        formatDate,
        formatDateShort,
        formatDateTime,
        timeAgo,
        formatNumber,
        formatCurrency,
        escapeHtml,
        getUrlParams,
        setUrlParam,
        debounce,
        throttle,
        isValidEmail,
        isValidPhone,
        Storage,
        Theme
    };

    // Note: Theme initialization is handled in the page templates, not here
    // to allow each page to set its own default theme
})();
