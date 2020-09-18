from django.test import TestCase
from django.contrib.auth.models import Group
from apps.rol.models import Rol
from apps.proyecto.models import Proyecto
from apps.fase.models import Fase

class TestRolSetUp(TestCase):
    def setUp(self):
        self.nombre = 'test'        
        self.fase = Fase.objects.create(nombre='fase_test', descripcion='fase_test',
        		proyecto=Proyecto.objects.first())
        self.group=Group.objects.create(name='grupo1')


class RolTestCrear(TestRolSetUp):

    def setUp(self):
        super(RolTestCrear, self).setUp()

    def test_nombre(self):        
        self.assertEqual(self.nombre, 'test')

  

    def test_pertenece_Group(self):
        self.assertEqual(self.group, Group.objects.first())


class RolTestEditar(TestRolSetUp):

    def setUp(self):
        super(RolTestEditar, self).setUp()        

    def test_editar_nombre(self):
        nombre_anterior = self.nombre
        self.nombre = 'rol-test-nombre-cambiado'

        self.assertNotEqual(self.nombre,nombre_anterior)        
        

    def test_editar_group(self):
        group_anterior = Group.objects.none()
        group_anterior = self.group
        self.group = Group.objects.create(name='grupo2')
        
        self.assertNotEqual(self.group,group_anterior)

        

# === Indice de la documentación de la Aplicación rol  === <br/>
# 1.apps     : [[apps.py]]<br/>
# 2.forms    : [[forms.py]]<br/>
# 3.tests    : [[tests.py]]<br/>
# 4.urls     : [[urls.py]]<br/>
# 5.views    : [[views.py]]<br/>

# Regresar al menu principal : [Menú Principal](../../docs-index/index.html)