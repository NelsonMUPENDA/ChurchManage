"""
Context processors pour ChurchManageApp
Fournit les données globales à tous les templates
"""
from .models import ChurchSettings


def church_settings(request):
    """
    Context processor qui rend les paramètres de l'église disponibles
    dans tous les templates via la variable {{ church_settings }}
    """
    # Skip admin URLs to avoid context conflicts
    if request.path.startswith('/admin/'):
        return {}
    
    try:
        settings = ChurchSettings.get_settings()
    except:
        # En cas d'erreur (ex: base de données vide), retourner un objet vide
        settings = None
    
    return {
        'church_settings': settings
    }
