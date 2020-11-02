from django.db import models
from apps.usuario.models import User
from apps.item.models import Item
from apps.linea_base.models import LineaBase
from apps.proyecto.models import Proyecto
import datetime

tipo_solicitud = [('Item', 'Item'), ('LineaBase', 'LineaBase')]

class Voto(models.Model):
	votante = models.ForeignKey(User, on_delete=models.DO_NOTHING)
	decision = models.BooleanField(default=True)
	fecha_voto = models.DateField(default=datetime.date.today)


class Solicitud(models.Model):
	asunto = models.CharField(max_length=100, default="")
	solicitante = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='solicitante', blank=True, null=True)
	votantes = models.ManyToManyField(User, blank=True)
	item = models.ForeignKey(Item, on_delete=models.CASCADE, blank=True, null=True)
	proyecto = models.ForeignKey(Proyecto, on_delete=models.CASCADE, blank=True, null=True)
	tipo = models.CharField(max_length=100, choices=tipo_solicitud, default='Item')
	linea_base = models.ForeignKey(LineaBase, on_delete=models.CASCADE, blank=True, null=True)
	fecha_solicitada = models.DateField(default=datetime.date.today)  
	votacion = models.IntegerField(default=0)
	descripcion = models.TextField()
	auditoria = models.ManyToManyField(Voto,blank=True)
	en_proceso = models.BooleanField(default=True)
    



	def __str__(self):
		return self.asunto