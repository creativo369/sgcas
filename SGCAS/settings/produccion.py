from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'd9alvv5plovg8n',
        'USER': 'lkadbdgmkddzym',
        'PASSWORD': 'cd175db2f69f71c7dbba2cfe23f1c1987d99dc08e1502500b3255e7794564b37',
        'HOST': 'ec2-54-156-121-142.compute-1.amazonaws.com',
        'PORT': 5432,
    },
}
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

# STATICFILES_DIRS = (BASE_DIR, 'static')
STATICFILES_DIRS = (os.path.join(BASE_DIR, "SGCAS", "static"),)
