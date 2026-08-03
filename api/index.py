import os
import sys

# Get the path to the repository root and ecocart project folder
root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ecocart_dir = os.path.join(root_dir, 'ecocart')

# Insert directories into sys.path so Python can resolve ecocart.settings & apps
for path in [ecocart_dir, root_dir]:
    if path not in sys.path:
        sys.path.insert(0, path)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecocart.settings')

from django.core.wsgi import get_wsgi_application

app = get_wsgi_application()
