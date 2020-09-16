from django.test import TestCase
from django.core.exceptions import ValidationError
from apps.usuario.models import User

class TestProyectoSetUp(TestCase):
    def setUp(self):
    	self.gerente = User.objects.create(username='gerente-proyecto')
    	self.nombre = 'proyecto-prueba'
    	self.descripcion = 'descripcion-proyecto-prueba'
    	

class ProyectoTestCrear(TestProyectoSetUp):

    def setUp(self):
        super(ProyectoTestCrear, self).setUp()

    def test_nombre(self):
        nombre_proyecto = 'proyecto-prueba'
        #self.assertEqual(self.nombre, 'proyecto-prueba')
        if not self.nombre == nombre_proyecto:
            raise ValidationError('Datos proporcionados no coinciden.')
        

    def test_descripcion(self):
        descripcion_proyecto = 'descripcion-proyecto-prueba'
        #self.assertEqual(self.descripcion, 'descripcion-proyecto-prueba')          
        if not self.descripcion == descripcion_proyecto:
            raise ValidationError('Datos proporcionados no coinciden.')
        


class ProyectoTestEditar(TestProyectoSetUp):

    def setUp(self):
        super(ProyectoTestEditar, self).setUp()
        self.gerente = User.objects.create(username='gerente2')

    def test_editar_nombre(self):
        nombre_anterior = self.nombre
        self.nombre = 'Proyecto-test-nombre-cambiado'
        #self.assertNotEqual(self.nombre, nombre_anterior)
        if self.nombre == nombre_anterior:
            raise ValidationError ('Datos proporcionados son iguales.')
        

    def test_editar_descripcion(self):
        descripcion_anterior = self.descripcion
        self.descripcion = 'descripcion-cambiada-test'
        #self.assertNotEqual(self.descripcion, descripcion_anterior)
        if self.descripcion == descripcion_anterior:
            raise ValidationError ('Datos proporcionados son iguales')
        





# **Volver atras** : [[models.py]]

# **Ir a la documentación de la URL de la Aplicación** :[[urls.py]]

# === Indice de la documentación de la Aplicación Proyecto  === <br/>
# 1.admin   : [[admin.py]]<br/>
# 2.apps    : [[apps.py]]<br/>
# 3.forms   : [[forms.py]]<br/>
# 4.models  : [[models.py]]<br/>
# 5.tests   : [[tests.py]]<br/>
# 6.urls    : [[urls.py]]<br/>
# 7.views   : [[views.py]]<br/>

# Regresar al menu principal : [Menú Principal](../../docs-index/index.html)