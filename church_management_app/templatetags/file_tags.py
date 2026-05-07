from django import template

register = template.Library()

@register.filter
def filesize(value):
    """Formate la taille d'un fichier en octets, Ko, Mo, Go"""
    try:
        size = int(value)
        if size < 1024:
            return f"{size} o"
        elif size < 1024 * 1024:
            return f"{size / 1024:.1f} Ko"
        elif size < 1024 * 1024 * 1024:
            return f"{size / (1024 * 1024):.1f} Mo"
        else:
            return f"{size / (1024 * 1024 * 1024):.1f} Go"
    except (ValueError, TypeError):
        return "0 o"
