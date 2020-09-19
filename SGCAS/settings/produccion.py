from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['sgcas.herokuapp.com']

# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',

        'NAME': 'qjrltnycoqigoz',
        'USER': 'qjrltnycoqigoz',
        'PASSWORD': '03e10c13eec96b237f23b64b7c1c2408813a52bc4925c756b59e2198486b2101',
        'HOST': 'ec2-34-238-26-109.compute-1.amazonaws.com',
        'PORT': 5432,
    },
}
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

# STATICFILES_DIRS = (BASE_DIR, 'static')
STATICFILES_DIRS = (os.path.join(BASE_DIR, "SGCAS", "static"),)
