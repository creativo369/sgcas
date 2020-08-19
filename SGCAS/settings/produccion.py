from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['sgcas.herokuapp.com']

# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'd6dmt73g9bcgtv',
        'USER': 'vidmjwtyehbzdf',
        'PASSWORD': '37719fa80206868d4ed5d3f8d3be17319504d24fcd72578b4c66398e683e2d29',
        'HOST': 'ec2-34-197-141-7.compute-1.amazonaws.com',
        'PORT': 5432,
    },
}
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

# STATICFILES_DIRS = (BASE_DIR, 'static')
STATICFILES_DIRS = (os.path.join(BASE_DIR, "SGCAS", "static"),)
