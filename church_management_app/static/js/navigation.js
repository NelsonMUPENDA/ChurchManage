/**
 * Navigation Module - Génération de la navigation dynamique
 * Remplace la logique de navigation React par du JavaScript natif
 */

(function() {
    'use strict';

    // Configuration des éléments de navigation par groupe
    const NAV_GROUPS = {
        'Général': [
            { to: '/dashboard/', icon: 'bi-house', label: 'Tableau de bord', color: 'indigo', sticker: 'LIVE', stickerVariant: 'cpd-sticker-gospel' }
        ],
        'Communauté': [
            { to: '/members/', icon: 'bi-people', label: 'Membres', color: 'blue', sticker: 'PROFILS', stickerVariant: 'cpd-sticker-gospel' }
        ],
        'Activités': [
            { to: '/events/', icon: 'bi-calendar-event', label: 'Programmes & Activités', color: 'green', sticker: 'PLAN', stickerVariant: 'cpd-sticker-gold' },
            { to: '/diaconat/', icon: 'bi-clipboard-check', label: 'Diaconat', color: 'indigo', sticker: 'SERVICE', stickerVariant: 'cpd-sticker' },
            { to: '/evangelisation/', icon: 'bi-megaphone', label: 'Évangélisation', color: 'green', sticker: 'GOSPEL', stickerVariant: 'cpd-sticker-gospel' },
            { to: '/mariage/', icon: 'bi-heart', label: 'Mariage', color: 'purple', sticker: 'AMOUR', stickerVariant: 'cpd-sticker-gold' }
        ],
        'Administration': [
            { to: '/users/', icon: 'bi-person-gear', label: 'Utilisateurs', color: 'indigo' },
            { to: '/audit-logs/', icon: 'bi-journal-text', label: 'Journaux', color: 'indigo' }
        ],
        'Communication': [
            { to: '/announcements/', icon: 'bi-megaphone', label: 'Annonces', color: 'purple', sticker: 'ACTU', stickerVariant: 'cpd-sticker' },
            { to: '/documents/', icon: 'bi-file-text', label: 'Documents', color: 'purple', sticker: 'DOCS', stickerVariant: 'cpd-sticker' }
        ],
        'Finances': [
            { to: '/finances/', icon: 'bi-currency-dollar', label: 'Finances', color: 'yellow', sticker: 'DONS', stickerVariant: 'cpd-sticker-gold' },
            { to: '/reports/', icon: 'bi-graph-up', label: 'Rapports', color: 'red', sticker: 'PDF', stickerVariant: 'cpd-sticker-gospel' }
        ],
        'Église': [
            { to: '/about/', icon: 'bi-info-circle', label: 'Infos Église', color: 'indigo', sticker: 'ÉGLISE', stickerVariant: 'cpd-sticker' }
        ]
    };

    // Filtrer les éléments selon le rôle
    function getNavItemsForRole(role, departmentName = '') {
        const isAdmin = role === 'admin' || role === 'super_admin';
        const isTreasurer = role === 'treasurer' || role === 'financial_head';
        const dept = (departmentName || '').toLowerCase();
        const isProtocolDeptHead = role === 'department_head' && (dept.includes('protoc') || dept.includes('protocol'));
        const isSecretary = role === 'secretary' || role === 'protocol_head' || isProtocolDeptHead;
        const isLogisticsHead = (role === 'logistics_head' || (role === 'department_head' && dept.includes('logist'))) && !isProtocolDeptHead;
        const isEvangelismHead = role === 'evangelism_head' || (role === 'department_head' && (dept.includes('evang') || dept.includes('évang')));

        if (isAdmin) {
            return NAV_GROUPS;
        }

        if (isSecretary || isLogisticsHead) {
            return filterGroups(['Général', 'Activités', 'Communication']);
        }

        if (isTreasurer) {
            return filterGroups(['Général', 'Communication', 'Finances']);
        }

        if (isEvangelismHead) {
            return filterGroups(['Général', 'Activités', 'Communication']);
        }

        // Default user
        return filterGroups(['Général', 'Communication']);
    }

    function filterGroups(allowedGroups) {
        const filtered = {};
        allowedGroups.forEach(group => {
            if (NAV_GROUPS[group]) {
                filtered[group] = NAV_GROUPS[group];
            }
        });
        return filtered;
    }

    // Générer le HTML de la navigation
    function renderNav(containerId, currentPage) {
        const container = document.getElementById(containerId);
        if (!container) return;

        const user = Auth.state.user;
        const role = user?.is_superuser ? 'super_admin' : 
                     user?.is_staff ? 'admin' : 
                     user?.role;
        const navGroups = getNavItemsForRole(role, user?.department_name);

        let html = '';
        
        Object.entries(navGroups).forEach(([groupName, items]) => {
            if (items.length === 0) return;

            html += `
                <div class="nav-section-title">${groupName}</div>
                <div class="mb-3">
            `;

            items.forEach(item => {
                const isActive = currentPage && item.to.includes(currentPage);
                const activeClass = isActive ? 'active' : '';
                
                html += `
                    <a href="${item.to}" class="cpd-nav-item ${activeClass}">
                        <i class="bi ${item.icon}"></i>
                        <span>${item.label}</span>
                        ${item.sticker ? `<span class="cpd-sticker ${item.stickerVariant}">${item.sticker}</span>` : ''}
                    </a>
                `;
            });

            html += '</div>';
        });

        container.innerHTML = html;
    }

    // Navigation publique (site vitrine)
    const PUBLIC_NAV_ITEMS = [
        { to: '/', icon: 'bi-house', label: 'Accueil' },
        { to: '/about/', icon: 'bi-info-circle', label: 'À Propos' },
        { to: '/calendar/', icon: 'bi-calendar-event', label: 'Événements' },
        { to: '/contact/', icon: 'bi-envelope', label: 'Contact' }
    ];

    function renderPublicNav(containerId, currentPage) {
        const container = document.getElementById(containerId);
        if (!container) return;

        const html = PUBLIC_NAV_ITEMS.map(item => {
            const isActive = currentPage === item.to || 
                           (currentPage === '/' && item.to === '/') ||
                           (currentPage.includes(item.to.replace(/\/$/, '')));
            const activeClass = isActive ? 'active' : '';
            
            return `
                <li class="nav-item">
                    <a class="nav-link ${activeClass}" href="${item.to}">
                        <i class="bi ${item.icon} me-1"></i>
                        ${item.label}
                    </a>
                </li>
            `;
        }).join('');

        container.innerHTML = html;
    }

    // Header avec bouton de connexion/déconnexion
    function updateAuthButton() {
        const btn = document.getElementById('authButton');
        if (!btn) return;

        // Check if Auth module is loaded (not available on public pages)
        const isAuthenticated = typeof Auth !== 'undefined' && Auth.state && Auth.state.isAuthenticated;

        if (isAuthenticated) {
            const homePath = Auth.getHomePath ? Auth.getHomePath() : '/dashboard/';
            btn.innerHTML = `
                <a href="${homePath}" class="btn btn-primary">
                    <i class="bi bi-grid me-1"></i>
                    Mon Espace
                </a>
            `;
        } else {
            btn.innerHTML = `
                <a href="/login/" class="btn btn-primary">
                    <i class="bi bi-box-arrow-in-right me-1"></i>
                    Se Connecter
                </a>
            `;
        }
    }

    // Export global
    window.Navigation = {
        render: renderNav,
        renderPublic: renderPublicNav,
        updateAuthButton,
        NAV_GROUPS,
        PUBLIC_NAV_ITEMS
    };
})();
