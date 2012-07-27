import os
import sys
 
sys.path.append('/home/biomecanica/Operacion_Sonrisa')
sys.path.append('/home/biomecanica/Operacion_Sonrisa/tds_os')

path = '/home/biomecanica/Operacion_Sonrisa'
if path not in sys.path:
    sys.path.insert(0, '/home/biomecanica/Operacion_Sonrisa')
 
os.environ['DJANGO_SETTINGS_MODULE'] = 'tds_os.settings'
 
import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
