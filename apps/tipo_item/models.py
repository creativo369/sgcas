from django.db import models

# Create your models here.
class TipoItem(models.Model):
	nombre = models.CharField(max_length = 50)
	descripcion = models.CharField(max_length = 50)
	# atributos = boolean, char, date, numerico
	# archivo = models.
	def _str__(self):
		return '{}'.format(self.TipoItem.nombre)