"""
WSGI config for SGCAS project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/howto/deployment/wsgi/
"""

import os
#mport time
#import traceback
#import signal
#import sys

from django.core.wsgi import get_wsgi_application

#sys.path.append('/home/victor/Projects/SGCAS') 
# adjust the Python version in the line below as needed 
#sys.path.append('/home/victor/Projects/SGCAS/venv/lib/python3.7/site-packages')

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SGCAS.settings')

#try: 
 #   application = get_wsgi_application() 
#except Exception: 
    # Error loading applications 
 #   if 'mod_wsgi' in sys.modules: 
  #      traceback.print_exc() 
   #     os.kill(os.getpid(), signal.SIGINT) 
    #    time.sleep(2.5)

application = get_wsgi_application()


