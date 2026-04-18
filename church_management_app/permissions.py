# permissions.py - Gestion des rôles et permissions
from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages

# ============================================================
# Définition des permissions par rôle
# ============================================================

ROLE_PERMISSIONS = {
    'super_admin': {
        'menu': ['dashboard', 'members', 'families', 'home_groups', 'departments', 'ministries',
                 'events', 'attendance', 'finances', 'announcements',
                 'trainings', 'logistics', 'diaconat', 'baptisms', 'evangelisation', 'marriages',
                 'documents', 'contacts', 'audit_logs', 'reports', 'account'],
        'can_create': True,
        'can_edit': True,
        'can_delete': True,
        'can_export': True,
        'can_manage_users': True,
        'can_manage_settings': True,
    },
    'pastor': {
        'menu': ['dashboard', 'members', 'families', 'home_groups', 'departments', 'ministries',
                 'events', 'attendance', 'finances', 'announcements',
                 'trainings', 'logistics', 'diaconat', 'baptisms', 'evangelisation', 'marriages',
                 'documents', 'contacts', 'audit_logs', 'reports', 'account'],
        'can_create': True,
        'can_edit': True,
        'can_delete': True,
        'can_export': True,
        'can_manage_users': True,
        'can_manage_settings': True,
    },
    'admin': {
        'menu': ['dashboard', 'members', 'families', 'home_groups', 'departments', 'ministries',
                 'events', 'attendance', 'finances', 'announcements',
                 'trainings', 'logistics', 'diaconat', 'baptisms', 'evangelisation', 'marriages',
                 'documents', 'contacts', 'audit_logs', 'reports', 'account'],
        'can_create': True,
        'can_edit': True,
        'can_delete': True,
        'can_export': True,
        'can_manage_users': True,
        'can_manage_settings': False,
    },
    'administrator': {
        'menu': ['dashboard', 'members', 'families', 'home_groups', 'departments', 'ministries',
                 'events', 'attendance', 'finances', 'announcements',
                 'trainings', 'logistics', 'diaconat', 'baptisms', 'evangelisation', 'marriages',
                 'documents', 'contacts', 'reports', 'account'],
        'can_create': True,
        'can_edit': True,
        'can_delete': True,
        'can_export': True,
        'can_manage_users': True,
        'can_manage_settings': False,
    },
    'financial_head': {
        'menu': ['dashboard', 'finances', 'reports', 'account'],
        'can_create': True,
        'can_edit': True,
        'can_delete': True,
        'can_export': True,
        'can_manage_users': False,
        'can_manage_settings': False,
    },
    'treasurer': {
        'menu': ['dashboard', 'finances', 'account'],
        'can_create': True,
        'can_edit': True,
        'can_delete': False,
        'can_export': True,
        'can_manage_users': False,
        'can_manage_settings': False,
    },
    'protocol_head': {
        'menu': ['dashboard', 'members', 'families', 'home_groups', 'departments', 'ministries',
                 'events', 'attendance', 'announcements', 'baptisms', 'marriages', 'documents', 'account'],
        'can_create': True,
        'can_edit': True,
        'can_delete': False,
        'can_export': True,
        'can_manage_users': False,
        'can_manage_settings': False,
    },
    'secretary': {
        'menu': ['dashboard', 'members', 'families', 'home_groups', 'departments', 'ministries',
                 'events', 'attendance', 'announcements',
                 'baptisms', 'marriages', 'documents', 'contacts', 'reports', 'account'],
        'can_create': True,
        'can_edit': True,
        'can_delete': False,
        'can_export': True,
        'can_manage_users': False,
        'can_manage_settings': False,
    },
    'department_head': {
        'menu': ['dashboard', 'members', 'families', 'home_groups', 'departments', 'ministries',
                 'events', 'attendance', 'documents', 'account'],
        'can_create': True,
        'can_edit': True,
        'can_delete': False,
        'can_export': False,
        'can_manage_users': False,
        'can_manage_settings': False,
    },
    'logistics_head': {
        'menu': ['dashboard', 'logistics', 'diaconat', 'events', 'account'],
        'can_create': True,
        'can_edit': True,
        'can_delete': True,
        'can_export': False,
        'can_manage_users': False,
        'can_manage_settings': False,
    },
    'evangelism_head': {
        'menu': ['dashboard', 'evangelisation', 'members', 'reports', 'account'],
        'can_create': True,
        'can_edit': True,
        'can_delete': False,
        'can_export': True,
        'can_manage_users': False,
        'can_manage_settings': False,
    },
    'member': {
        'menu': ['dashboard', 'account'],
        'can_create': False,
        'can_edit': False,
        'can_delete': False,
        'can_export': False,
        'can_manage_users': False,
        'can_manage_settings': False,
    },
    'visitor': {
        'menu': ['dashboard', 'account'],
        'can_create': False,
        'can_edit': False,
        'can_delete': False,
        'can_export': False,
        'can_manage_users': False,
        'can_manage_settings': False,
    },
}

# ============================================================
# Fonctions utilitaires
# ============================================================

def get_user_permissions(user):
    """Retourne les permissions d'un utilisateur"""
    if user.is_superuser:
        return ROLE_PERMISSIONS.get('super_admin', {})
    return ROLE_PERMISSIONS.get(user.role, ROLE_PERMISSIONS.get('visitor', {}))

def can_access_menu(user, menu_name):
    """Vérifie si l'utilisateur peut accéder à un menu"""
    if user.is_superuser:
        return True
    permissions = get_user_permissions(user)
    allowed_menus = permissions.get('menu', [])
    return menu_name in allowed_menus

def can_create(user):
    """Vérifie si l'utilisateur peut créer"""
    if user.is_superuser:
        return True
    permissions = get_user_permissions(user)
    return permissions.get('can_create', False)

def can_edit(user):
    """Vérifie si l'utilisateur peut modifier"""
    if user.is_superuser:
        return True
    permissions = get_user_permissions(user)
    return permissions.get('can_edit', False)

def can_delete(user):
    """Vérifie si l'utilisateur peut supprimer"""
    if user.is_superuser:
        return True
    permissions = get_user_permissions(user)
    return permissions.get('can_delete', False)

def can_export(user):
    """Vérifie si l'utilisateur peut exporter"""
    if user.is_superuser:
        return True
    permissions = get_user_permissions(user)
    return permissions.get('can_export', False)

def can_manage_users(user):
    """Vérifie si l'utilisateur peut gérer les utilisateurs"""
    if user.is_superuser:
        return True
    permissions = get_user_permissions(user)
    return permissions.get('can_manage_users', False)

def get_role_display_name(role):
    """Retourne le nom affiché d'un rôle"""
    role_names = {
        'super_admin': 'Super Administrateur',
        'pastor': 'Pasteur',
        'admin': 'Administrateur',
        'administrator': 'Administrateur',
        'financial_head': 'Responsable Financier',
        'treasurer': 'Trésorier',
        'protocol_head': 'Responsable Protocole',
        'secretary': 'Secrétaire',
        'department_head': 'Chef de Département',
        'logistics_head': 'Responsable Logistique',
        'evangelism_head': 'Responsable Évangélisation',
        'member': 'Membre',
        'visitor': 'Visiteur',
    }
    return role_names.get(role, role)

# ============================================================
# Décorateurs pour les vues
# ============================================================

def role_required(allowed_roles):
    """
    Décorateur qui vérifie si l'utilisateur a un rôle autorisé
    Usage: @role_required(['admin', 'pastor', 'financial_head'])
    """
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if request.user.is_superuser:
                return view_func(request, *args, **kwargs)
            if request.user.role in allowed_roles:
                return view_func(request, *args, **kwargs)
            messages.error(request, "Vous n'avez pas les permissions nécessaires pour accéder à cette page.")
            return redirect('dashboard')
        return _wrapped_view
    return decorator

def admin_required(view_func):
    """Décorateur pour les vues réservées aux administrateurs"""
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_superuser or request.user.role in ['admin', 'administrator', 'super_admin']:
            return view_func(request, *args, **kwargs)
        messages.error(request, "Accès réservé aux administrateurs.")
        return redirect('dashboard')
    return _wrapped_view

def finance_required(view_func):
    """Décorateur pour les vues réservées à la finance"""
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_superuser or request.user.role in ['financial_head', 'treasurer', 'admin', 'pastor']:
            return view_func(request, *args, **kwargs)
        messages.error(request, "Accès réservé au personnel financier.")
        return redirect('dashboard')
    return _wrapped_view

def pastor_required(view_func):
    """Décorateur pour les vues réservées au pasteur"""
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_superuser or request.user.role in ['pastor', 'admin', 'super_admin']:
            return view_func(request, *args, **kwargs)
        messages.error(request, "Accès réservé au pasteur.")
        return redirect('dashboard')
    return _wrapped_view

def member_management_required(view_func):
    """Décorateur pour les vues de gestion des membres"""
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        allowed_roles = ['super_admin', 'pastor', 'admin', 'administrator', 'protocol_head', 'secretary', 'department_head']
        if request.user.is_superuser or request.user.role in allowed_roles:
            return view_func(request, *args, **kwargs)
        messages.error(request, "Vous n'avez pas les permissions pour gérer les membres.")
        return redirect('dashboard')
    return _wrapped_view
