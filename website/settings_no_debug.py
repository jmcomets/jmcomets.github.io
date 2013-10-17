"""
Django release settings for jmcomets.com project.
"""

from settings import *

# Debug
DEBUG = False
TEMPLATE_DEBUG = DEBUG

# Database
DATABASES = {
        'default': {
            'HOST': 'ec2-54-235-102-202.compute-1.amazonaws.com',
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': 'd521t9cvrb3ive',
            'USER': 'rktcmzwcoaryhi',
            'PASSWORD': 'GL2DChq-QmIS0n-FYiYWYzKLSP',
            'PORT': '5432',
            }
        }
