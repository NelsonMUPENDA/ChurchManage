#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'church_management.settings')
    
    # Apply compatibility patches for Python 3.14 BEFORE importing Django
    try:
        import sys
        if sys.version_info >= (3, 14):
            # Add project to path temporarily to import patches
            project_path = os.path.dirname(os.path.abspath(__file__))
            if project_path not in sys.path:
                sys.path.insert(0, project_path)
            from church_management_app.patches import apply_patches
            apply_patches()
    except Exception:
        pass  # Silently fail if patches can't be applied
    
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
