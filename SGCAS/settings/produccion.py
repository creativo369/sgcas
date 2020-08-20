from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['sgcas.herokuapp.com']

# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'dao28eim3euv24',
        'USER': 'cmpwlzhuwkgxjm',
        'PASSWORD': '858c4b358153c790af1c66bdd2f2306a161d9587f9d8d157d0e7c22c9fe576e3',
        'HOST': 'ec2-34-238-26-109.compute-1.amazonaws.com',
        'PORT': 5432,
    },
}
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

# STATICFILES_DIRS = (BASE_DIR, 'static')
STATICFILES_DIRS = (os.path.join(BASE_DIR, "SGCAS", "static"),)
