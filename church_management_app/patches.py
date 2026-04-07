"""
Monkey patches pour corriger les bugs de compatibilité Python 3.14 avec Django 4.2.x
Ce fichier doit être importé AVANT que Django ne charge ses templates
"""
import sys


def patch_django_template_context():
    """
    Corrige le bug 'super' object has no attribute 'dicts' dans Django 4.2.x avec Python 3.14
    """
    if sys.version_info < (3, 14):
        return  # Pas nécessaire avant Python 3.14
    
    try:
        from django.template.context import BaseContext
        import copy
        
        # Définir une nouvelle méthode __copy__ qui évite l'appel à super().__copy__()
        def patched_copy(self):
            duplicate = self.__class__.__new__(self.__class__)
            for key, value in self.__dict__.items():
                if key == 'dicts':
                    setattr(duplicate, key, value[:])
                else:
                    setattr(duplicate, key, copy.copy(value))
            return duplicate
        
        # Remplacer la méthode __copy__
        BaseContext.__copy__ = patched_copy
        print("✅ Patch Django appliqué: BaseContext.__copy__ corrigé pour Python 3.14")
        
    except Exception as e:
        print(f"⚠️  Erreur lors de l'application du patch Django: {e}")
        import traceback
        traceback.print_exc()


def apply_patches():
    """Appliquer tous les patches nécessaires au démarrage"""
    patch_django_template_context()


# Appliquer les patches immédiatement
apply_patches()
