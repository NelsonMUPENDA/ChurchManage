# permissions_tags.py - Template tags pour les permissions
from django import template
from church_management_app.permissions import (
    can_access_menu, can_create, can_edit, can_delete, can_export,
    can_manage_users, get_role_display_name, get_user_permissions
)

register = template.Library()

@register.filter(name='can_access_menu')
def can_access_menu_filter(user, menu_name):
    """Filtre pour vérifier l'accès à un menu"""
    if not user or not user.is_authenticated:
        return False
    return can_access_menu(user, menu_name)

@register.filter(name='can_create')
def can_create_filter(user):
    """Filtre pour vérifier si l'utilisateur peut créer"""
    if not user or not user.is_authenticated:
        return False
    return can_create(user)

@register.filter(name='can_edit')
def can_edit_filter(user):
    """Filtre pour vérifier si l'utilisateur peut modifier"""
    if not user or not user.is_authenticated:
        return False
    return can_edit(user)

@register.filter(name='can_delete')
def can_delete_filter(user):
    """Filtre pour vérifier si l'utilisateur peut supprimer"""
    if not user or not user.is_authenticated:
        return False
    return can_delete(user)

@register.filter(name='can_export')
def can_export_filter(user):
    """Filtre pour vérifier si l'utilisateur peut exporter"""
    if not user or not user.is_authenticated:
        return False
    return can_export(user)

@register.filter(name='can_manage_users')
def can_manage_users_filter(user):
    """Filtre pour vérifier si l'utilisateur peut gérer les utilisateurs"""
    if not user or not user.is_authenticated:
        return False
    return can_manage_users(user)

@register.filter(name='role_display')
def role_display_filter(user):
    """Filtre pour afficher le nom du rôle"""
    if not user or not user.is_authenticated:
        return 'Anonyme'
    if user.is_superuser:
        return 'Super Administrateur'
    return get_role_display_name(user.role)

@register.simple_tag(takes_context=True)
def get_allowed_menus(context):
    """Tag pour récupérer les menus autorisés pour l'utilisateur"""
    request = context.get('request')
    if not request or not request.user.is_authenticated:
        return []
    permissions = get_user_permissions(request.user)
    return permissions.get('menu', [])

@register.simple_tag(takes_context=True)
def has_permission(context, permission_name):
    """Tag pour vérifier une permission spécifique"""
    request = context.get('request')
    if not request or not request.user.is_authenticated:
        return False
    
    user = request.user
    if user.is_superuser:
        return True
    
    permissions = get_user_permissions(user)
    return permissions.get(permission_name, False)


@register.filter(name='get_item')
def get_item(dictionary, key):
    """Filtre pour récupérer une valeur d'un dictionnaire par clé"""
    if dictionary is None:
        return None
    return dictionary.get(key)
