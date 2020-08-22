from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['sgcas.herokuapp.com']

# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'd4l2en2linv18c',
        'USER': 'itlhcpnbevkdni',
        'PASSWORD': '1611f55748128bc7a2ed35bf93f22e4d7097753cb6c999ae7248e44dfc3fd84a',
        'HOST': 'ec2-54-91-178-234.compute-1.amazonaws.com',
        'PORT': 5432,
    },
}
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

# STATICFILES_DIRS = (BASE_DIR, 'static')
STATICFILES_DIRS = (os.path.join(BASE_DIR, "SGCAS", "static"),)
