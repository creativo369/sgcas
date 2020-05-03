from django.db import models
from django.contrib.auth.models import User

from apps.proyecto.models import Proyecto


# === Clase que modela el concepto de un comite para los proyectos ===
class Comite(models.Model):
    # 1. **nombre**: Campo para dar asignar un nombre al comité.<br/>
    # 2. **descripción**: Campo para describir brevemente las responsabilidades e información.<br/>
    # 3. **miembros**: Relación de MuchosAmuchos con los miembros de un proyecto.<br/>
    # 4. **proyecto**: Relación del comite con un proyecto.<br/>

    nombre = models.CharField(max_length=50)
    descripcion = models.TextField()
    miembros = models.ManyToManyField(User, blank=True)
    proyecto = models.ForeignKey(Proyecto, on_delete=models.CASCADE, default=None, blank=True, null=True)

    def __str__(self):
        """
        **Función para asignar un alias al modelo Comité**<br/>
        **:return:** el nombre comité<br/>
        """
        return self.nombre

    class Meta:
        # **Clase Meta que personaliza los permisos que tendra un comité para gestionar en un rol**
        permissions = [
            ("Can add comite", "Puede crear un comité"),
            ("Can change comite", "Puede editar el comité"),
            ("Can delete comite", "Puede eliminar un comité"),
            ("Can view comite", "Puede visualizar un comité"),
        ]
# **Volver atras** : [[forms.py]]

# **Ir a la documentación de pruebas unitarias del modulo comité** : [[tests.py]]

# === Indice de la documentación de la Aplicación Comité  === <br/>
# 1.admin   : [[admin.py]]<br/>
# 2.apps    : [[apps.py]]<br/>
# 3.forms   : [[forms.py]]<br/>
# 4.models  : [[models.py]]<br/>
# 5.tests   : [[tests.py]]<br/>
# 6.urls    : [[urls.py]]<br/>
# 7.views   : [[views.py]]<br/>