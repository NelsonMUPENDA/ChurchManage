from django.apps import AppConfig


class ChurchManagementAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'church_management_app'
    verbose_name = 'Gestion de l\'Église'

    def ready(self):
        # Appliquer les patches de compatibilité
        from . import patches
        patches.apply_patches()
        
        # Import signals if needed
        pass
