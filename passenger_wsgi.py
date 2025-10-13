import sys, os

# Añadir la ruta raíz del proyecto
sys.path.insert(0, '/var/www/vhosts/patchamama.com/academia.patchamama.com/devilearn')

# Configurar las variables de entorno
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "devilearn.settings")

# Cargar la aplicación WSGI de Django
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
