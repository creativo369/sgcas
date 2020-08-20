from apps.usuario.models import User
from django.test import TestCase
from apps.comite.models import Comite
from apps.proyecto.models import Proyecto


class TestComiteSetUp(TestCase):
    def setUp(self):
        self.proyecto = Proyecto.objects.first()
        self.miembro = User.objects.create(username='miembro-comite-test')
        self.comite = Comite.objects.create(nombre='comite-test', descripcion='descripcion-comite-test',
                                            proyecto=self.proyecto)
        self.comite.miembros.add(self.miembro)


class ComiteTestCrear(TestComiteSetUp):

    def setUp(self):
        super(ComiteTestCrear, self).setUp()

    def test_nombre(self):
        self.assertEqual(self.comite.nombre, 'comite-test')
        print('Comite-test_nombre OK')

    def test_descripcion(self):
        self.assertEqual(self.comite.descripcion, 'descripcion-comite-test')
        print('Comite-test_descripcion OK')

    def test_pertenece_proyecto(self):
        self.assertEqual(self.comite.proyecto, self.proyecto)
        print('Comite-test_pertenece_proyecto OK')

    def test_miembro(self):
        self.assertEqual(self.comite.miembros.first(), self.miembro)
        print('Comite-test_miembro OK')


class ComiteTestEditar(TestComiteSetUp):

    def setUp(self):
        super(ComiteTestEditar, self).setUp()
        self.miembro_2 = User.objects.create(username='miembro-comite-2')

    def test_editar_nombre(self):
        nombre_anterior = self.comite.nombre
        self.comite.nombre = 'comite-test-nombre-cambiado'
        self.comite.save()
        self.assertNotEqual(self.comite.nombre, nombre_anterior)
        print('Comite-test_editar_nombre OK')

    def test_editar_descripcion(self):
        descripcion_anterior = self.comite.descripcion
        self.comite.descripcion = 'descripcion-cambiada-test'
        self.comite.save()
        self.assertNotEqual(self.comite.nombre, descripcion_anterior)
        print('Comite-test_editar_descripcion OK')


class ComiteTestEliminar(TestComiteSetUp):
    def setUp(self):
        super(ComiteTestEliminar, self).setUp()
        self.id_comite = self.comite.id

    def __del__(self):
        print('Comite borrado OK')

    def test_eliminar_comite(self):
        self.comite.delete()
# **Volver atras** : [[models.py]]

# **Ir a la documentación de URLS del modulo comité** : [[urls.py]]

# === Indice de la documentación de la Aplicación Comité  === <br/>
# 1.admin   : [[admin.py]]<br/>
# 2.apps    : [[apps.py]]<br/>
# 3.forms   : [[forms.py]]<br/>
# 4.models  : [[models.py]]<br/>
# 5.tests   : [[tests.py]]<br/>
# 6.urls    : [[urls.py]]<br/>
# 7.views   : [[views.py]]<br/>
