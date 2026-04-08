/**
 * Toast/Notification System - Remplace ToastProvider React
 * Affiche des notifications toast en JavaScript natif
 */

(function() {
    'use strict';

    // Container pour les toasts
    let toastContainer = null;

    function ensureContainer() {
        if (!toastContainer) {
            toastContainer = document.createElement('div');
            toastContainer.id = 'toast-container';
            toastContainer.style.cssText = `
                position: fixed;
                top: 20px;
                right: 20px;
                z-index: 9999;
                display: flex;
                flex-direction: column;
                gap: 10px;
                max-width: 400px;
            `;
            document.body.appendChild(toastContainer);
        }
        return toastContainer;
    }

    // Types de toasts avec styles
    const toastTypes = {
        success: {
            icon: '✓',
            className: 'toast-success',
            bgClass: 'bg-success',
            textClass: 'text-white'
        },
        error: {
            icon: '✕',
            className: 'toast-error',
            bgClass: 'bg-danger',
            textClass: 'text-white'
        },
        warning: {
            icon: '⚠',
            className: 'toast-warning',
            bgClass: 'bg-warning',
            textClass: 'text-dark'
        },
        info: {
            icon: 'ℹ',
            className: 'toast-info',
            bgClass: 'bg-info',
            textClass: 'text-white'
        }
    };

    function push({ type = 'info', title = '', message = '', duration = 5000 }) {
        const container = ensureContainer();
        const config = toastTypes[type] || toastTypes.info;

        // Créer l'élément toast
        const toast = document.createElement('div');
        toast.className = `toast align-items-center ${config.bgClass} ${config.textClass} border-0 show`;
        toast.setAttribute('role', 'alert');
        toast.style.cssText = `
            min-width: 300px;
            opacity: 0;
            transform: translateX(100%);
            transition: all 0.3s ease;
        `;

        toast.innerHTML = `
            <div class="d-flex">
                <div class="toast-body">
                    <div class="d-flex align-items-center gap-2">
                        <span class="fs-5">${config.icon}</span>
                        <div>
                            ${title ? `<strong class="d-block">${escapeHtml(title)}</strong>` : ''}
                            ${message ? `<span>${escapeHtml(message)}</span>` : ''}
                        </div>
                    </div>
                </div>
                <button type="button" class="btn-close btn-close-white me-2 m-auto ${config.textClass === 'text-dark' ? 'btn-close-dark' : ''}" 
                        data-bs-dismiss="toast" aria-label="Close"></button>
            </div>
        `;

        // Gestionnaire de fermeture
        const closeBtn = toast.querySelector('.btn-close');
        closeBtn.addEventListener('click', () => removeToast(toast));

        container.appendChild(toast);

        // Animation d'entrée
        requestAnimationFrame(() => {
            toast.style.opacity = '1';
            toast.style.transform = 'translateX(0)';
        });

        // Auto-fermeture
        if (duration > 0) {
            setTimeout(() => removeToast(toast), duration);
        }

        return toast;
    }

    function removeToast(toast) {
        toast.style.opacity = '0';
        toast.style.transform = 'translateX(100%)';
        setTimeout(() => {
            toast.remove();
            // Nettoyer le container s'il est vide
            if (toastContainer && toastContainer.children.length === 0) {
                toastContainer.remove();
                toastContainer = null;
            }
        }, 300);
    }

    function escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }

    // Méthodes pratiques
    function success(title, message, duration) {
        return push({ type: 'success', title, message, duration });
    }

    function error(title, message, duration) {
        return push({ type: 'error', title, message, duration });
    }

    function warning(title, message, duration) {
        return push({ type: 'warning', title, message, duration });
    }

    function info(title, message, duration) {
        return push({ type: 'info', title, message, duration });
    }

    // Export global
    window.Toast = {
        push,
        success,
        error,
        warning,
        info
    };
})();
