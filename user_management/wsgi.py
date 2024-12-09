"""
WSGI config for user_management project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'user_management.settings')

application = get_wsgi_application()



# Ejecutar script para crear superusuario
import os
if os.getenv('CREATE_SUPERUSER', 'false').lower() == 'true':
    from users.create_superuser import *
