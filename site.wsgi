import os, sys

activate_this = '/home/a0397412/python/bin/activate_this.py'
with open(activate_this) as f:
  exec(f.read(), {'__file__': activate_this})
sys.path.insert(0, os.path.join('/home/a0397412/domains/easynote.uxp.ru/myproject'))
os.environ['DJANGO_SETTINGS_MODULE'] = 'myproject.settings'
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
