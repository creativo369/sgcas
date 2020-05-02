from django.db import models


# Create your models here.
class Usuario(models.Model):
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    nombres = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    roles = models.CharField(max_length=50)
    estado = models.BooleanField(default=False)

    def __str__(self):
        return '{}'.format(self.Usuario.nombres)

    class Meta:
        permissions = [
            ("Can add usuario", "Puede registrar un usuario"),
            ("Can change usuario", "Puede modificar el usuario"),
            ("Can delete usuario", "Puede eliminar un usuario"),
            ("Can view usuario", "Puede visualizar un usuario"),
        ]
