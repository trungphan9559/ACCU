"""
WSGI config for main project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/howto/deployment/wsgi/
"""

import os
import sys

sys.path.append('/opt/bitnami/projects/msp-project/SourceCode')
os.environ.setdefault("PYTHON_EGG_CACHE", "/opt/bitnami/projects/msp-project/SourceCode/main/egg_cache")
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'main.settings')

application = get_wsgi_application()
