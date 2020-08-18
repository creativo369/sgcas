##Configuraciones para el envio de email a traves de gmail
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'is2.equipo7.sgcas@gmail.com'
EMAIL_HOST_PASSWORD = 'is212345678'
EMAIL_PORT = 587
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'