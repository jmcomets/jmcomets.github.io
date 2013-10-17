"""
WSGI config for jmcomets.com project.
"""

from os import environ as env
env.setdefault('DJANGO_SETTINGS_MODULE', 'website.settings_no_debug')

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
