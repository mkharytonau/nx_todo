import os

import sys
print(sys.path)
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
print(__file__)
print(os.path.dirname(os.path.abspath(__file__)))


#Django configuration
from django.core.wsgi import get_wsgi_application
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")
application = get_wsgi_application()


from .queries import queries
from .daemon import MyDaemon
#from .thirdparty import enums
from .thirdparty import functions
from .reminding import Reminder