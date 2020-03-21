from django.db import models

# Create your models here.
class Usuario(models.Model):
    username= models.CharField(max_length=50)
    passwordd=models.CharField(max_length=50)
    nombres=models.CharField(max_length=50)
    apellido=models.CharField(max_length=50)
    rol_de_sistema=models.CharField(max_length=50) #Este tiene que ser del tipo Rol pero como no tengo el modelo Rol , mientras asi
    estado=models.CharField(max_length=50)

    def __str__(self):
        return '{}'.format(self.Usuario.nombres)