from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import datetime
from django.core.exceptions import ValidationError

class Proyecto(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='gerente')
    nombre = models.CharField(max_length=50)
    descripcion = models.TextField()
    fecha_creacion = models.DateField(default=datetime.date.today)
    estado = models.CharField(max_length=30, default="Pendiente")
    slug = models.CharField(max_length=50, default="")
    miembros = models.ManyToManyField(User, blank=True)

    # fases										# Pendiente de hacer
    # tiposItems								# Pendiente de hacer

    def __str__(self):
        return self.nombre

    def validate_unique(self, exclude=None):
        if Proyecto.objects.filter(nombre=self.nombre).exclude(pk=self.id).exists():
            raise ValidationError("Un proyecto con el mismo título ya se encuentra registrado")

    def save(self, *args, **kwargs):
        self.validate_unique()
        self.slug = self.nombre.replace(" ", "_").lower()  # return string lo cual va ser unico en nuestra DB
        super(Proyecto, self).save(*args, **kwargs)