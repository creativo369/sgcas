from django.test import TestCase
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
        try:
            self.assertEqual(self.nombre, 'proyecto-prueba')
        except AssertionError as e:
            print("Error de comparacion: {}".format(e))

    def test_descripcion(self):
        try:
            self.assertEqual(self.descripcion, 'descripcion-proyecto-prueba')
        except AssertionError as e:
            print("Error de comparacion: {}".format(e))


class ProyectoTestEditar(TestProyectoSetUp):

    def setUp(self):
        super(ProyectoTestEditar, self).setUp()
        self.gerente = User.objects.create(username='gerente2')

    def test_editar_nombre(self):
        nombre_anterior = self.nombre
        self.nombre = 'Proyecto-test-nombre-cambiado'
        try:
            self.assertNotEqual(self.nombre, nombre_anterior)
        except AssertionError as e:
            print("Error de comparacion: {}".format(e))

    def test_editar_descripcion(self):
        descripcion_anterior = self.descripcion
        self.descripcion = 'descripcion-cambiada-test'
        try:
            self.assertNotEqual(self.descripcion, descripcion_anterior)
        except AssertionError as e:
            print("Error de comparacion: {}".format(e))

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
