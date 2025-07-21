"""
ASGI config for website_1 project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/asgi/
"""

import os
# asgi.py
import os
import django
from fastapi import FastAPI
from fastapi.middleware.wsgi import WSGIMiddleware
from django.core.asgi import get_asgi_application
from fastapi_app import fastapi_app  # import your FastAPI app

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'website_1.settings')
django.setup()

# Get Django ASGI application
django_asgi_app = get_asgi_application()
# Mount Django under "/"
fastapi_app.mount("/", django_asgi_app)

# Final app to run with uvicorn
app = fastapi_app
