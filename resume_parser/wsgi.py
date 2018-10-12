"""
WSGI config for resume_parser project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/howto/deployment/wsgi/
"""
from whitenoise import WhiteNoise

from resume_parser import pdf_parser

application = MyWSGIApp()
application = WhiteNoise(application, root='/path/to/static/files')
application.add_files('/path/to/more/static/files', prefix='more-files/')

import os
#
#from django.core.wsgi import get_wsgi_application
#from whitenoise.django import DjangoWhiteNoise

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "resume_parser.settings")

#application = get_wsgi_application()
#application = DjangoWhiteNoise(application)
