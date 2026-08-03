"""
WSGI config for ecocart project.

It exposes the WSGI callable as a module-level variable named ``application``.
"""

import os
import sys

# Ensure ecocart project folder is in sys.path for Vercel serverless functions
current_dir = os.path.dirname(os.path.abspath(__file__))
project_dir = os.path.dirname(current_dir)
root_dir = os.path.dirname(project_dir)

for d in [project_dir, root_dir]:
    if d not in sys.path:
        sys.path.insert(0, d)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecocart.settings')

from django.core.wsgi import get_wsgi_application

application = get_wsgi_application()
app = application
