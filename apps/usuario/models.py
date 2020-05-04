from django.db import models


# === Clase que modela el concepto de un usuario ===
class Usuario(models.Model):
    # 1. **username**: atributo donde se almacena el username de un usuario.<br/>
    # 2. **password**: atributo que guarda la contraseña del usuario.<br/>
    # 3. **nombres**: atributo donde se almacena el nombre del usuario.<br/>
    # 4. **apellido**: atributo donde se almacena el apellido del usuario.<br/>
    # 5. **roles**: atributo donde se almacena los roles de un usuario.<br/>
    # 6. **estado**: atributo que alamacena el estado del usuario en el sistema.<br/>
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    nombres = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    roles = models.CharField(max_length=50)
    estado = models.BooleanField(default=False)

    def __str__(self):
        """
        **Función para asignar un alias al modelo Usuario**<br/>
        **:return:** el nombre usuario<br/>
        """
        return '{}'.format(self.Usuario.nombres)

# === Indice de la documentación de la Aplicación Usuario  === <br/>
# 1.apps        : [[apps.py]]<br/>
# 2.forms       : [[forms.py]]<br/>
# 3.middleware  : [[middleware.py]]<br/>
# 4.models      : [[models.py]]<br/>
# 5.tests       : [[tests.py]]<br/>
# 6.urls        : [[urls.py]]<br/>
# 7.views       : [[views.py]]<br/>
