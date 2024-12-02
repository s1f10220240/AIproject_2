"""
ASGI config for AIproject project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/asgi/
"""

import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'AIproject.settings')

application = get_asgi_application()
