"""
WSGI config for website_1 project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/wsgi/
"""

#from django.core.wsgi import get_wsgi_application

# myproject/asgi.py
import os
import django
from fastapi.middleware.wsgi import WSGIMiddleware
from django.core.asgi import get_asgi_application
from fastapi_app import fastapi_app

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
django.setup()

# Get Django ASGI app
django_asgi_app = get_asgi_application()

# Mount Django at `/`, FastAPI runs side-by-side
fastapi_app.mount("/", django_asgi_app)

# The final ASGI app for uvicorn
app = fastapi_app


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'website_1.settings')

#application = get_wsgi_application()
