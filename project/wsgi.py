"""WSGI config for project project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/wsgi/
"""

import os
import time

from django.core.wsgi import get_wsgi_application
import gunicorn.glogging

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.prod_settings")

application = get_wsgi_application()


class TolerableLogger(gunicorn.glogging.Logger):
    def now(self):
        return time.strftime("%Y-%m-%dT%H:%M:%S%z")
