from django.db import models
from django.contrib.auth.models import User
import datetime
from django.core.exceptions import ValidationError



class Proyecto(models.Model):
    """
    Clase que modela el concepto de Proyecto
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='gerente')
    nombre = models.CharField(max_length=50)
    descripcion = models.TextField()
    fecha_creacion = models.DateField(default=datetime.date.today)
    ultima_modificación = models.DateTimeField(auto_now=True)
    estado = models.CharField(max_length=30, default="Pendiente")
    slug = models.CharField(max_length=50, default="")
    miembros = models.ManyToManyField(User, blank=True)


    def __str__(self):
        return self.nombre

    def validate_unique(self, exclude=None):
        """
        Función que valida que el nombre de un proyecto sea unico.
        :param exclude: None
        :return: Mensaje de Validación
        """
        if Proyecto.objects.filter(nombre=self.nombre).exclude(pk=self.id).exists():
            raise ValidationError("Un proyecto con el mismo título ya se encuentra registrado")

    def save(self, *args, **kwargs):
        """
        Función que guarda el proyecto en la base de datos como unico.
        :param args:
        :param kwargs:
        :return: Un string que va ser unico en nuestra base de datos
        """
        self.validate_unique()
        self.slug = self.nombre.replace(" ", "_").lower()
        super(Proyecto, self).save(*args, **kwargs)
