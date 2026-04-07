"""
ASGI config for church_management project.
"""
import os
from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'church_management.settings')

application = get_asgi_application()
